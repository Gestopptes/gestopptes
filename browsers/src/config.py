import os

TEMPORAIO_URL = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
MONGO_HOSTNAME = os.getenv("MONGO_HOSTNAME", "localhost")
SELENIUM_ADDRESS = os.getenv("SELENIUM_ADDRESS", "http://localhost:4444")
IFRAME_IP = os.getenv("IFRAME_IP", "localhost")

SCRAPE_TASK_VERSION = "v8"


Q_BROWSERS = "q-browsers"
Q_BROWSERS_PROCESS_COUNT = 6

# Q_CPU_PROCESSING = "q-cpu-processing"
# Q_CPU_PROCESS_COUNT = 8


PAGE_LOAD_TIMEOUT = 13
ACTIVITY_TIMEOUT = 300


LAMAINDEX_PORT = 11434
LAMAINDEX_HOST = os.getenv("LLAMAINDEX_HOST", "localhost")
LLAMA_MONGO_COLLECTION = 'llama_index'
LLAMA_MONGO_DB = 'llama_db'
LLAMA_INDEX_NAME = 'all_minilm_ollama'