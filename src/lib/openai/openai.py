import os
import json
from typing import List
from dotenv import load_dotenv
from src.lib.base import LLMBase
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.helpers.errors import QueryGeneratorError
from src.lib.prompts import get_messages

load_dotenv()


class OpenAILLM(LLMBase):
    def __init__(self, **kwargs):
        '''
        Initializes the OpenAI class
        '''
        self.api_key = os.getenv('OPENAI_API_KEY', "")
        self.prompt = ""
        self.llm = None

    def setup(self):
        '''
        Sets up the SQLGeneratorLLM by getting the model and tokenizer
        '''
        try:
            self.get_prompt()
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                api_key=self.api_key
            )
            self.llm = llm
        except Exception as e:
            raise QueryGeneratorError(e)

    def get_prompt(self):
        '''
        Generates the prompt template
        '''
        messages = [
            ("system", get_messages()),
        ]

        messages.extend([
            ("human", """
                    Text: {query}
                    Columns: {columns}
                    related_columns: {related_columns}
                    Query:
                    """)
        ])
        self.prompt = ChatPromptTemplate.from_messages(messages)

    def _get_query(self, query: str, columns: List, related_columns: List):
        '''
        Gets the SQL query based on the question and schemas
        '''
        chain = self.get_llm_chain()
        result = chain.invoke(
            {
                "query": query,
                "columns": columns,
                "related_columns": related_columns
            }
        )
        return result.content

    def format_response(self, jsonStr: str):
        # Strip the ```json and ```
        jsonString = jsonStr.strip('```json').strip('```')

        try:
            formatted_json = json.loads(jsonString)
            return formatted_json
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return jsonStr

    def generate_query(self, query: str, columns: List, related_columns: List):
        '''
        Generates the SQL query based on the question and schemas
        '''
        query = self._get_query(query, columns, related_columns)
        return self.format_response(query)
