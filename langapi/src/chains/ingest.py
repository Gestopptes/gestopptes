from typing import List, Tuple, Optional

from langchain_community.graphs import Neo4jGraph
from langchain_openai import ChatOpenAI

def build_ingest_chain(graph: Neo4jGraph, llm: ChatOpenAI) -> None:
    def chain(
        urls: List[str],
        chunk_size: int = 4096,
        chunk_overlap: int = 128,
        headers_to_split_on: List[Tuple[str, str]] = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
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
            ("system", "You are a data sanitation engine. You have to proccess the input text into a sanitized version of it. Remove noise. Keep as much of the main content as possible. Remove long strips of text representing structured data. Be specific with dates and locations. Your reply should also be a valid markdown file with the same headers as the original markdown. Don't reduce the size of the original fille to less than 1/3 of its length. Always use the full name of things, always use the most accurate time description, mark important information as bold."),
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
            node_properties=True,
            relationship_properties=True,
        )
        graph_documents = llm_graph_transformer.convert_to_graph_documents(splits)
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
    llm = ChatOpenAI(model=os.environ.get("OPENAI_MODEL_NAME"), temperature=0)

    chain = build_ingest_chain(graph=graph, llm=llm)

    print(
        chain(
            urls=["https://en.wikipedia.org/wiki/Attempted_assassination_of_Donald_Trump"],
        )
    )