from temporalio import activity
from ..config import LAMAINDEX_HOST

@activity.defn
def lama_index_demo(url):
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    from ..database import db_get_markdown

    markdown = db_get_markdown(url)
    assert markdown, "no markdown"

    from llama_index.core import Document

    document = Document(text=markdown, metadata={"url": url})

    from llama_index.core.node_parser.relational.markdown_element import MarkdownElementNodeParser

    from llama_index.llms.ollama import Ollama

    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    llm = Ollama(base_url=ollaam_url, model="llama3", request_timeout=1200.0)
    parser = MarkdownElementNodeParser(llm=llm)
    nodes = parser.get_nodes_from_documents([document])

    from llama_index.core import StorageContext
    from llama_index.core.data_structs.data_structs import IndexDict

    from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
    from ..database import MONGO_CLIENT
    store = MongoDBAtlasVectorSearch(MONGO_CLIENT)
    storage_context = StorageContext.from_defaults(vector_store=store)

    from llama_index.core import VectorStoreIndex

    ollama_embedding = OllamaEmbedding(
        model_name="all-minilm",
        base_url=ollaam_url,
        ollama_additional_kwargs={"mirostat": 0},
    )

    index = VectorStoreIndex(
        index_struct=IndexDict(index_id='516d372f-486b-4012-aeb9-2bded2391451', summary=None, nodes_dict={}, doc_id_dict={}, embeddings_dict={}),
        storage_context=storage_context,
        embed_model=ollama_embedding
    )

    index.insert_nodes(nodes=nodes)