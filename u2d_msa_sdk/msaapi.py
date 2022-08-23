from enum import Enum
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Sequence,
    Type,
    Union,
)

from fastapi import FastAPI
from fastapi import routing
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.encoders import DictIntStrAny, SetIntStr
from fastapi.params import Depends
from fastapi.types import DecoratedCallable
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Receive, Scope, Send


class MSAFastAPI(FastAPI):

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

    def build_middleware_stack(self) -> ASGIApp:
        return super().build_middleware_stack()

    def openapi(self) -> Dict[str, Any]:
        return super().openapi()

    def setup(self) -> None:
        super().setup()

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        return await super().__call__(scope, receive, send)

    def add_api_route(self, path: str, endpoint: Callable[..., Coroutine[Any, Any, Response]], *,
                      response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
                      tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
                      summary: Optional[str] = None, description: Optional[str] = None,
                      response_description: str = "Successful Response",
                      responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
                      deprecated: Optional[bool] = None, methods: Optional[List[str]] = None,
                      operation_id: Optional[str] = None,
                      response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                      response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                      response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
                      response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
                      include_in_schema: bool = True,
                      response_class: Union[Type[Response], DefaultPlaceholder] = Default(
                          JSONResponse
                      ), name: Optional[str] = None, openapi_extra: Optional[Dict[str, Any]] = None,
                      generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                          generate_unique_id
                      )) -> None:
        super().add_api_route(path, endpoint, response_model=response_model, status_code=status_code, tags=tags,
                              dependencies=dependencies, summary=summary, description=description,
                              response_description=response_description, responses=responses, deprecated=deprecated,
                              methods=methods, operation_id=operation_id, response_model_include=response_model_include,
                              response_model_exclude=response_model_exclude,
                              response_model_by_alias=response_model_by_alias,
                              response_model_exclude_unset=response_model_exclude_unset,
                              response_model_exclude_defaults=response_model_exclude_defaults,
                              response_model_exclude_none=response_model_exclude_none,
                              include_in_schema=include_in_schema, response_class=response_class, name=name,
                              openapi_extra=openapi_extra, generate_unique_id_function=generate_unique_id_function)

    def api_route(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
                  tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
                  summary: Optional[str] = None, description: Optional[str] = None,
                  response_description: str = "Successful Response",
                  responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
                  methods: Optional[List[str]] = None, operation_id: Optional[str] = None,
                  response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                  response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                  response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
                  response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
                  include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
                  name: Optional[str] = None, openapi_extra: Optional[Dict[str, Any]] = None,
                  generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                      generate_unique_id
                  )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().api_route(path, response_model=response_model, status_code=status_code, tags=tags,
                                 dependencies=dependencies, summary=summary, description=description,
                                 response_description=response_description, responses=responses, deprecated=deprecated,
                                 methods=methods, operation_id=operation_id,
                                 response_model_include=response_model_include,
                                 response_model_exclude=response_model_exclude,
                                 response_model_by_alias=response_model_by_alias,
                                 response_model_exclude_unset=response_model_exclude_unset,
                                 response_model_exclude_defaults=response_model_exclude_defaults,
                                 response_model_exclude_none=response_model_exclude_none,
                                 include_in_schema=include_in_schema, response_class=response_class, name=name,
                                 openapi_extra=openapi_extra, generate_unique_id_function=generate_unique_id_function)

    def add_api_websocket_route(self, path: str, endpoint: Callable[..., Any], name: Optional[str] = None) -> None:
        super().add_api_websocket_route(path, endpoint, name)

    def websocket(self, path: str, name: Optional[str] = None) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().websocket(path, name)

    def include_router(self, router: routing.APIRouter, *, prefix: str = "",
                       tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
                       responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
                       deprecated: Optional[bool] = None, include_in_schema: bool = True,
                       default_response_class: Type[Response] = Default(JSONResponse),
                       callbacks: Optional[List[BaseRoute]] = None,
                       generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                           generate_unique_id
                       )) -> None:
        super().include_router(router, prefix=prefix, tags=tags, dependencies=dependencies, responses=responses,
                               deprecated=deprecated, include_in_schema=include_in_schema,
                               default_response_class=default_response_class, callbacks=callbacks,
                               generate_unique_id_function=generate_unique_id_function)

    def get(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
            summary: Optional[str] = None, description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
            include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                generate_unique_id
            )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().get(path, response_model=response_model, status_code=status_code, tags=tags,
                           dependencies=dependencies, summary=summary, description=description,
                           response_description=response_description, responses=responses, deprecated=deprecated,
                           operation_id=operation_id, response_model_include=response_model_include,
                           response_model_exclude=response_model_exclude,
                           response_model_by_alias=response_model_by_alias,
                           response_model_exclude_unset=response_model_exclude_unset,
                           response_model_exclude_defaults=response_model_exclude_defaults,
                           response_model_exclude_none=response_model_exclude_none, include_in_schema=include_in_schema,
                           response_class=response_class, name=name, callbacks=callbacks, openapi_extra=openapi_extra,
                           generate_unique_id_function=generate_unique_id_function)

    def put(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
            tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
            summary: Optional[str] = None, description: Optional[str] = None,
            response_description: str = "Successful Response",
            responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
            operation_id: Optional[str] = None,
            response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
            response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
            response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
            include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
            name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
            openapi_extra: Optional[Dict[str, Any]] = None,
            generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                generate_unique_id
            )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().put(path, response_model=response_model, status_code=status_code, tags=tags,
                           dependencies=dependencies, summary=summary, description=description,
                           response_description=response_description, responses=responses, deprecated=deprecated,
                           operation_id=operation_id, response_model_include=response_model_include,
                           response_model_exclude=response_model_exclude,
                           response_model_by_alias=response_model_by_alias,
                           response_model_exclude_unset=response_model_exclude_unset,
                           response_model_exclude_defaults=response_model_exclude_defaults,
                           response_model_exclude_none=response_model_exclude_none, include_in_schema=include_in_schema,
                           response_class=response_class, name=name, callbacks=callbacks, openapi_extra=openapi_extra,
                           generate_unique_id_function=generate_unique_id_function)

    def post(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
             tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
             summary: Optional[str] = None, description: Optional[str] = None,
             response_description: str = "Successful Response",
             responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
             operation_id: Optional[str] = None,
             response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
             response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
             include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
             name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
             openapi_extra: Optional[Dict[str, Any]] = None,
             generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                 generate_unique_id
             )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().post(path, response_model=response_model, status_code=status_code, tags=tags,
                            dependencies=dependencies, summary=summary, description=description,
                            response_description=response_description, responses=responses, deprecated=deprecated,
                            operation_id=operation_id, response_model_include=response_model_include,
                            response_model_exclude=response_model_exclude,
                            response_model_by_alias=response_model_by_alias,
                            response_model_exclude_unset=response_model_exclude_unset,
                            response_model_exclude_defaults=response_model_exclude_defaults,
                            response_model_exclude_none=response_model_exclude_none,
                            include_in_schema=include_in_schema, response_class=response_class, name=name,
                            callbacks=callbacks, openapi_extra=openapi_extra,
                            generate_unique_id_function=generate_unique_id_function)

    def delete(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
               tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
               summary: Optional[str] = None, description: Optional[str] = None,
               response_description: str = "Successful Response",
               responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
               operation_id: Optional[str] = None,
               response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
               response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
               response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
               response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
               include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
               name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
               openapi_extra: Optional[Dict[str, Any]] = None,
               generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                   generate_unique_id
               )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().delete(path, response_model=response_model, status_code=status_code, tags=tags,
                              dependencies=dependencies, summary=summary, description=description,
                              response_description=response_description, responses=responses, deprecated=deprecated,
                              operation_id=operation_id, response_model_include=response_model_include,
                              response_model_exclude=response_model_exclude,
                              response_model_by_alias=response_model_by_alias,
                              response_model_exclude_unset=response_model_exclude_unset,
                              response_model_exclude_defaults=response_model_exclude_defaults,
                              response_model_exclude_none=response_model_exclude_none,
                              include_in_schema=include_in_schema, response_class=response_class, name=name,
                              callbacks=callbacks, openapi_extra=openapi_extra,
                              generate_unique_id_function=generate_unique_id_function)

    def options(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
                tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
                summary: Optional[str] = None, description: Optional[str] = None,
                response_description: str = "Successful Response",
                responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
                operation_id: Optional[str] = None,
                response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
                response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
                response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
                include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
                name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
                openapi_extra: Optional[Dict[str, Any]] = None,
                generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                    generate_unique_id
                )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().options(path, response_model=response_model, status_code=status_code, tags=tags,
                               dependencies=dependencies, summary=summary, description=description,
                               response_description=response_description, responses=responses, deprecated=deprecated,
                               operation_id=operation_id, response_model_include=response_model_include,
                               response_model_exclude=response_model_exclude,
                               response_model_by_alias=response_model_by_alias,
                               response_model_exclude_unset=response_model_exclude_unset,
                               response_model_exclude_defaults=response_model_exclude_defaults,
                               response_model_exclude_none=response_model_exclude_none,
                               include_in_schema=include_in_schema, response_class=response_class, name=name,
                               callbacks=callbacks, openapi_extra=openapi_extra,
                               generate_unique_id_function=generate_unique_id_function)

    def head(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
             tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
             summary: Optional[str] = None, description: Optional[str] = None,
             response_description: str = "Successful Response",
             responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
             operation_id: Optional[str] = None,
             response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
             response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
             response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
             include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
             name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
             openapi_extra: Optional[Dict[str, Any]] = None,
             generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                 generate_unique_id
             )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().head(path, response_model=response_model, status_code=status_code, tags=tags,
                            dependencies=dependencies, summary=summary, description=description,
                            response_description=response_description, responses=responses, deprecated=deprecated,
                            operation_id=operation_id, response_model_include=response_model_include,
                            response_model_exclude=response_model_exclude,
                            response_model_by_alias=response_model_by_alias,
                            response_model_exclude_unset=response_model_exclude_unset,
                            response_model_exclude_defaults=response_model_exclude_defaults,
                            response_model_exclude_none=response_model_exclude_none,
                            include_in_schema=include_in_schema, response_class=response_class, name=name,
                            callbacks=callbacks, openapi_extra=openapi_extra,
                            generate_unique_id_function=generate_unique_id_function)

    def patch(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
              tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
              summary: Optional[str] = None, description: Optional[str] = None,
              response_description: str = "Successful Response",
              responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
              operation_id: Optional[str] = None,
              response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
              response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
              response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
              response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
              include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
              name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
              openapi_extra: Optional[Dict[str, Any]] = None,
              generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                  generate_unique_id
              )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().patch(path, response_model=response_model, status_code=status_code, tags=tags,
                             dependencies=dependencies, summary=summary, description=description,
                             response_description=response_description, responses=responses, deprecated=deprecated,
                             operation_id=operation_id, response_model_include=response_model_include,
                             response_model_exclude=response_model_exclude,
                             response_model_by_alias=response_model_by_alias,
                             response_model_exclude_unset=response_model_exclude_unset,
                             response_model_exclude_defaults=response_model_exclude_defaults,
                             response_model_exclude_none=response_model_exclude_none,
                             include_in_schema=include_in_schema, response_class=response_class, name=name,
                             callbacks=callbacks, openapi_extra=openapi_extra,
                             generate_unique_id_function=generate_unique_id_function)

    def trace(self, path: str, *, response_model: Optional[Type[Any]] = None, status_code: Optional[int] = None,
              tags: Optional[List[Union[str, Enum]]] = None, dependencies: Optional[Sequence[Depends]] = None,
              summary: Optional[str] = None, description: Optional[str] = None,
              response_description: str = "Successful Response",
              responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None, deprecated: Optional[bool] = None,
              operation_id: Optional[str] = None,
              response_model_include: Optional[Union[SetIntStr, DictIntStrAny]] = None,
              response_model_exclude: Optional[Union[SetIntStr, DictIntStrAny]] = None,
              response_model_by_alias: bool = True, response_model_exclude_unset: bool = False,
              response_model_exclude_defaults: bool = False, response_model_exclude_none: bool = False,
              include_in_schema: bool = True, response_class: Type[Response] = Default(JSONResponse),
              name: Optional[str] = None, callbacks: Optional[List[BaseRoute]] = None,
              openapi_extra: Optional[Dict[str, Any]] = None,
              generate_unique_id_function: Callable[[routing.APIRoute], str] = Default(
                  generate_unique_id
              )) -> Callable[[DecoratedCallable], DecoratedCallable]:
        return super().trace(path, response_model=response_model, status_code=status_code, tags=tags,
                             dependencies=dependencies, summary=summary, description=description,
                             response_description=response_description, responses=responses, deprecated=deprecated,
                             operation_id=operation_id, response_model_include=response_model_include,
                             response_model_exclude=response_model_exclude,
                             response_model_by_alias=response_model_by_alias,
                             response_model_exclude_unset=response_model_exclude_unset,
                             response_model_exclude_defaults=response_model_exclude_defaults,
                             response_model_exclude_none=response_model_exclude_none,
                             include_in_schema=include_in_schema, response_class=response_class, name=name,
                             callbacks=callbacks, openapi_extra=openapi_extra,
                             generate_unique_id_function=generate_unique_id_function)
    
