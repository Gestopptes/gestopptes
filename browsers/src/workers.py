
import multiprocessing
from concurrent.futures import ProcessPoolExecutor
from temporalio.worker import SharedStateManager, Worker
from temporalio.client import Client


async def browser_worker():
    from .config import Q_BROWSERS, Q_BROWSERS_PROCESS_COUNT, TEMPORAIO_URL
    from .tasks import ALL_ACTIVITIES
    from .workflows import ALL_WORKFLOWS
    
    client = await Client.connect(TEMPORAIO_URL)

    return Worker(
        client,
        task_queue=Q_BROWSERS,
        workflows=ALL_WORKFLOWS,
        activities=ALL_ACTIVITIES,
        activity_executor=ProcessPoolExecutor(Q_BROWSERS_PROCESS_COUNT),
        max_concurrent_activities=Q_BROWSERS_PROCESS_COUNT,
        shared_state_manager=SharedStateManager.create_from_multiprocessing(
            multiprocessing.Manager()
        ),
    )


# def cpu_worker(client):    
#     from .config import Q_CPU_PROCESSING, Q_CPU_PROCESS_COUNT
#     from .tasks import ALL_ACTIVITIES
#     from .workflows import ALL_WORKFLOWS

#     return Worker(
#         client,
#         task_queue=Q_CPU_PROCESSING,
#         workflows=ALL_WORKFLOWS,
#         activities=ALL_ACTIVITIES,
#         activity_executor=ProcessPoolExecutor(Q_CPU_PROCESS_COUNT),
#         max_concurrent_activities=Q_CPU_PROCESS_COUNT,
#         shared_state_manager=SharedStateManager.create_from_multiprocessing(
#             multiprocessing.Manager()
#         ),
#     )