import os

TEMPORAIO_URL = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
MONGO_HOSTNAME = os.getenv("MONGO_HOSTNAME", "localhost")
SELENIUM_ADDRESS = os.getenv("SELENIUM_ADDRESS", "http://localhost:4444")


SCRAPE_TASK_VERSION = "v8"


Q_BROWSERS = "q-browsers"
Q_BROWSERS_PROCESS_COUNT = 6

# Q_CPU_PROCESSING = "q-cpu-processing"
# Q_CPU_PROCESS_COUNT = 8


PAGE_LOAD_TIMEOUT = 13
ACTIVITY_TIMEOUT = 15