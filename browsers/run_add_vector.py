
from src.lama_index.tasks import *
from dotenv import load_dotenv

load_dotenv()

BASE_URL = 'https://en.wikipedia.org/wiki/Attempted_assassination_of_Donald_Trump'

if __name__ == "__main__":
    lama_index_url2neo4j_vector_index(BASE_URL, {})