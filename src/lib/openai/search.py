import os
import openai
import tiktoken
from dotenv import load_dotenv
from esearch.index import ESearch
from fastapi.responses import JSONResponse
from src.database import Setting

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
set_base = "cl100k_base"

EMBEDDING_MODEL = "text-embedding-3-large"


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def init_search():
    system_text = "Pick one word exactly from the original text. Do not generate a new word. Favour nouns when picking the word"

    # tokens = num_tokens_from_string(system_text, set_base)

    messages = [
        {"role": "system", "content": system_text},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response, messages


def get_search_word(q: str) -> str:
    """Returns the most similar word to the query string."""
    _, messages = init_search()
    messages.append({"role": "user", "content": q})
    # tokens = num_tokens_from_string(q, set_base)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content


def similarities(question: str, setting: Setting):
    word = get_search_word(question)

    def pretty_response(response):
        output = []
        for hit in response['hits']['hits']:
            score = hit['_score']
            result = {key: value for key, value in hit['_source'].items() if key != 'description_vector'}

            pretty_output = (f"\nSummary: {result}\nScore: {score}")
            print(pretty_output)
            output.append(pretty_output)

        return output

    es = ESearch()
    question_embedding = openai.Embedding.create(input=word, model=EMBEDDING_MODEL, dimensions=1024)

    body = {
        "knn": {
            "field": "description_vector",
            "query_vector": question_embedding["data"][0]["embedding"],
            "k": 5,
            "num_candidates": 10
        },
        "size": 10,
    }
    resp = es.client.search(
        index=setting.es_index,
        body=body
    )
    response_data = pretty_response(resp)
    return JSONResponse(content=response_data)
