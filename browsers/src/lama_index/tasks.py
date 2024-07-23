from temporalio import activity

def build_openai_embedings():
    from ..config import LAMAINDEX_HOST
    from llama_index.embeddings.openai import OpenAIEmbedding
    return OpenAIEmbedding(model="text-embedding-3-large", api_base=f"http://{LAMAINDEX_HOST}:11333/v1")

def build_ollama_embedings():
    from ..config import LAMAINDEX_HOST
    from llama_index.embeddings.ollama import OllamaEmbedding
    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    ollama_embedding = OllamaEmbedding(
        model_name="all-minilm",
        base_url=ollaam_url,
        ollama_additional_kwargs={"mirostat": 0, "num_ctx": 4096},
        
    )
    return ollama_embedding

def build_openai_llm():
    from ..config import LAMAINDEX_HOST
    from llama_index.llms.openai import OpenAI
    return OpenAI(model="gpt-4o-mini", api_base=f"http://{LAMAINDEX_HOST}:11333/v1", temperature=0)

def build_ollama_llm():
    from ..config import LAMAINDEX_HOST
    from llama_index.llms.ollama import Ollama
    ollaam_url=f"http://{LAMAINDEX_HOST}:11434"
    llm = Ollama(base_url=ollaam_url, model="llama3", request_timeout=1200.0,
                 additional_kwargs={
                    "temperature": 0.0, "num_ctx": 32_768
                })
    return llm

def build_neo4j_vector_index(emb, documents=[]):
    from ..config import NEO4J_HOSTNAME
    from llama_index.core import VectorStoreIndex
    from llama_index.vector_stores.neo4jvector import Neo4jVectorStore
    neo4j_vector = Neo4jVectorStore(
        embedding_dimension = 1536,
        hybrid_search=True,
        username="neo4j",
        password="your_password",
        url=f"bolt://{NEO4J_HOSTNAME}:7687",
    )

    from llama_index.core import StorageContext

    storage_context = StorageContext.from_defaults(vector_store=neo4j_vector)
    from llama_index.core.node_parser import TokenTextSplitter
    from llama_index.core.ingestion import IngestionPipeline
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=2*1024,
                chunk_overlap=256,
                separator="\n",
                backup_separators=[" "],
            ),
        ],
    )
    if documents:
        return VectorStoreIndex(
            nodes=pipeline.run(documents=documents),
            storage_context=storage_context,
            embed_model=emb,
        )
    return VectorStoreIndex.from_documents(
        [],
        storage_context=storage_context,
        embed_model=emb,
    )


@activity.defn
def lama_index_url2neo4j_vector_index(url, options):
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    from ..database import db_get_markdown

    markdown = db_get_markdown(url)
    assert markdown, "no markdown"

    import re
    markdown = re.sub(r"[(.+)](.+)", r"\1", markdown)

    from llama_index.core import Document

    document = Document(text=markdown, metadata={"url": url})

    # emb = build_openai_embedings()
    emb = build_ollama_embedings()
    index = build_neo4j_vector_index(emb, documents=[document])


def build_neo4j_property_graph_index(llm, emb, documents=[]):
    from ..config import NEO4J_HOSTNAME
    from llama_index.core import PropertyGraphIndex
    from typing import Literal
    from llama_index.core.indices.property_graph import SchemaLLMPathExtractor

    from llama_index.graph_stores.neo4j import Neo4jPropertyGraphStore

    # best practice to use upper-case
    kg_extractors = [
        SchemaLLMPathExtractor(
            llm=llm,
            possible_entities=Literal["person", "nonprofit_organization", "organization", "event", "fact", "product", "work_of_art", "law", "money", "percent", "quantity", "ordinal", "cardinal", "date", "time", "language", "geopolitical_entity", "location"],
            possible_relations=["cause", "causing", "caused_by", "because", "since", "after", "for", "as_and_of"],
            num_workers=1,
            max_triplets_per_chunk=60,
            strict=False,
        ),
    ]
    graph_store = Neo4jPropertyGraphStore(
        username="neo4j",
        password="your_password",
        url=f"bolt://{NEO4J_HOSTNAME}:7687",
        # database="trump"
    )
    
    from llama_index.core.node_parser import TokenTextSplitter
    from llama_index.core.ingestion import IngestionPipeline
    pipeline = IngestionPipeline(
        transformations=[
            TokenTextSplitter(
                chunk_size=2*1024,
                chunk_overlap=256,
                separator="\n",
                backup_separators=[" "],
            ),
        ],
    )
    if documents:
        return PropertyGraphIndex(
            nodes=pipeline.run(documents=documents),
            llm=llm,
            embed_model=emb,
            kg_extractors=kg_extractors,
            property_graph_store=graph_store,
            show_progress=True,
        )
    return PropertyGraphIndex.from_documents(
            documents=[],
            llm=llm,
            embed_model=emb,
            kg_extractors=kg_extractors,
            property_graph_store=graph_store,
            show_progress=True,
        )


@activity.defn
def lama_index_url2neo4j_property_graph_index(url, options):
    from llama_index.core.node_parser.file.markdown import MarkdownNodeParser 

    from ..database import db_get_markdown

    markdown = db_get_markdown(url)
    assert markdown, "no markdown"

    import re
    markdown = re.sub(r"[(.+)](.+)", r"\1", markdown)

    from llama_index.core import Document

    document = Document(text=markdown, metadata={"url": url})

    llm = build_openai_llm()
    emb = build_openai_embedings()
    index = build_neo4j_property_graph_index(llm, emb, documents=[document])



@activity.defn
def chat_with_property_graph(input):
    emb = build_ollama_embedings()
    llm = build_ollama_llm()
    index = build_neo4j_property_graph_index(llm, emb)
    qengine = index.as_query_engine(llm=llm)
    return qengine.query(input)


@activity.defn
def chat_with_vectors(input):
    emb = build_openai_embedings()
    llm = build_ollama_llm()
    index = build_neo4j_vector_index(llm, emb)
    ret = index.as_retriever()
    return ret.retrieve(input)


@activity.defn
def chat_ollama(messages):
    llm = build_ollama_llm()
    return llm.chat(messages)