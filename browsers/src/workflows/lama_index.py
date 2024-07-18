from temporalio import  workflow
import asyncio
from ..config import SCRAPE_TASK_VERSION
from ._helpers import execute_child_workflow, execute_workflow, execute_activity


@workflow.defn
class LamaIndexDemoWorkflow:
    @staticmethod
    def make_id(url):
        return SCRAPE_TASK_VERSION+"__lama_demo_v2__"+url
    
    @workflow.run
    async def run(self, url):
        from ..tasks import lama_index_demo
        return await execute_activity(
            lama_index_demo,
            url,
        )



async def execute_lama(url):
    return await execute_workflow(LamaIndexDemoWorkflow, url)