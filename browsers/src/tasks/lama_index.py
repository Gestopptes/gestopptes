from temporalio import activity
from ..config import LAMAINDEX_HOST, LLAMA_MONGO_COLLECTION, LLAMA_INDEX_NAME, LLAMA_MONGO_DB

def build_ollama_embedings():
    from llama_index.embeddings.ollama import OllamaEmbedding
    ollaam_url=f"http://{LAMAINDEX_HOST}:11435"
    ollama_embedding = OllamaEmbedding(
        model_name="all-minilm",
        base_url=ollaam_url,
        ollama_additional_kwargs={"mirostat": 0, "num_ctx": 4096},
        
    )
    return ollama_embedding

def build_ollama_llm():
    from llama_index.llms.ollama import Ollama
    
    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    llm = Ollama(base_url=ollaam_url, model="llama3", request_timeout=1200.0, context_window=128_000,
                 additional_kwargs={
                    # "num_keep": 5,
                    # "seed": 42,
                    # "num_predict": 100,
                    # "top_k": 20,
                    # "top_p": 0.9,
                    # "tfs_z": 0.5,
                    # "typical_p": 0.7,
                    # "repeat_last_n": 33,
                    "temperature": 0.0,
                    # "repeat_penalty": 1.2,
                    # "presence_penalty": 1.5,
                    # "frequency_penalty": 1.0,
                    # "mirostat": 1,
                    # "mirostat_tau": 0.8,
                    # "mirostat_eta": 0.6,
                    # "penalize_newline": true,
                    # "stop": ["\n", "user:"],
                    # "numa": false,
                    # "num_ctx": 1024,
                    # "num_batch": 2,
                    # "num_gqa": 1,
                    "main_gpu": 1,
                    # "low_vram": false,
                    # "f16_kv": true,
                    # "vocab_only": false,
                    "use_mmap": True,
                    # "use_mlock": false,
                    # "embedding_only": false,
                    # "rope_frequency_base": 1.1,
                    # "rope_frequency_scale": 0.8,
                    # "num_thread": 8
                })
    return llm

def build_neo4j_index(llm, emb):
    from typing import Literal
    from llama_index.core import PropertyGraphIndex
    from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

    from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

    # best practice to use upper-case
    entities = Literal["PERSON", "PLACE", "ORGANIZATION"]
    relations = Literal["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"]

    # define which entities can have which relations
    validation_schema = {
        "PERSON": ["HAS", "PART_OF", "WORKED_ON", "WORKED_WITH", "WORKED_AT"],
        "PLACE": ["HAS", "PART_OF", "WORKED_AT"],
        "ORGANIZATION": ["HAS", "PART_OF", "WORKED_WITH"],
    }

    kg_extractor = SchemaLLMPathExtractor(
        llm=llm,
        possible_entities=entities,
        possible_relations=relations,
        kg_validation_schema=validation_schema,
        strict=True,
    )
    graph_store = Neo4jPropertyGraphStore(
        username="neo4j",
        password="your_password",
        url="bolt://100.66.129.30:7687",
    )
    index = PropertyGraphIndex(
        llm=llm,
        embed_model=emb,
        kg_extractors=[kg_extractor],
        property_graph_store=graph_store,
        show_progress=True,
    )

    return index

@activity.defn
def lama_index_demo(url):
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    from ..database import db_get_markdown

    markdown = db_get_markdown(url)
    assert markdown, "no markdown"

    from llama_index.core import Document

    document = Document(text=markdown, metadata={"url": url})

    from llama_index.core.node_parser.relational.markdown_element import MarkdownElementNodeParser

    llm = build_ollama_llm()
    parser = MarkdownElementNodeParser(llm=llm)
    nodes = parser.get_nodes_from_documents([document])

    emb = build_ollama_embedings()
    index = build_neo4j_index(llm, emb)

    index.insert_nodes(nodes=nodes)