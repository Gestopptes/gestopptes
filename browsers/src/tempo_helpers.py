from temporalio import  workflow
from datetime import timedelta
import asyncio
from temporalio.common import RetryPolicy, WorkflowIDReusePolicy #, WorkflowIDConflictPolicy  # master branch only
from temporalio.workflow import ParentClosePolicy
from temporalio.exceptions import WorkflowAlreadyStartedError
from temporalio.client import Client

from .config import DEFAULT_TASK_Q, DEFAULT_ACTIVITY_TIMEOUT, TEMPORAIO_URL

ACTIVITY_OPT = dict(
    task_queue=DEFAULT_TASK_Q,
    start_to_close_timeout=timedelta(seconds=DEFAULT_ACTIVITY_TIMEOUT),
    # heartbeat_timeout=timedelta(seconds=16),
    retry_policy=RetryPolicy(
        backoff_coefficient=3.0,
        maximum_attempts=1,
        initial_interval=timedelta(seconds=DEFAULT_ACTIVITY_TIMEOUT/9),
        maximum_interval=timedelta(seconds=DEFAULT_ACTIVITY_TIMEOUT),
        non_retryable_error_types=["AssertionError", "TypeError"],
    )
)

CHILD_WORKFLOW_OPT = dict(
    parent_close_policy=ParentClosePolicy.ABANDON,
    id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
    # id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,  # master branch only + execute_workflow onyl
    task_queue=DEFAULT_TASK_Q,
)

WORKFLOW_OPT = dict(
    id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE_FAILED_ONLY,
    # id_conflict_policy=WorkflowIDConflictPolicy.USE_EXISTING,  # master branch only
    task_queue=DEFAULT_TASK_Q,
)


async def execute_child_workflow(the_wf, *args, **kw):
    the_id = the_wf.make_id(*args)
    assert the_id is not None, f'bad id for wf {the_wf}: {the_id}'
    opt = dict(CHILD_WORKFLOW_OPT)
    opt.update(kw)
    try:
        return await workflow.execute_child_workflow(
            the_wf.run,
            args=args,
            id=the_id,
            **opt
        )
    except WorkflowAlreadyStartedError:
        handle = await workflow.get_external_workflow_handle(the_id)
        return await handle.result()



async def execute_workflow(the_wf, *args, **kw):
    client = await Client.connect(TEMPORAIO_URL)
    the_id = the_wf.make_id(*args)
    assert the_id is not None, f'bad id for wf {the_wf}: {the_id}'
    opt = dict(WORKFLOW_OPT)
    opt.update(kw)
    try:
        handle = await client.start_workflow(
            the_wf.run,
            args=args,

            id=the_id,
            **opt,
        )
        return await handle.result()
    except WorkflowAlreadyStartedError:
        handle = client.get_workflow_handle(the_id)
        return await handle.result()


async def execute_activity(the_act, *args, **kw):
    opt = dict(ACTIVITY_OPT)
    opt.update(kw)
    return await workflow.execute_activity(
        the_act,
        args=args,
        **opt
    )



######################### AUTO HEARTBEATER ########################
# https://github.com/temporalio/samples-python/blob/main/custom_decorator/activity_utils.py
from datetime import datetime
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, cast
from temporalio import activity

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def auto_heartbeater(fn: F) -> F:
    # We want to ensure that the type hints from the original callable are
    # available via our wrapper, so we use the functools wraps decorator
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        heartbeat_timeout = activity.info().heartbeat_timeout
        heartbeat_task = None
        if heartbeat_timeout:
            # Heartbeat twice as often as the timeout
            heartbeat_task = asyncio.create_task(
                heartbeat_every(heartbeat_timeout.total_seconds() / 2)
            )
        try:
            return await fn(*args, **kwargs)
        finally:
            if heartbeat_task:
                heartbeat_task.cancel()
                # Wait for heartbeat cancellation to complete
                await asyncio.wait([heartbeat_task])

    return cast(F, wrapper)


async def heartbeat_every(delay: float, *details: Any) -> None:
    # Heartbeat every so often while not cancelled
    while True:
        await asyncio.sleep(delay)
        print(f"Heartbeating at {datetime.now()}")
        activity.heartbeat(*details)