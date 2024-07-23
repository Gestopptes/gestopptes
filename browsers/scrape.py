import asyncio
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import timedelta

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import SharedStateManager, Worker


import logging
logging.basicConfig(level=logging.INFO)

with workflow.unsafe.imports_passed_through():
    import src
    import src.config
    import src.database
    import src.browsers.webdriver
    import src.lama_index
    import src.browsers.workers

    from src.browsers.workflows import run_scrape

    from src.database import init_mongo


BASE_URL = 'https://github.com/langchain-ai/langchain/tree/langchain%3D%3D0.2.6/templates/csv-agent'
SCRAPE_CLASS = 'Link--primary'
# BASE_URL = 'https://sparganothis.org'
# BASE_URL = "https://stackoverflow.com/questions/62649161/how-long-does-temporal-guarantee-id-uniqueness"
MAX_DEPTH = 3
# SCRAPE_CLASS = None

async def main():
    init_mongo()
    # Start client

    # Run a worker for the workflow
    worker1 = await src.browsers.workers.worker_selenium()
    async with worker1:
        # async with src.workers.cpu_worker(client):
        x = await run_scrape(BASE_URL, MAX_DEPTH, SCRAPE_CLASS)
        print(f"finished scrape: total pages = {x}")


if __name__ == "__main__":
    asyncio.run(main())