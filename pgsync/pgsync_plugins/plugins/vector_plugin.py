from pgsync import plugin
import copy
from dotenv import load_dotenv
import time
from embedding_model import get_embeddings

load_dotenv


class VectorPlugin(plugin.Plugin):
    name = 'Vector'

    def transform(self, original_doc, **kwargs):
        doc = copy.deepcopy(original_doc)
        if "_meta" in doc:
            del doc["_meta"]

        doc_result = ' '.join([f"{key}: {value}" for key, value in doc.items()]).strip()

        # to avoid hitting embedding_model rate limit
        time.sleep(0.5)

        reduced_embedding = get_embeddings(doc_result)

        doc['search_vectors'] = reduced_embedding

        return doc
