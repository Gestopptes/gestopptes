import logging
import os
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex


logger = logging.getLogger("uvicorn")


def get_index():
    from llama_index.core import StorageContext
    from llama_index.core.data_structs.data_structs import IndexDict

    from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
    from ....browsers.src.database import MONGO_CLIENT
    from ....browsers.src.config import LLAMA_MONGO_COLLECTION, LLAMA_INDEX_NAME, LLAMA_MONGO_DB
    store = MongoDBAtlasVectorSearch(MONGO_CLIENT, db_name=LLAMA_MONGO_DB, collection_name=LLAMA_MONGO_COLLECTION, index_name=LLAMA_INDEX_NAME)
    storage_context = StorageContext.from_defaults(vector_store=store)

    from llama_index.core import VectorStoreIndex

    index = VectorStoreIndex(
        index_struct=IndexDict(index_id=LLAMA_INDEX_NAME, summary=None, nodes_dict={}, doc_id_dict={}, embeddings_dict={}),
        storage_context=storage_context,
    )
    return index
