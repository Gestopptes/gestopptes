from temporalio import activity
from ..config import LAMAINDEX_HOST

@activity.defn
def lama_index_demo(url):
    from llama_index.embeddings.ollama import OllamaEmbedding
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    ollama_embedding = OllamaEmbedding(
        model_name="all-minilm",
        base_url=f"http://{LAMAINDEX_HOST}:11434",
        ollama_additional_kwargs={"mirostat": 0},
    )

    pass_embedding = ollama_embedding.get_text_embedding_batch(
        ["This is a passage!", "This is another passage"], show_progress=True
    )
    print(len(pass_embedding))

    query_embedding = ollama_embedding.get_query_embedding("Where is blue?")
    print(len(query_embedding))