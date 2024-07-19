
from src.tasks.lama_index import lama_index_demo


BASE_URL = 'https://github.com/langchain-ai/langchain/tree/langchain%3D%3D0.2.6/templates/csv-agent'


if __name__ == "__main__":
    lama_index_demo(BASE_URL)