import logging
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from temporalio.worker import SharedStateManager, Worker
from temporalio.client import Client

log = logging.getLogger(__name__)

async def worker_gpu():
    from ..config import TEMPORAIO_URL, GPU_COUNT
    from .workflows import Q_GPU_NAME
    from .tasks import lama_index_url2neo4j_property_graph_index, lama_index_url2neo4j_vector_index
    from .workflows import LamaIndexVectorsWorkflow, LamaIndexAllWorkflow, LamaIndexNeo4jWorkflow

    client = await Client.connect(TEMPORAIO_URL)
    log.info("building gpu worker...")

    return Worker(
        client,
        task_queue=Q_GPU_NAME,
        workflows=[
            LamaIndexVectorsWorkflow, LamaIndexAllWorkflow, LamaIndexNeo4jWorkflow,
        ],
        activities=[
             lama_index_url2neo4j_property_graph_index, lama_index_url2neo4j_vector_index,
        ],
        activity_executor=ProcessPoolExecutor(GPU_COUNT),
        max_concurrent_activities=GPU_COUNT,
        max_concurrent_workflow_tasks=100,
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
    )