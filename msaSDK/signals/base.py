from typing import Any, Callable, Dict, List

from starlette.background import BackgroundTask
from starlette.requests import Request

from .handler import MSASignalHandler, MSATaskHandler

signal = MSASignalHandler()
task = MSATaskHandler()


async def initiate_signal(
    request: Request, name: str, **kwargs: Dict[str, Any]
) -> None:
    """
    Will fire the signal. Can also be a coroutine. Long running
    background tasks will be terminated by host.

    NB: Only one signal per function, need request object

    Args:
        request (Request): Do not remove request object
        name (str): Handler name without spaces
    """
    task = BackgroundTask(signal.handlers().get(name), **kwargs)
    request.state.background = task


async def initiate_task(obj: Callable, *args: List[Any], **kwargs: Dict[str, Any]):
    """
    Initiate task is different from initiate signal.
    Any number of tasks can be fired within a single function.
    Also, no request object is required for task.

    Args:
        obj: function object (Callable)
        args: function arguments
        kwargs: function arguments
    """
    return await task.add_task(obj, *args, **kwargs)
