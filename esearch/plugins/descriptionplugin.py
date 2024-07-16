from pgsync import plugin

# from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np
import time
from embedding_model import get_embed_model, get_embeddings

text = ["This is a sample document."]


def normalize_l2(x):
    x = np.array(x)
    if x.ndim == 1:
        norm = np.linalg.norm(x)
        if norm == 0:
            return x
        return x / norm
    else:
        norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
        return np.where(norm == 0, x, x / norm)


class DescriptionPlugin(plugin.Plugin):
    name = 'Description'

    def transform(self, doc, **kwargs):
        # columns = ["firstName", "lastName", "gender", "phone", 'goode', "dateOfBirth", "email", "citizenship", "address", "contactType", "insuranceProvider", "zohoInvoiceCustomerID"]
        columns = ["firstName"]
        metadata = {col: doc.get(col, None) for col in columns}

        result = '; '.join([f"{doc.get(col, None)}" for col in columns]) + ';'
        time.sleep(0.5)  # to avoid passing rate limit on Voyage per minute

        if result:
            val = result

            # ###### openai implementation
            # EMBEDDING_MODEL = "text-embedding-3-large"
            # val_embedding = openai.Embedding.create(input=val, model=EMBEDDING_MODEL, dimensions=1024)
            # val_embedding = ollama.embeddings(model='llama3', prompt=val)
            # doc['description_vector'] = val_embedding

            # ###### llama implementation
            # val_embedding = ollama.embeddings(model='llama3', prompt=val)
            # val_embedding_array = np.array(val_embedding.get("embedding"))

            # # Apply PCA or Gaussian random projection to reduce the dimensions to 1024
            # transformer = GaussianRandomProjection(n_components=1024)
            # reduced_embedding = transformer.fit_transform(val_embedding_array.reshape(1, -1))
            # # # Flatten the result back to 1D
            # reduced_embedding = reduced_embedding.flatten()
            # reduced_embedding = reduced_embedding.tolist()

            # Use l2 normalization
            # cut_dim = val_embedding.get("embedding")[:1024]
            # norm_dim = normalize_l2(cut_dim)
            # reduced_embedding = norm_dim.tolist()
            # Use l2 normalization
            # ###### llama implementation

            # ###### Use voyage-large-2-instruct
            reduced_embedding = get_embeddings(val)
            # ###### Use voyage-large-2-instruct

            doc['description'] = val
            doc['metadata'] = metadata
            doc['description_vector'] = reduced_embedding
        else:
            doc['description'] = ""
            doc['description_vector'] = []
            doc['metadata'] = {}

        print('>>>>>finished one record')

        return doc
