from enum import Enum
from abc import ABC, abstractmethod
from langchain_core.prompts import ChatPromptTemplate


class LLMType(Enum):
    DEFAULT = "default"
    OPENAI = "openai"


class LLMBase(ABC):
    @abstractmethod
    def setup(self):
        '''
        Abstract method to set up the LLM
        '''
        pass

    @abstractmethod
    def get_prompt(self):
        '''
        Abstract method to get the prompt for the LLM
        '''
        pass

    @abstractmethod
    def generate_query(self, question: str, schemas: str):
        '''
        Abstract method to generate a query based on the question and schemas
        '''
        pass

    def validate_query(self, query: str):
        '''
        Validates the generated query
        '''
        return True, ""

    def get_llm_chain(self, prompt: ChatPromptTemplate = None):
        '''
        '''
        chain = (prompt or self.prompt) | self.llm
        return chain
