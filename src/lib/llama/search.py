from elasticsearchquerygenerator.elasticsearchquerygenerator import ElasticSearchQuery
from llama_index.vector_stores.elasticsearch import ElasticsearchStore, AsyncDenseVectorStrategy
from llama_index.core import Settings, VectorStoreIndex, QueryBundle
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama
from llama_index.llms.ollama import Ollama
from src.database import Setting

from src.lib.llama.embeddings import get_embeddings

embed_model = OllamaEmbedding("llama3")
Settings.embed_model = embed_model

llm = Ollama(model="llama3", request_timeout=60.0)
Settings.llm = llm

helper = ElasticSearchQuery(size=1000, BucketName="be2_test_index1")


def init_search():
    system_text = "Pick one word exactly from the original text. The word must exist in the original text as it is and should not be shortened and must have same spelling. Do not generate a new word. Favour nouns when picking the word. In your response only return the word, nothing else"

    messages = [
        {"role": "system", "content": system_text, "stream": False},
    ]

    response = ollama.chat(model='llama3', messages=messages)
    return response, messages


def get_search_word(q: str) -> str:
    """Returns the most similar word to the query string."""
    _, messages = init_search()
    messages.append({"role": "user", "content": q})
    response = ollama.chat(model='llama3', messages=messages)

    return response['message']['content']


def similarities(query: str, setting: Setting):
    # word = get_search_word(query)
    dense_vector_store = ElasticsearchStore(
        es_url="http://localhost:9200",
        index_name=setting.es_index,
        vector_field='description_vector',
        text_field='description',
        retrieval_strategy=AsyncDenseVectorStrategy(),
    )
    index = VectorStoreIndex.from_vector_store(dense_vector_store)

    bundle = QueryBundle(query_str=query,
                         embedding=get_embeddings(query))
    retriever = index.as_retriever()
    results = retriever.retrieve(bundle)

    query_engine = index.as_query_engine(llm, similarity_top_k=70)
    response = query_engine.query(bundle)

    return response
