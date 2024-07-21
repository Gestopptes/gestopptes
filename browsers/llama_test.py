
from src.tasks.lama_index import *
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://en.wikipedia.org/wiki/Attempted_assassination_of_Donald_Trump'


if __name__ == "__main__":
    # lama_index_demo(BASE_URL)

    emb = build_openai_embedings()
    llm = build_ollama_llm()
    index = build_neo4j_index(llm, emb)
    qengine = index.as_query_engine(llm=llm)
    from llama_index.core.llms import ChatMessage
    while True:
        _in = input(">>> ")
        # messages = [
            # ChatMessage(
                # role="system", content="You are a human"
            # ),
            # ChatMessage(role="user", content=_in),
        # ]
        if _in == 'exit':
            break
        # print(llm.chat(messages))
        
        print(qengine.query(_in))