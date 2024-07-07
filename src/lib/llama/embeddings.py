from sklearn.random_projection import GaussianRandomProjection
import ollama
import numpy as np


def get_embeddings(query: str):
    def normalize_l2(text):
        val_embedding = ollama.embeddings(model='llama3', prompt=text)
        cut_dim = val_embedding.get("embedding")[:1024]
        x = np.array(cut_dim)
        if x.ndim == 1:
            norm = np.linalg.norm(x)
            if norm == 0:
                reduced_embedding = x
            else:
                reduced_embedding = x / norm
        else:
            norm = np.linalg.norm(x, 2, axis=1, keepdims=True)
            reduced_embedding = np.where(norm == 0, x, x / norm)

        reduced_embedding = reduced_embedding.tolist()
        return reduced_embedding

    # Gaussian Random Projection
    def grp(text):
        val_embedding = ollama.embeddings(model='llama3', prompt=text)
        val_embedding_array = np.array(val_embedding.get("embedding"))

        transformer = GaussianRandomProjection(n_components=1024)
        reduced_embedding = transformer.fit_transform(val_embedding_array.reshape(1, -1))

        # Flatten the result back to 1D
        reduced_embedding = reduced_embedding.flatten()

        # return reduced_embedding
        return reduced_embedding.tolist()

    return normalize_l2(query)
