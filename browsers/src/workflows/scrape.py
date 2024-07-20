from temporalio import  workflow
import asyncio
from ..config import SCRAPE_TASK_VERSION
from ._helpers import execute_child_workflow, execute_workflow, execute_activity


@workflow.defn
class DownloadWorkflow:
    @staticmethod
    def make_id(url):
        return SCRAPE_TASK_VERSION+"__download_v1__"+url
    
    @workflow.run
    async def run(self, url):
        from ..tasks import render_page_to_html
        return await execute_activity(
            render_page_to_html,
            url,
        )


@workflow.defn
class ExtractMarkdownWorkflow:
    @staticmethod
    def make_id(url):
        return SCRAPE_TASK_VERSION+"__markdown_v1__"+url
    
    @workflow.run
    async def run(self, url):
        from ..tasks import extract_markdown_from_html
        return await execute_activity(
            extract_markdown_from_html,
            url,
        )



@workflow.defn
class ScrapeWorkflow:
    @staticmethod
    def make_id(url, *_a):
        return SCRAPE_TASK_VERSION+"__scrape_v1__"+url
    
    @workflow.run
    async def run(self, url, scrape_options, depth):
        from ..tasks import extract_links_from_url
        from ..workflows.lama_index import LamaIndexDemoWorkflow
        url = scrape_options["url"]
        await execute_child_workflow(
            DownloadWorkflow,
            url
        )

        await execute_child_workflow(
            ExtractMarkdownWorkflow,
            url
        )

        child_counts = 1
        if depth >= scrape_options["max_depth"]:
            return child_counts
        
        urls = await execute_activity(
            extract_links_from_url,
            url,
            scrape_options,
        )
        
        child_counts += sum(await asyncio.gather(*[
                execute_child_workflow(ScrapeWorkflow, next_url, scrape_options, depth+1)
                for next_url in urls
        ]))

        return child_counts


async def execute_scrape(url, scrape_options):
    return await execute_workflow(ScrapeWorkflow, url, scrape_options, 1)