import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearchquerygenerator.elasticsearchquerygenerator import ElasticSearchQuery
from llama_index.vector_stores.elasticsearch import ElasticsearchStore, AsyncDenseVectorStrategy
from llama_index.core import Settings, VectorStoreIndex, QueryBundle
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama
from llama_index.llms.ollama import Ollama
from src.database import Setting
# from src.lib.llama.embeddings import get_embeddings
from embedding_model import get_embed_model, get_embeddings
import asyncio


load_dotenv()

embed_model = OllamaEmbedding("llama3")
Settings.embed_model = embed_model

llm = Ollama(model="llama3", request_timeout=60.0)
Settings.llm = llm

# helper = ElasticSearchQuery(size=1000, BucketName="be2_test_index1")


def init_search():
    # system_text = "Pick one word exactly from the original text. The word must exist in the original text as it is and should not be shortened and must have same spelling. Do not generate a new word. Favour nouns when picking the word. In your response only return the word, nothing else"
    system_text = "I want to search my db with these sentence. Give me the main keywords from it starting with the most important. The most important must exist in the original text as it is and should not be shortened and must have same spelling. Do not generate a new word. Favour nouns when picking the word and do not select a general term from the text if there are more specific terms in the text In your response only return the words seperated by comma, nothing else"
    # system_text = "I want to search my db with these sentence. Give me the main keywords from it starting with the most important. The most important must exist in the original text as it is and should not be shortened and must have same spelling. Do not generate a new word. Favour nouns when picking the word. In your response only return the words seperated by comma, nothing else"
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


# be2_test_contact_ggikz_index
def similarities_with_voyage(query: str, setting: Setting, llm_check=False):
    # Ensure uvloop is not used
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
    print('>>>>set', query, setting.es_index, setting.email, setting.db_host, setting.db_port)
    word_list = get_search_word(query).split(',')
    word_list = [s.strip() for s in word_list]

    # es = Elasticsearch("http://localhost:9200")
    es_url = f"{os.getenv('ELASTICSEARCH_HOST')}:{os.getenv('ELASTICSEARCH_PORT')}"
    try:
        es = Elasticsearch(es_url)
    except Exception as e:
        print(f"Error occured: {e}")
        return {"error": True, "message": e}
    #
    # if llm_check:
    #     dense_vector_store = ElasticsearchStore(
    #         # es_url="http://localhost:9200",  # for Elastic Cloud authentication see above
    #         es_url=es_url,
    #         index_name=setting.es_index,
    #         # index_name="be2_test_index5",
    #         vector_field='description_vector',
    #         text_field='description',
    #         retrieval_strategy=AsyncDenseVectorStrategy(),
    #     )
    #     print('>>>pass1')
    #     index = VectorStoreIndex.from_vector_store(dense_vector_store)
    #     print('>>>pass2')
    #
    #     bundle = QueryBundle(query_str=query,
    #                          embedding=get_embeddings(query))
    #     retriever = index.as_retriever()
    #
    #     results = retriever.retrieve(bundle)
    #     print('>>>pass3', results)
    #
    #     query_engine = index.as_query_engine(llm, similarity_top_k=70)
    #     query_engine = index.as_query_engine(llm)
    #     response = query_engine.query(bundle)
    #
    #     return response

    # elastic search query
    # Constructing the should clause for the words in name_list using wildcard
    print('>>the q', query, word_list)
    # word_list = words
    # word_list = ['Sabryna', "Kes"]
    # Constructing the should clause for the words in name_list using wildcard and match_phrase
    should_clauses = [
        {"wildcard": {"description": {"value": f"*{word}*", "case_insensitive": True}}} for word in word_list
    ]

    should_clauses.extend([{"match_phrase": {"description": query}}])

    print('>>>>shh', should_clauses)

    combined_query = {
        "size": 70,
            "knn": {
                "field": "description_vector",
                "query_vector": get_embeddings(query),
                "k": 15 if llm_check else 7,
                "num_candidates": 15 if llm_check else 10
            },
        "query": {
            "bool": {
                "must": [
                    {
                        "bool": {
                            "should": should_clauses,
                            "minimum_should_match": 1  # At least one should match
                        }
                    },
                    # {
                    #     "wildcard": {
                    #         "description": {"value": "*Sab*"}
                    #     }
                    # },
                ]
            }
        }
    }
    # print('>>>combind', combined_query)

    response = es.search(
        index=setting.es_index,
        body=combined_query
    )

    def process_es_results(es_response):
        nodes = []
        for hit in es_response['hits']['hits']:
            source = hit['_source']
            score = hit['_score']
            name = source.get('name', '')
            # type = source.get('type', '')
            info = source.get('info', '')
            manufacturer = source.get('manufacturer', '')
            release_date = source.get('releaseDate', '')
            description = source.get('description', '')
            # node = TextNode(text=text, metadata=metadata)
            nodes.append({'score': score, 'name': name, 'type': source.get('type', ''), 'info': info,
                          'manufacturer': manufacturer, 'release_date': release_date, 'description': description})
        return nodes

    # print('>>resp', response)
    # return response
    res = process_es_results(response)

    print('>>>is llms check', llm_check, res)
    if llm_check:
        # system_text = f"In the below database records, treat each string seperated by the identifier 'b_seperator;' as its own unique record. This identifier should not be returned. Return only the direct answers, no unneccessary text. Answer this query from it: {query}"
        # system_text = f"In the below database records, treat each string seperated by the identifier 'b_seperator;' as its own unique record. This identifier should not be returned. Your response should be like this: Your search results returned: (response here)"
        system_text = ''
        # tokens = num_tokens_from_string(system_text, set_base)
        # print('>>>system tokens', tokens)

        messages = [
            {"role": "system", "content": system_text, "stream": False},
        ]
        messages_list = [f"{r.get('description')}" for r in res]
        message = ' b_seperator '.join(messages_list)
        # messages.insert(0, f"{query}\n")
        message = f"Answer this query '{query}': " + message
        messages.append({"role": "user", "content": message})
        print('>>>messsages', messages)
        llm_response = ollama.chat(model='llama3', messages=messages)
        print('>>>llm', llm_response)
        return {'words': word_list, 'response': llm_response['message']['content'], 'original': res}


    # from transformers import pipeline
    #
    # # Initialize the pipeline for text generation with the LLaMA model
    # generator = pipeline("text-generation", model="gpt2")
    #
    # # Example input text
    # prompt = "Once upon a time"
    #
    # # Generate text based on the prompt
    # generated_text = generator(prompt, max_length=100)[0]['generated_text']
    #
    # print(generated_text)

    return {'words': word_list, 'response': res}
