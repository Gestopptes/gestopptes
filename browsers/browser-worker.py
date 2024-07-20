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
    import src.webdriver
    import src.tasks
    import src.workflows
    import src.workers
    from src.workflows.scrape import execute_scrape
    from src.database import init_mongo


interrupt_event = asyncio.Event()
async def main():
    init_mongo()
    # Start client

    # Run a worker for the workflow
    worker1 = await src.workers.browser_worker()
    await worker1.run()
    try:
        # Wait indefinitely until the interrupt event is set
        await interrupt_event.wait()
    finally:
        # The worker will be shutdown gracefully due to the async context manager
        print("\nShutting down the worker\n")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nInterrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())