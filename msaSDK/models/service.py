# -*- coding: utf-8 -*-
from functools import lru_cache
from typing import Dict, List, Optional

from fastapi_utils.api_settings import APISettings
from pydantic import validator
from sqlmodel import SQLModel

from msaSDK.models.health import MSAHealthDefinition


class MSAServiceDefinition(APISettings, SQLModel):
    """
    MSAApp Settings (Service Definitions)

    This class enables the configuration of your MSAApp instance through the use of environment variables.

    Any of the instance attributes can be overridden upon instantiation by either passing the desired value to the
    initializer, or by setting the corresponding environment variable.

    Attribute `xxx_yyy` corresponds to environment variable `API_XXX_YYY`. So, for example, to override
    `openapi_prefix`, you would set the environment variable `API_OPENAPI_PREFIX`.

    Note that assignments to variables are also validated, ensuring that even if you make runtime-modifications
    to the config, they should have the correct types.
    """
    name: str = "msaSDK Service"
    """Service Name, also used as Title."""
    version: str = "0.0.0"
    """Version of the Service."""
    host: str = "127.0.0.1"
    """Host/IP which the service runs on."""
    port: int = 8090
    """Port which the service binds to."""
    tags: List[str] = []
    """Optional Metadata: Use this to carry some variables through the service instance."""
    allow_origins: List[str] = ["*"]
    """CORSMiddleware. List[str]. List of allowed origins (as strings) or all of them with the wildcard ``*`` ."""
    allow_credentials: bool = True
    """CORSMiddleware. Bool. Allow (True) Credentials (Authorization headers, Cookies, etc)."""
    allow_methods: List[str] = ["*"]
    """CORSMiddleware. List[str]. Specific HTTP methods (POST, PUT) or all of them with the wildcard ``*`` ."""
    allow_headers: List[str] = ["*"]
    """CORSMiddleware. List[str]. Specific HTTP headers or all of them with the wildcard ``*`` ."""
    healthdefinition: MSAHealthDefinition = MSAHealthDefinition()
    """Healthdefinition Instance."""
    uvloop: bool = True
    """Use UVLoop instead of asyncio loop."""
    sysrouter: bool = True
    """Enable the System Routes defined by router.system module (/sysinfo, /sysgpuinfo, /syserror, ...)."""
    servicerouter: bool = True
    """Enable the Service Routes defined by the MSAApp (/scheduler, /status, /defintion, /settings, /schema, /info, ...)."""
    starception: bool = True
    """Enable Starception Middleware."""
    validationception: bool = True
    """Enable Validation Exception Handler."""
    httpception: bool = True
    """Enable the HTTP Exception Handler, which provides HTML Error Pages instead of JSONResponse."""
    httpception_exclude: List[int] = [307, ]
    """List of HTTP Exception Codes which are excluded and just forwarded by the HTTP Exception Handler."""
    cors: bool = True
    """Enable CORS Middleware."""
    httpsredirect: bool = False
    """Enable HTTPS Redirect Middleware."""
    gzip: bool = False
    """Enable GZIP Middleware."""
    session: bool = False
    """Enable Session Middleware."""
    csrf: bool = True
    """Enable CSRF Forms Protection Middleware."""
    msgpack: bool = False
    """Enable Messagepack Negotiation Middleware."""
    instrument: bool = True
    """Enable Prometheus Instrumentation for the instance."""
    static: bool = True
    """Enable the internal Static Folder (``msastatic``) and Mount to instance."""
    pages: bool = True
    """Enable the Pages Routes (/profiler, /testpage), if site is Off also (/, /monitor, /monitor_inline)."""
    graphql: bool = False
    """Enable initiation of Strawberry GraphQLRouter (/graphql)."""
    context: bool = False
    """Enable Context Middleware."""
    pagination: bool = False
    """Enable FastAPI Pagination."""
    profiler: bool = False
    """Enable Profiler Middleware."""
    profiler_output_type: str = "html"  # text or html
    """Set the Profiler Output Type, should be html or text, html is needed if you want to use the profiler on the Admin Site."""
    profiler_single_calls: bool = True
    """Enable to Track each Request by the Profiler."""
    profiler_url: str = "/profiler"
    """Set the URL to reach the profiler result html, /profiler."""
    templates: bool = True
    """Enable the internal Templates and mount the directory."""
    templates_dir: List[str] = ["msatemplates", "msatemplates/errors"]
    """Set the List of Directories for the MSAUITemplate Engine to look for the requested template."""
    timing: bool = False
    """Enables Timing Middleware, reports timing data at the granularity of individual endpoint calls."""
    limiter: bool = False
    """Enables Rate Limiter (slowapi)."""
    scheduler: bool = True
    "Enables MSA Scheduler Engine."
    scheduler_poll_millis: int = 1000
    """Set's Scheduler Poll Minimum."""
    db: bool = True
    """Enables internal Asynchron SQLite DB."""
    db_debug: bool = False
    """Enables internal DB Debug output."""
    db_crud: bool = True
    """Enables CRUD API creation of the provided SQLModels."""
    db_meta_drop: bool = False
    """If True, all existing Data and Schemas in internal DB get's deleted at Startup."""
    db_meta_create: bool = True
    """Enables internal DB Metadata creation from defined SQLModels at Startup."""
    db_url: str = "sqlite+aiosqlite:///msa_sdk.db?check_same_thread=True"
    """Set's DB URL, compatibility with async and SQLModel/SQLAlchemy is required."""
    site: bool = True
    """Enables internal Admin Site Dashboard."""
    site_auth: bool = False
    """Extends internal Admin Dashboard with Auth."""
    site_title: str = "Admin"
    """Set's internal Admin Dashboard Titel."""
    site_copyright: str = "Copyright © 2022 by u2d.ai"
    """Set's internal Admin Dashboard copyright information."""
    site_icon: str = "/msastatic/img/favicon.png"
    """Set's internal Admin Dashboard Favicon."""
    site_url: str = ""
    """Set's internal Admin Dashboard Site URL, normally empty."""
    root_path: str = "/admin"
    """Set's internal Admin Dashboard Root Path, normally ``/admin``."""
    language: str = ""  # 'zh_CN','en_US'
    """Set's internal Admin Dashboard language (``zh_CN`` or ``en_US``=default if empty)."""

    @validator('root_path', 'site_url', pre=True)
    def valid_url(cls, url: str):
        """ Internal Validator for ``root_path`` and ``site_url`` to remove ending ``/``."""
        return url[:-1] if url.endswith('/') else url


@lru_cache()
def get_msa_app_settings() -> MSAServiceDefinition:
    """
    This function returns a cached instance of the MSAServiceDefinition object.
    Note:
        Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.
    """
    return MSAServiceDefinition()
