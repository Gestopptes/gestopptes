
from src.lama_index.tasks import *
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    while True:
        _in = input(">>> ")
        if _in == 'exit':
            break
        print(chat_with_property_graph(_in))