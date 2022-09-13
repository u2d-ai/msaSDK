# -*- coding: utf-8 -*-
__version__ = '0.1.0'

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
from fastapi.responses import ORJSONResponse
from fastapi.types import DecoratedCallable
from fastapi.utils import generate_unique_id
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import BaseRoute
from starlette.types import ASGIApp, Receive, Scope, Send

if __name__ == '__main__':
    pass


class MSAFastAPI(FastAPI):
    pass
