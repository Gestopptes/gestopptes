from temporalio import  workflow
import asyncio

from datetime import timedelta
import asyncio
from temporalio.common import RetryPolicy


from ..config import TASK_VERSION, SELENIUM_PAGE_LOAD_TIMEOUT
from ..tempo_helpers import execute_child_workflow, execute_workflow, execute_activity


Q_SELENIUM_NAME = "q-browsers-selenium"
Q_SELENIUM_RETRY =     retry_policy=RetryPolicy(
        backoff_coefficient=3.0,
        maximum_attempts=3,
        initial_interval=timedelta(seconds=1),
        maximum_interval=timedelta(seconds=9),
        non_retryable_error_types=["AssertionError", "TypeError"],
    )
Q_SELENIUM_TIMEOUT = timedelta(seconds=SELENIUM_PAGE_LOAD_TIMEOUT * 10)
Q_PROCESS_HTML_NAME = "q-browsers-process-html"

@workflow.defn
class DownloadWorkflow:
    @staticmethod
    def make_id(url):
        return TASK_VERSION+"__download_v1__"+url
    
    @workflow.run
    async def run(self, url):
        from .tasks.download_html import selenium_render_page_to_html
        return await execute_activity(
            selenium_render_page_to_html,
            url,
            task_queue=Q_SELENIUM_NAME,
            retry_policy=Q_SELENIUM_RETRY,
            start_to_close_timeout=Q_SELENIUM_TIMEOUT
        )


@workflow.defn
class ExtractMarkdownWorkflow:
    @staticmethod
    def make_id(url):
        return TASK_VERSION+"__markdown_v1__"+url
    
    @workflow.run
    async def run(self, url):
        from .tasks.html_to_markdown import extract_markdown_from_html
        return await execute_activity(
            extract_markdown_from_html,
            url,
            task_queue=Q_PROCESS_HTML_NAME,
        )
    

@workflow.defn
class ScrapeWorkflow:
    @staticmethod
    def make_id(url, *_a):
        return TASK_VERSION+"__scrape_v1__"+url
    
    @workflow.run
    async def run(self, url, scrape_options, depth):
        from .tasks.html_extract_links import extract_links_from_url
        url = scrape_options["url"]
        await execute_child_workflow(
            DownloadWorkflow,
            url,
            task_queue=Q_SELENIUM_NAME,
        )

        await execute_child_workflow(
            ExtractMarkdownWorkflow,
            url,
            task_queue=Q_PROCESS_HTML_NAME,
        )

        child_counts = 1
        if depth >= scrape_options["max_depth"]:
            workflow.logger.info("stopping because of max depth: %s/%s", depth, scrape_options['max_depth'])
            return child_counts
        
        urls = await execute_activity(
            extract_links_from_url,
            url,
            scrape_options,
            task_queue=Q_PROCESS_HTML_NAME,
        )
        workflow.logger.info("scraper extracted: %s urls", len(urls))
        
        child_counts += sum(await asyncio.gather(*[
                execute_child_workflow(ScrapeWorkflow, next_url, scrape_options, depth+1,task_queue=Q_PROCESS_HTML_NAME,)
                for next_url in urls
        ]))

        workflow.logger.info("scraper found total: %s children", child_counts)

        return child_counts


async def run_scrape(url, scrape_options):
    return await execute_workflow(ScrapeWorkflow, url, scrape_options, 1,
            task_queue=Q_PROCESS_HTML_NAME,)