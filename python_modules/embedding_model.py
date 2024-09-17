import os
from dotenv import load_dotenv
from langchain_voyageai import VoyageAIEmbeddings

load_dotenv()


model_name = os.getenv('VOYAGE_MODEL', "")  # Please check https://docs.voyageai.com/docs/embeddings for the available models
voyage_api_key = os.getenv('VOYAGE_API_KEY', "")


def get_embed_model():
    embed_model = VoyageAIEmbeddings(
        model=model_name, voyage_api_key=voyage_api_key
    )
    return embed_model


def get_embeddings(text):
    embed_model = get_embed_model()
    embeddings = embed_model.embed_query(text)

    return embeddings
