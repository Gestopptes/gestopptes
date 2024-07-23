import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from temporalio.worker import SharedStateManager, Worker
from temporalio.client import Client

log = logging.getLogger(__name__)

SELENIUM_COUNT = 6 # we have 9 containers but they sometimes restart
PROCESS_HTML_COUNT = 7

async def worker_selenium():
    from ..config import TEMPORAIO_URL
    from .workflows import Q_SELENIUM_NAME
    from .tasks.download_html import selenium_render_page_to_html

    from .workflows import DownloadWorkflow
    
    client = await Client.connect(TEMPORAIO_URL)
    log.info("building selenium worker...")

    return Worker(
        client,
        task_queue=Q_SELENIUM_NAME,
        workflows=[
            DownloadWorkflow,
        ],
        activities=[
            selenium_render_page_to_html,
        ],
        activity_executor=ProcessPoolExecutor(SELENIUM_COUNT),
        max_concurrent_activities=SELENIUM_COUNT,
        max_concurrent_workflow_tasks=SELENIUM_COUNT * 10 + 10,
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
    )


async def worker_process_html():
    from ..config import TEMPORAIO_URL
    from .workflows import Q_PROCESS_HTML_NAME
    from .tasks.html_extract_links import extract_links_from_url
    from .tasks.html_to_markdown import extract_markdown_from_html

    from .workflows import ScrapeWorkflow, ExtractMarkdownWorkflow
    
    client = await Client.connect(TEMPORAIO_URL)
    log.info("building html processing worker...")

    return Worker(
        client,
        task_queue=Q_PROCESS_HTML_NAME,
        workflows=[
            ScrapeWorkflow,
            ExtractMarkdownWorkflow,
        ],
        activities=[
            extract_links_from_url,
            extract_markdown_from_html,
        ],
        activity_executor=ProcessPoolExecutor(PROCESS_HTML_COUNT),
        max_concurrent_activities=PROCESS_HTML_COUNT,
        max_concurrent_workflow_tasks=PROCESS_HTML_COUNT * 10 + 10,
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
    )