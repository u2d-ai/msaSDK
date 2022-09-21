import asyncio
import functools
from functools import wraps

queue = asyncio.Queue()


class MSASignalHandler:

    """
    Decorator on call collects all handlers on start of server.
    All handlers are collected to registry.
    """

    def __init__(self):
        self._registry = {}

    def handlers(self):
        """
        Will return all the handlers. Helper for _registry.
        """
        return self._registry

    def register(self, _func=None):
        """
        Decorator to register the handler.
        Handler must be asynchronous.
        """

        def _wrap(func):
            if asyncio.iscoroutinefunction(func):
                self._register_handler(func)
            else:
                raise Exception("Signal handler must be async")

            @wraps(func)
            def _wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrapper

        if _func is None:
            return _wrap
        else:
            return _wrap(func=_func)

    def _register_handler(self, func):

        if func.__name__ not in self._registry:
            self._registry[func.__name__] = func


class MSATaskHandler:

    """
    Unlike signal handler, task handler gives users the freedom to write
    any function, call any number of times from the endpoint function.
    Handled with queues.
    """

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()

    async def handler(self):
        """Call add_task method to append new task to the queue
        Intended to run during every request.
        """
        producers = asyncio.create_task(self.add_task())
        self.loop.create_task(self.runner())
        await self.loop.gather(producers)
        await queue.join()

    async def add_task(self, function_object=None, *args, **kwargs):
        """
        Only valid objects are appended to the queue.
        Add task with function_object and arguments"""
        if function_object:
            obj = functools.partial(function_object, *args, **kwargs)
            await queue.put(obj)

    async def runner(self, *args, **kwargs):
        """Open loop to execute every queue updates"""
        await asyncio.sleep(1)
        while True:
            await asyncio.sleep(1)
            function_object = await queue.get()
            await function_object(*args, **kwargs)
            queue.task_done()
