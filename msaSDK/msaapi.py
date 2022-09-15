# -*- coding: utf-8 -*-

import asyncio
import inspect
import json
import os
import sys
import traceback
import typing
import uuid
from typing import Optional, List, Dict, Any, Union, Sequence, Type, Callable, Coroutine

from fastapi import FastAPI, routing
from fastapi.datastructures import Default
from fastapi.params import Depends
from fastapi.utils import generate_unique_id
from jpcore.component import Component
from jpcore.justpy_app import templates, template_options, cookie_signer, JustpyAjaxEndpoint
from jpcore.justpy_config import COOKIE_MAX_AGE, CRASH, STATIC_ROUTE, \
    STATIC_DIRECTORY, STATIC_NAME, MEMORY_DEBUG
from jpcore.justpy_config import FAVICON, LATENCY
from jpcore.justpy_config import SESSION_COOKIE_NAME, SESSIONS
from jpcore.template import Context
from jpcore.webpage import WebPage
from justpy.htmlcomponents import JustpyBaseComponent
from starlette.endpoints import WebSocketEndpoint
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse, Response, JSONResponse
from starlette.routing import Route, BaseRoute


class MSAFastAPI(FastAPI):
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
        self.STATIC_ROUTE = STATIC_ROUTE
        self.STATIC_DIRECTORY = STATIC_DIRECTORY
        self.STATIC_NAME = STATIC_NAME
        self.WebPage = WebPage
        self.ui_current_module = sys.modules["justpy.justpy"]
        self.ui_current_dir = os.path.dirname(self.ui_current_module.__file__)

        super().__init__(debug=debug, routes=routes, title=title, description=description, version=version,
                         openapi_url=openapi_url, openapi_tags=openapi_tags, servers=servers, dependencies=dependencies,
                         default_response_class=default_response_class, docs_url=docs_url, redoc_url=redoc_url,
                         swagger_ui_oauth2_redirect_url=swagger_ui_oauth2_redirect_url,
                         swagger_ui_init_oauth=swagger_ui_init_oauth, middleware=middleware,
                         exception_handlers=exception_handlers, on_startup=on_startup, on_shutdown=on_shutdown,
                         terms_of_service=terms_of_service, contact=contact, license_info=license_info,
                         openapi_prefix=openapi_prefix, root_path=root_path, root_path_in_servers=root_path_in_servers,
                         responses=responses, callbacks=callbacks, deprecated=deprecated,
                         include_in_schema=include_in_schema, swagger_ui_parameters=swagger_ui_parameters,
                         generate_unique_id_function=generate_unique_id_function, **extra)

    def route_as_text(self, route):
        # print("route_as_text")
        """
        get a string representation of the given route
        """
        text = f"{route.__class__.__name__}(name: {route.name}, path: {route.path}, format: {route.path_format},  regex: {route.path_regex})"
        if isinstance(route, Route):
            text += f"func: {route.endpoint.__name__}"
        return text

    def add_jproute(self, path: str, wpfunc: typing.Callable, name: str = None):
        # print("add_jproute")
        """
        add a route for the given Webpage returning func

        Args:
            path(str): the path to use as route
            wpfunc(typing.Callable): a Webpage returning func
            name(str): the name of the route
        """
        endpoint = self.response(wpfunc)
        if name is None:
            name = wpfunc.__name__
        self.router.add_route(path, endpoint, name=name, include_in_schema=False)

    def jproute(self,
                path: str,
                name: typing.Optional[str] = None) -> typing.Callable:  # pragma: nocover
        # print("jproute")
        """
        justpy route decorator

        function will we "wrapped" as a response and a route added

        Args:
            func(typing.Callable): the function to convert to a reponse
        """

        def routeResponse(func: typing.Callable) -> typing.Callable:
            # print("routeResponse")
            """
            decorator for the given func

            Args:
                func(typing.Callable)

            Returns:
                Callable: an endpoint that has been routed

            """
            endpoint = self.response(func)
            self.router.add_route(
                path,
                endpoint,
                name=name if name is not None else func.__name__,
                include_in_schema=False,
            )
            self.route(path)
            return endpoint

        return routeResponse

    def response(self, func: typing.Callable):
        # print("response")
        """
        response decorator converts a function to a response

        see also https://github.com/justpy-org/justpy/issues/532
        castAsEndPoint

        Args:
            func(typing.Callable): the function (returning a WebPage) to convert to a response
        """

        async def funcResponse(request) -> HTMLResponse:
            # print("funcResponse")
            """
            decorator function to apply the function to the request and
            return it as a response

            Args:
                request(Request): the request to apply the function to

            Returns:
                Response: a HTMLResponse applying the justpy infrastructure

            """
            new_cookie = self.handle_session_cookie(request)
            wp = await self.get_page_for_func(request, func)
            response = self.get_response_for_load_page(request, wp)
            response = self.set_cookie(request, response, wp, new_cookie)
            if LATENCY:
                await asyncio.sleep(LATENCY / 1000)
            return response

        # return the decorated function, thus allowing access to the func
        # parameter in the funcResponse later when applied
        return funcResponse

    async def get_page_for_func(self, request, func: typing.Callable) -> WebPage:
        # print("get_page_for_func")
        """
        get the Webpage for the given func

        Args:
            request: the request to pass to the given function
            func: the function

        Returns:
            WebPage: the Webpage returned by the given function
        """
        # @TODO - get rid of the global func_to_run concept that isn't
        # in scope here (anymore) anyways
        func_to_run = func
        func_parameters = len(inspect.signature(func_to_run).parameters)
        assert (func_parameters < 2), f"Function {func_to_run.__name__} cannot have more than one parameter"
        if inspect.iscoroutinefunction(func_to_run):
            if func_parameters == 1:
                load_page = await func_to_run(request)
            else:
                load_page = await func_to_run()
        else:
            if func_parameters == 1:
                load_page = func_to_run(request)
            else:
                load_page = func_to_run()
        return load_page

    def get_response_for_load_page(self, request, load_page):
        # print("get_response_for_load_page")
        """
        get the response for the given webpage

        Args:
            request(Request): the request to handle
            load_page(WebPage): the webpage to wrap with justpy and
            return as a full HtmlResponse

        Returns:
            Reponse: the response for the given load_page
        """
        page_type = type(load_page)
        assert issubclass(
            page_type, WebPage
        ), f"Function did not return a web page but a {page_type.__name__}"
        if len(load_page) == 0 and not load_page.html:
            error_html = """<span style="color:red">Web page is empty - you might want to add components</span>"""
            return HTMLResponse(error_html, 500)
        page_options = {
            "reload_interval": load_page.reload_interval,
            "body_style": load_page.body_style,
            "body_classes": load_page.body_classes,
            "css": load_page.css,
            "head_html": load_page.head_html,
            "body_html": load_page.body_html,
            "display_url": load_page.display_url,
            "dark": load_page.dark,
            "title": load_page.title,
            "redirect": load_page.redirect,
            "highcharts_theme": load_page.highcharts_theme,
            "debug": load_page.debug,
            "events": load_page.events,
            "favicon": load_page.favicon if load_page.favicon else FAVICON,
        }
        if load_page.use_cache:
            page_dict = load_page.cache
        else:
            page_dict = load_page.build_list()
        template_options["tailwind"] = load_page.tailwind
        context = {
            "request": request,
            "page_id": load_page.page_id,
            "justpy_dict": json.dumps(page_dict, default=str),
            "use_websockets": json.dumps(WebPage.use_websockets),
            "options": template_options,
            "page_options": page_options,
            "html": load_page.html,
        }
        # wrap the context in a context object to make it available
        context_obj = Context(context)
        context["context_obj"] = context_obj
        response = templates.TemplateResponse(load_page.template_file, context)
        return response

    def handle_session_cookie(self, request) -> typing.Union[bool, Response]:
        # print("handle_session_cookie")
        """
        handle the session cookie for this request

        Returns:
            True if a new cookie and session has been created
        """
        # Handle web requests
        session_cookie = request.cookies.get(SESSION_COOKIE_NAME)
        new_cookie = None
        if SESSIONS:
            new_cookie = False
            if session_cookie:
                try:
                    session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                except:
                    return PlainTextResponse("Bad Session")
                request.state.session_id = session_id
                request.session_id = session_id
            else:
                # Create new session_id
                request.state.session_id = str(uuid.uuid4().hex)
                request.session_id = request.state.session_id
                new_cookie = True

        return new_cookie

    def set_cookie(self, request, response, load_page, new_cookie: typing.Union[bool, Response]):
        # print("set_cookie")
        """
        set the cookie_value

        Args:
            request: the request
            response: the response to be sent
            load_page(WebPage): the WebPage to handle
            new_cookie(bool|Response): True if there is a new cookie. Or Response if cookie was invalid
        """
        if isinstance(new_cookie, Response):
            return new_cookie
        if SESSIONS and new_cookie:
            cookie_value = cookie_signer.sign(request.state.session_id)
            cookie_value = cookie_value.decode("utf-8")
            response.set_cookie(
                SESSION_COOKIE_NAME, cookie_value, max_age=COOKIE_MAX_AGE, httponly=True
            )
            for k, v in load_page.cookies.items():
                response.set_cookie(k, v, max_age=COOKIE_MAX_AGE, httponly=True)
        return response


