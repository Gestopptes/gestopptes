
from src.tasks.lama_index import *
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    llm = build_ollama_llm()
    from llama_index.core.llms import ChatMessage
    while True:
        _in = input(">>> ")
        messages = [
            ChatMessage(
                role="system", content="You are a human"
            ),
            ChatMessage(role="user", content=_in),
        ]
        if _in == 'exit':
            break
        print(llm.chat(messages))