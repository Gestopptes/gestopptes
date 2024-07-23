import os

TEMPORAIO_URL = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
MONGO_HOSTNAME = os.getenv("MONGO_HOSTNAME", "localhost")
SELENIUM_IP = os.getenv("SELENIUM_IP", "localhost")
IFRAME_IP = os.getenv("IFRAME_IP", "localhost")
NEO4J_HOSTNAME = os.getenv("NEO4J_HOSTNAME","localhost")

TASK_VERSION = "v8"


DEFAULT_TASK_Q = "default-gestopptes"
DEFAULT_ACTIVITY_TIMEOUT = 20
SELENIUM_PAGE_LOAD_TIMEOUT = 13


LAMAINDEX_PORT =  os.getenv("LLAMAINDEX_PORT", "11434")
LAMAINDEX_HOST = os.getenv("LLAMAINDEX_HOST", "localhost")


LAMAINDEX_PORT_NOPROXY =  os.getenv("LLAMAINDEX_PORT_NOPROXY", "11434")
LAMAINDEX_HOST_NOPROXY = os.getenv("LLAMAINDEX_HOST_NOPROXY", "localhost")

LLAMA_MONGO_COLLECTION = 'llama_index'
LLAMA_MONGO_DB = 'llama_db'
LLAMA_INDEX_NAME = 'all_minilm_ollama'


GPU_COUNT = int(os.getenv("WORKER_GPU_COUNT", "1"))