# -*- coding: utf-8 -*-
import time
import codecs
from typing import Optional, Dict

from pyinstrument import Profiler

from starlette.routing import Router
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class MSAProfilerMiddleware:
    """ PyInstrument Profiler as Middleware

        Used to create a HTML from the Profiler result if enabled in the MSAServiceDefinition instance.

        Args:
            msa_app: Optional[Router] = None, Instance of the MSAApp
            profiler_interval: float = 0.0001,
            profiler_output_type: str = "html", ``text`` or ``html``should be html if Admin Site Profiler Page should be used.
            track_each_request: bool = True, Tracks each single request and profiles it immediatly, if off then profiler creates result while shutdwon event.
            **profiler_kwargs: other pyinstrument args like 'html_file_name'
    """
    def __init__(
        self, app: ASGIApp,
        *,
        msa_app: Optional[Router] = None,
        profiler_interval: float = 0.0001,
        profiler_output_type: str = "html",
        track_each_request: bool = True,
        **profiler_kwargs: Dict
    ):
        self.app = app
        """Linked/Mounted MSAApp Instance"""
        self._profiler = Profiler(interval=profiler_interval)

        self._server_app = msa_app
        self._output_type = profiler_output_type
        self._profiler_kwargs: dict = profiler_kwargs
        self._handler_init_done: bool = False
        self._htmlfile_init_done: bool = False
        self._track_each_request: bool = track_each_request

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """register an event handler for profiler stop"""
        if self._server_app is not None and not self._handler_init_done:
            self._handler_init_done = True
            self._server_app.add_event_handler("shutdown", self.get_profiler_result)

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        self._profiler.start()

        request = Request(scope, receive=receive)

        # Default status code
        status_code = 500

        async def wrapped_send(message: Message) -> None:
            if message['type'] == 'http.response.start':
                nonlocal status_code
                status_code = message['status']
            await send(message)

        try:
            await self.app(scope, receive, wrapped_send)
        finally:
            if scope["type"] == "http":
                self._profiler.stop()
                end = time.perf_counter()
                if self._output_type == "html" and not self._htmlfile_init_done:
                    await self.get_profiler_result()
                elif self._track_each_request:
                    await self.get_profiler_result()

    async def get_profiler_result(self):
        """ Produces the profiler result in the defined output type format, ``text`` or ``html``"""
        if self._output_type == "text":
            print(self._profiler.output_text(**self._profiler_kwargs))
        elif self._output_type == "html":
            html_name = self._profiler_kwargs.get("html_file_name")
            if html_name is None:
                html_name = "./msatemplates/profiler.html"
            html_code = self._profiler.output_html(**self._profiler_kwargs) # HTMLRenderer().render(session=self._profiler.last_session)
            html_code = html_code.replace("pyinstrument", "msaSDK Profiler").replace("Pyinstrument", "msaSDK Profiler")
            with codecs.open(html_name, "w", "utf-8") as f:
                f.write(html_code)
