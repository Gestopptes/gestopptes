from temporalio import  workflow
from datetime import timedelta
import asyncio
from temporalio.common import RetryPolicy, WorkflowIDReusePolicy #, WorkflowIDConflictPolicy  # master branch only
from temporalio.workflow import ParentClosePolicy
from temporalio.exceptions import WorkflowAlreadyStartedError
from temporalio.client import Client

from ..config import Q_BROWSERS, ACTIVITY_TIMEOUT, TEMPORAIO_URL

ACTIVITY_OPT = dict(
    task_queue=Q_BROWSERS,
    start_to_close_timeout=timedelta(seconds=ACTIVITY_TIMEOUT),
    # heartbeat_timeout=timedelta(seconds=16),
    retry_policy=RetryPolicy(
        backoff_coefficient=3.0,
        maximum_attempts=3,
        initial_interval=timedelta(seconds=ACTIVITY_TIMEOUT/9),
        maximum_interval=timedelta(seconds=ACTIVITY_TIMEOUT),
        non_retryable_error_types=["AssertionError", "TypeError"],
    )
)

CHILD_WORKFLOW_OPT = dict(
    parent_close_policy=ParentClosePolicy.ABANDON,
    id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE,
    # id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,  # master branch only + execute_workflow onyl
    task_queue=Q_BROWSERS,
)

WORKFLOW_OPT = dict(
    id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE,
    # id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,  # master branch only
    task_queue=Q_BROWSERS,
)


async def execute_child_workflow(the_wf, *args):
    the_id = the_wf.make_id(*args)
    assert the_id is not None, f'bad id for wf {the_wf}: {the_id}'
    try:
        return await workflow.execute_child_workflow(
            the_wf.run,
            args=args,
            id=the_id,
            **CHILD_WORKFLOW_OPT
        )
    except WorkflowAlreadyStartedError:
        handle = await workflow.get_external_workflow_handle(the_id)
        return await handle.result()



async def execute_workflow(the_wf, *args):
    client = await Client.connect(TEMPORAIO_URL)
    the_id = the_wf.make_id(*args)
    assert the_id is not None, f'bad id for wf {the_wf}: {the_id}'
    try:
        handle = await client.start_workflow(
            the_wf.run,
            args=args,

            id=the_id,
            **WORKFLOW_OPT,
        )
        return await handle.result()
    except WorkflowAlreadyStartedError:
        handle = client.get_workflow_handle(the_id)
        return await handle.result()


async def execute_activity(the_act, *args):
    return await workflow.execute_activity(
        the_act,
        args=args,
        **ACTIVITY_OPT
    )