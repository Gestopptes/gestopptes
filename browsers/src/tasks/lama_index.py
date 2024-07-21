from temporalio import activity
from ..config import LAMAINDEX_HOST

def build_openai_embedings():
    from llama_index.embeddings.openai import OpenAIEmbedding
    return OpenAIEmbedding(model="text-embedding-3-large")

def build_ollama_embedings():
    from llama_index.embeddings.ollama import OllamaEmbedding
    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    ollama_embedding = OllamaEmbedding(
        model_name="all-minilm",
        base_url=ollaam_url,
        ollama_additional_kwargs={"mirostat": 0, "num_ctx": 4096},
        
    )
    return ollama_embedding

def build_openai_llm():
    from llama_index.llms.openai import OpenAI
    return OpenAI(model="gpt-4o-mini")

def build_ollama_llm():
    from llama_index.llms.ollama import Ollama
    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    llm = Ollama(base_url=ollaam_url, model="llama3", request_timeout=1200.0,
                 additional_kwargs={
                    "temperature": 0.0, "num_ctx": 32_768
                })
    return llm

from llama_index.core import PropertyGraphIndex

def build_neo4j_index(llm, emb) -> PropertyGraphIndex:
    from typing import Literal
    from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

    from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

    # best practice to use upper-case
    entities = Literal["person", "nonprofit organization", "organization", "event", "fact", "product", "work of art", "law", "money", "percent", "quantity", "ordinal", "cardinal", "date", "time", "language", "geopolitical entity", "location"]
    relations = Literal["cause", "causing", "caused by", "because", "since", "after", "for", "as and of"]

    # define which entities can have which relations
    validation_schema = {
        "person": relations,
        "nonprofit organization": relations,
        "organization": relations,
        "event": relations,
        "fact": relations,
        "product": relations,
        "work of art": relations,
        "law": relations,
        "money": relations,
        "percent": relations,
        "quantity": relations,
        "ordinal": relations,
        "cardinal": relations,
        "date": relations,
        "time": relations,
        "language": relations,
        "geopolitical entity": relations,
        "location": relations,
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
    index = PropertyGraphIndex.from_documents(
        [],
        llm=llm,
        embed_model=emb,
        kg_extractors=[kg_extractor],
        property_graph_store=graph_store,
        show_progress=True,
    )

    return index

@activity.defn
def lama_index_demo(url, options):
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    from ..database import db_get_markdown

    markdown = db_get_markdown(url)
    assert markdown, "no markdown"

    from llama_index.core import Document

    document = Document(text=markdown, metadata={"url": url})

    from llama_index.core.node_parser.relational.markdown_element import MarkdownElementNodeParser

    llm = build_openai_llm()
    parser = MarkdownElementNodeParser(llm=llm)
    nodes = parser.get_nodes_from_documents([document])

    emb = build_openai_embedings()
    index = build_neo4j_index(llm, emb)

    index.insert_nodes(nodes=nodes[:10])