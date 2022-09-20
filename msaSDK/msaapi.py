# -*- coding: utf-8 -*-
import asyncio
import importlib
import os
from typing import Optional, List, Dict, Any, Union, Sequence, Type, Callable, Coroutine

from fastapi import FastAPI, routing
from fastapi.datastructures import Default
from fastapi.params import Depends
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.routing import BaseRoute
from starlette.staticfiles import StaticFiles

from msaSDK.jpui.jpcore.justpy_app import JustpyApp
from msaSDK.jpui.jpcore.webpage import WebPage
from msaSDK.jpui.justpy.justpy import AjaxEndpoint, JustpyEvents


class MSAFastAPI(FastAPI, JustpyApp):
    """
    a MSAFastAPI application is a special FastAPI application
    It includes justpy UI routing
    """

    def __init__(self, *, debug: bool = False, routes: Optional[List[BaseRoute]] = None, title: str = "FastAPI",
                 description: str = "", version: str = "0.1.0", openapi_url: Optional[str] = "/openapi.json",
                 openapi_tags: Optional[List[Dict[str, Any]]] = None,
                 servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
                 dependencies: Optional[Sequence[Depends]] = None,
                 default_response_class: Type[Response] = Default(JSONResponse), docs_url: Optional[str] = "/docs",
                 redoc_url: Optional[str] = "/redoc",
                 swagger_ui_oauth2_redirect_url: Optional[str] = "/docs/oauth2-redirect",
                 swagger_ui_init_oauth: Optional[Dict[str, Any]] = None,
                 middleware: Optional[Sequence[Middleware]] = None, exception_handlers: Optional[
                Dict[
                    Union[int, Type[Exception]],
                    Callable[[Request, Any], Coroutine[Any, Any, Response]],
                ]
            ] = None, on_startup: Optional[Sequence[Callable[[], Any]]] = None,
                 on_shutdown: Optional[Sequence[Callable[[], Any]]] = None, terms_of_service: Optional[str] = None,
                 contact: Optional[Dict[str, Union[str, Any]]] = None,
                 license_info: Optional[Dict[str, Union[str, Any]]] = None, openapi_prefix: str = "",
                 root_path: str = "", root_path_in_servers: bool = True,
                 responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
                 callbacks: Optional[List[BaseRoute]] = None, deprecated: Optional[bool] = None,
                 include_in_schema: bool = True, swagger_ui_parameters: Optional[Dict[str, Any]] = None,
                 generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                     generate_unique_id
                 ), **extra: Any) -> None:

        self.UI_STATIC_ROUTE = "/static"
        self.UI_STATIC_NAME = "static"
        self.WebPage = WebPage
        self.jpui_current_dir = "jpui/justpy"
        self.jpui_ajax_url: str = "/zzz_justpy_ajax"
        self.jpui_websocket_url: str = "/"

        super().__init__(debug=debug, routes=routes, title=title, description=description, version=version,
                         openapi_url=openapi_url, openapi_tags=openapi_tags, servers=servers,
                         dependencies=dependencies,
                         default_response_class=default_response_class, docs_url=docs_url, redoc_url=redoc_url,
                         swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
                         swagger_ui_init_oauth=swagger_ui_init_oauth, middleware=middleware,
                         exception_handlers=exception_handlers, on_startup=on_startup, on_shutdown=on_shutdown,
                         terms_of_service=terms_of_service, contact=contact, license_info=license_info,
                         openapi_prefix=openapi_prefix, root_path=root_path,
                         root_path_in_servers=root_path_in_servers,
                         responses=responses, callbacks=callbacks, deprecated=deprecated,
                         include_in_schema=include_in_schema, swagger_ui_parameters=swagger_ui_parameters,
                         generate_unique_id_function=generate_unique_id_function, **extra)

    def mount_jp_internal_routes(self):

        self.WebPage.loop = asyncio.get_event_loop()
        self.mount(self.UI_STATIC_ROUTE, StaticFiles(directory=self.jpui_current_dir + "/templates"),
                   name=self.UI_STATIC_NAME)
        self.mount(
            "/templates", StaticFiles(directory=self.jpui_current_dir + "/templates"), name="templates"
        )

        self.add_route("/zzz_justpy_ajax", AjaxEndpoint)
        self.add_websocket_route("/", JustpyEvents)


