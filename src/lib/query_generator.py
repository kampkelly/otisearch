import json
from typing import List
from src.lib.base import LLMType
from src.lib.openai.openai import OpenAILLM
from python_modules.embedding_model import get_embeddings


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

        return query_json

    def generate_query(self, query: str, columns: List, related_columns: List):
        '''
        Generates a SQL query based on the given question and schemas using the underlying language model.
        Validates the query and raises an error if it is not valid.
        '''
        query = self.llm.generate_query(query, json.dumps(columns), json.dumps(related_columns))
        query_with_vector = self.embed_query_vector(query)
        return query_with_vector
