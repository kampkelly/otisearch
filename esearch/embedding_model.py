import os
from llama_index.embeddings.voyageai import VoyageEmbedding
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# # Set the high watermark limit for memory allocations on MPS backend to 0.0
# os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

model_name = "voyage-large-2-instruct"
voyage_api_key = os.environ.get("VOYAGE_API_KEY", "your-api-key")


def get_embed_model():
    embed_model = VoyageEmbedding(
        model_name=model_name, voyage_api_key=voyage_api_key
    )
    return embed_model


def get_embeddings(text):
    embed_model = get_embed_model()
    embeddings = embed_model.get_query_embedding(text)
    return embeddings

# ###### Using the Hugging Face embedding model
# _embed_model = None
#
# def get_embed_model():
#     global _embed_model
#     if _embed_model is None:
#         _embed_model = HuggingFaceEmbedding(model_name="Salesforce/SFR-Embedding-Mistral")
#     return _embed_model
#
#
# def get_embeddings(text):
#     embed_model = get_embed_model()
#     embeddings = embed_model.get_text_embedding(text)
#     return embeddings
