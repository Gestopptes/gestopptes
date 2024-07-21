
from src.tasks.lama_index import *
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    emb = build_openai_embedings()
    llm = build_ollama_llm()
    index = build_neo4j_property_graph_index(llm, emb)
    qengine = index.as_query_engine(llm=llm)
    while True:
        _in = input(">>> ")
        if _in == 'exit':
            break
        print(qengine.query(_in))