from typing import List, Tuple, Optional
import json

from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

def fromat_metadata(document):
    return f"""{document.page_content}
    ############# METADATA JSON #############
    {json.dumps(document.metadata, indent=2)}
    """

def build_ingest_chain(graph: Neo4jGraph, vector_store: Neo4jVector, llm: ChatOpenAI) -> None:
    def chain(
        urls: List[str],
        chunk_size: int = 512,
        chunk_overlap: int = 32,
        headers_to_split_on: List[Tuple[str, str]] = [
            ("#", "header 1"),
            ("##", "header 2"),
            ("###", "header 3"),
            ("####", "header 4"),
            ("#####", "header 5"),
            ("######", "header 6"),
        ],
        allowed_nodes: Optional[List[str]] = None,
        allowed_relationships: Optional[List[str]] = None,

    ) -> str:
        from langchain_core.documents import Document
        from langchain_experimental.graph_transformers import LLMGraphTransformer
        from langchain_community.document_loaders import AsyncHtmlLoader

        loader = AsyncHtmlLoader(urls)
        docs = loader.load()

        from langchain_community.document_transformers import MarkdownifyTransformer
        md = MarkdownifyTransformer()
        converted_docs = md.transform_documents(docs)

        llm_converted_docs = []

        from langchain_core.prompts import ChatPromptTemplate

        prompt = ChatPromptTemplate([
            ("system", "You are a data sanitation engine. You have to proccess the input text into a sanitized version of it. Remove noise. Keep as much of the main content as possible. Remove long strips of text representing structured data. Be specific with dates and locations. Your reply should also be a valid markdown file with the same headers as the original markdown. Don't reduce the size of the original fille to less than 1/3 of its length. Always use the full name of things, as example: `Alex` becomes `Alexandru Petre`! Always use the most accurate time description, as example: `1:45` becomes `Monday, June 15, 2009 1:45 PM (en-US)`! When generationg the full names and times use the context for appropriate values. Mark important information as bold. Don't use ```markdown``` sintax, output the markdown text as is!"),
            ("human", "{input}"),
        ])

        # TODO: Gabi
        clean_chain = prompt | llm

        for cdoc in converted_docs:
            llm_converted_docs.append(
                Document(
                    page_content=clean_chain.invoke({"input": cdoc.page_content}).content, 
                    metadata=cdoc.metadata
                )
            )

        from langchain_text_splitters import MarkdownHeaderTextSplitter

        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

        split_docs = []
        for doc in llm_converted_docs:
            for split in markdown_splitter.split_text(doc.page_content):
                split_docs.append(Document(page_content=split.page_content, metadata={**doc.metadata, **split.metadata}))


        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        
        splits = text_splitter.split_documents(split_docs)

        # Extract graph data using OpenAI functions
        llm_graph_transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=allowed_nodes,
            allowed_relationships=allowed_relationships,
            node_properties=False,
            relationship_properties=False,
        )
        graph_documents = llm_graph_transformer.convert_to_graph_documents(splits)

        from hashlib import md5
        vector_store.add_texts(texts=[g.source.page_content for g in graph_documents], metadatas=[g.source.metadata for g in graph_documents], ids=[md5(g.source.page_content.encode("utf-8")).hexdigest() for g in graph_documents])

        from langchain_community.graphs.graph_document import Relationship, Node
        for gd in graph_documents:
            for n in gd.nodes:
                gd.relationships.append(Relationship(source=n, target=Node(id=md5(gd.source.page_content.encode("utf-8")).hexdigest(), type=vector_store.node_label), type='MENTIONED_IN_SOURCE'))

        # Store information into a graph
        graph.add_graph_documents(graph_documents=graph_documents)
        return "Graph construction finished"
    return chain

if __name__ == "__main__":
    from dotenv import load_dotenv
    assert load_dotenv(), "no dotenv"

    from langchain_mongodb.cache import MongoDBCache
    from langchain_core.globals import set_llm_cache
    import os

    set_llm_cache(MongoDBCache(
        connection_string = os.environ.get("MONGO_CONNECTION_STRING"),
        collection_name = "test_cache",
        database_name = "langchain_llm_cache",
    ))

    graph = Neo4jGraph()
    vector_store = Neo4jVector(embedding=OpenAIEmbeddings(model='text-embedding-3-small'))
    llm = ChatOpenAI(model=os.environ.get("OPENAI_MODEL_NAME"), temperature=0)
    
    # Initialize Langfuse handler
    from langfuse.callback import CallbackHandler
    langfuse_handler = CallbackHandler(
        secret_key="sk-lf-4d193bd3-8ca2-4d3b-8df4-18b5ca3bd1e7",
        public_key="pk-lf-d3c9084c-d882-4944-9d66-950930a88d2c",
        host="http://100.66.129.30:3066",
    )

    llm = llm.with_config({"callbacks": [langfuse_handler]})

    chain = build_ingest_chain(graph=graph, vector_store=vector_store, llm=llm)

    print(
        chain(
            urls=["https://en.wikipedia.org/wiki/Attempted_assassination_of_Donald_Trump"],
        )
    )