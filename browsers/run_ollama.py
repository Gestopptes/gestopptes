
from src.lama_index.tasks import *
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
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
        print(chat_ollama(messages))