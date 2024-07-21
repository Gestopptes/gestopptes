
from src.tasks.lama_index import *
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    emb = build_openai_embedings()
    llm = build_ollama_llm()
    index = build_neo4j_vector_index(llm, emb)
    ret = index.as_retriever()
    while True:
        _in = input(">>> ")
        if _in == 'exit':
            break
        
        print(ret.retrieve(_in))