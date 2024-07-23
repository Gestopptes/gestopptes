import asyncio
import logging
from temporalio import workflow

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


with workflow.unsafe.imports_passed_through():
    from werkzeug._reloader import run_with_reloader
    from src.browsers.workers import worker_process_html, worker_selenium
    from src.lama_index.workers import worker_gpu
    from src.database import init_mongo


interrupt_event = asyncio.Event()
async def async_main():
    init_mongo()
    # Start client

    # Run a worker for the workflow
    await asyncio.gather(
        (await worker_process_html()).run(),
        (await worker_selenium()).run(),
        (await worker_gpu()).run(),
    )
    try:
        # Wait indefinitely until the interrupt event is set
        await interrupt_event.wait()
    finally:
        # The worker will be shutdown gracefully due to the async context manager
        log.warning("\nShutting down the worker\n")


def sync_main():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(async_main())
    except KeyboardInterrupt:
        log.info("\nInterrupt received, shutting down...\n")
        interrupt_event.set()
        loop.run_until_complete(loop.shutdown_asyncgens())


if __name__ == "__main__":
    import glob
    src_py_glob = list(glob.glob("./src/**/*.py"))
    run_with_reloader(
        sync_main,
        extra_files=src_py_glob,
        reloader_type="stat", 
        interval=3)