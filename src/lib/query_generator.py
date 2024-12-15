import json
from dotenv import load_dotenv
from typing import List, Any
from src.lib.base import LLMType
from src.lib.openai.openai import OpenAILLM
from python_modules.embedding_model import get_embeddings, get_embed_model
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import create_retrieval_chain
from langchain.agents import (
    Tool,
    AgentExecutor,
    create_react_agent
)
from src.lib.esearch.custom import CustomElasticsearchRetriever
from src.lib.esearch.query import ESearchQuery

load_dotenv


class QueryGeneratorFactory:
    @staticmethod
    def get_setting(llm_type, **kwargs):
        '''
        Returns the appropriate SQL generator based on the specified LLM type.

        Args:
            llm_type (LLMType): The type of language model to use.
            **kwargs: Additional keyword arguments for initializing the specific SQL generator.

        Returns:
            SQLGeneratorLLM or OpenAILLM: An instance of the selected SQL generator based on the LLM type.

        Raises:
            ValueError: If the specified LLM type is unknown.
        '''
        if llm_type == LLMType.DEFAULT:
            return OpenAILLM(**kwargs)
        elif llm_type == LLMType.OPENAI:
            return OpenAILLM(**kwargs)
        else:
            raise ValueError("Unknown llm type")


class QueryGenerator:
    def __init__(self, setting_type: LLMType, **kwargs):
        self.llm = QueryGeneratorFactory.get_setting(setting_type, **kwargs)

    def setup(self):
        '''
        Sets up the SQLGenerator by calling the setup method of the underlying language model.
        '''
        return self.llm.setup()

    def embed_query_vector(self, query_json: dict) -> dict:
        query_vector = query_json.get("knn", {}).get("query_vector", "")

        if query_vector.startswith("<") and query_vector.endswith(">"):
            # Extract the text between < and >
            text_to_embed = query_vector[1:-1]

            # Get the embedding for the extracted text
            embedding = get_embeddings(text_to_embed)

            # Replace the query_vector with the embedding
            query_json["knn"]["query_vector"] = embedding
        elif query_vector:
            # Extract the text between < and >
            text_to_embed = query_vector

            # Get the embedding for the extracted text
            embedding = get_embeddings(text_to_embed)

            # Replace the query_vector with the embedding
            query_json["knn"]["query_vector"] = embedding

        return query_json

    def generate_query(self, query: str, columns: List, related_columns: List):
        '''
        Generates a SQL query based on the given question and schemas using the underlying language model.
        Validates the query and raises an error if it is not valid.
        '''
        query = self.llm.generate_query(query, json.dumps(columns), json.dumps(related_columns))
        query_with_vector = self.embed_query_vector(query)
        return query_with_vector

    def get_prompt(self, msg: str = None):
        '''

        '''
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assitant assiting users to find information from database data. The users query may contain little mistakes and spelling mistakes,
                    so if you see any similar information, report it and explain the similarity. The final answer must come from the database.
                    You have access to the following tools {tool_names} to use to assist in searching the database:\n\n
                    {tools}\n\n

                    Use the following format:\n\n

                    Question: the input query you must answer\n
                    Thought: You should always think about what to do, always use the Query_database at least once.\n
                    Action: the action to take, it can only be one of [{tool_names}]\n
                    Action Input: the input to the action\n
                    Observation: the result of the action\n
                    ... (this Thought/Action/Action Input/Observation can repeat not more than N times)\n\n

                    When you have a final response from database only, you MUST use the format:\n
                    Thought: I now know the final answer to the original query and I dont need to use a tool? Yes\n
                    Final Answer: [your response here]\n
                    Begin
                    """
                ),
                ("human", "{input}"),
                ("human", "{agent_scratchpad}"),
            ]
        )

        return prompt

    def retrieve_insights(self, query: str, es_index_name: str, columns: Any, related_columns: Any):
        '''

        '''
        esearch = ESearchQuery()
        es_client = esearch.esearch_client
        custom_retriever = CustomElasticsearchRetriever(index_name=es_index_name, esearch_client=es_client, columns=columns,
                                                        related_columns=related_columns, generate_query=self.generate_query)

        prompt = self.get_prompt()
        llm_chain = self.llm.get_llm_chain(prompt)
        # use llama here or another open source model good for reasoning tasks for llm_chain.
        # but custom_retriever should use best model for code generation
        rag_chain = create_retrieval_chain(custom_retriever, llm_chain)
        tools = [
            Tool(
                name="Query_database",
                func=lambda x, **kwargs: rag_chain.invoke({
                    "input": x,
                    "tool_names": kwargs.get("tools", ""),
                    "tools": kwargs.get("tool_names", ""),
                    "agent_scratchpad": kwargs.get("agent_scratchpad", ""),
                }),
                description="Use for querying. This is a retrieval tool used to answer users search request. It takes as input a string for what the user is searching for."
            )
        ]
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True, input_key="input")

        # you can use llama here or another open source model good for reasoning tasks
        agent = create_react_agent(self.llm.llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools,
            verbose=True,
            memory=memory,
            return_intermediate_steps=True,
            handle_parsing_errors=True,
            max_iterations=4
        )

        tool_names = [tool.name for tool in tools]
        tool_descriptions = "\n".join([f"{tool.name}: {tool.description}" for tool in tools])

        result = agent_executor.invoke({
            "input": query,
            "tool_names": ", ".join(tool_names),
            "tools": tool_descriptions,
            "agent_scratchpad": []
        })

        return result["output"]