async def handle_event(data_dict, com_type=0, page_event=False):
    # com_type 0: websocket, con_type 1: ajax
    connection_type = {0: "websocket", 1: "ajax"}

    event_data = data_dict["event_data"]
    try:
        p = WebPage.instances[event_data["page_id"]]
    except:
        return
    event_data["page"] = p
    if com_type == 0:
        event_data["websocket"] = WebPage.sockets[event_data["page_id"]][
            event_data["websocket_id"]
        ]
    # The page_update event is generated by the reload_interval Ajax call
    if event_data["event_type"] == "page_update":
        build_list = p.build_list()
        return {"type": "page_update", "data": build_list}

    if page_event:
        c = p
    else:
        component_id = event_data["id"]
        c = Component.instances.get(component_id, None)
        if c is not None:
            event_data["target"] = c


    try:
        if c is not None:
            before_result = await c.run_event_function("before", event_data, True)
    except:
        pass
    try:
        if c is not None:
            if hasattr(c, "on_" + event_data["event_type"]):
                event_result = await c.run_event_function(
                    event_data["event_type"], event_data, True
                )
            else:
                event_result = None

        else:
            event_result = None

    except Exception as e:
        # raise Exception(e)
        if CRASH:
            print(traceback.format_exc())
            sys.exit(1)
        event_result = None


    # If page is not to be updated, the event_function should return anything but None
    if event_result is None:
        if com_type == 0:  # WebSockets communication
            if LATENCY:
                await asyncio.sleep(LATENCY / 1000)
            await p.update()
        elif com_type == 1:  # Ajax communication
            build_list = p.build_list()
    try:
        if c is not None:
            after_result = await c.run_event_function("after", event_data, True)
    except:
        pass
    if com_type == 1 and event_result is None:
        dict_to_send = {
            "type": "page_update",
            "data": build_list,
            "page_options": {
                "display_url": p.display_url,
                "title": p.title,
                "redirect": p.redirect,
                "open": p.open,
                "favicon": p.favicon,
            },
        }
        return dict_to_send

