from temporalio import  workflow
import asyncio
from ..config import TASK_VERSION
from ..tempo_helpers import execute_child_workflow, execute_workflow, execute_activity

from datetime import timedelta

Q_GPU_NAME = "q-gpu"
Q_GPU_TIMEOUT = timedelta(seconds=3600)

@workflow.defn
class LamaIndexNeo4jWorkflow:
    @staticmethod
    def make_id(url, options):
        return TASK_VERSION+"__llama_index_neo4j_v2__"+url
    
    @workflow.run
    async def run(self, url, options):
        from .tasks import lama_index_url2neo4j_property_graph_index
        return await execute_activity(
            lama_index_url2neo4j_property_graph_index,
            url,
            options,
            task_queue=Q_GPU_NAME,
            start_to_close_timeout=Q_GPU_TIMEOUT,
            heartbeat_timeout=timedelta(seconds=5),
        )


@workflow.defn
class LamaIndexVectorsWorkflow:
    @staticmethod
    def make_id(url, options):
        return TASK_VERSION+"__llama_index_vectors_v2__"+url
    
    @workflow.run
    async def run(self, url, options):
        from .tasks import lama_index_url2neo4j_vector_index
        return await execute_activity(
            lama_index_url2neo4j_vector_index,
            url,
            options,
            task_queue=Q_GPU_NAME,
            start_to_close_timeout=Q_GPU_TIMEOUT,
            heartbeat_timeout=timedelta(seconds=5),
        )


@workflow.defn
class LamaIndexAllWorkflow:
    @staticmethod
    def make_id(url, options):
        return TASK_VERSION+"__llama_index_all_v2__"+url
    
    @workflow.run
    async def run(self, url, options):
        return await asyncio.gather(
            execute_child_workflow(
                LamaIndexNeo4jWorkflow,
                url,
                options,
                task_queue=Q_GPU_NAME,
            ),
            execute_child_workflow(
                LamaIndexVectorsWorkflow,
                url,
                options,
                task_queue=Q_GPU_NAME,
            )
        )


async def execute_lama(url, options):
    return await execute_workflow(LamaIndexAllWorkflow, url, options,
            task_queue=Q_GPU_NAME,)