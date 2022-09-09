# -*- coding: utf-8 -*-
__version__ = '0.0.3'

from functools import lru_cache
from typing import Dict, List, Optional

from fastapi_utils.api_settings import APISettings
from pydantic import validator, root_validator

from u2d_msa_sdk.models.health import MSAHealthDefinition


class MSAServiceDefinition(APISettings):
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
    name: str = "MSA SDK Service"
    version: str = "0.0.0"
    host: str = "127.0.0.1"
    port: int = 8090
    tags: List[str] = []
    metadata: Optional[Dict]
    allow_origins: List[str] = ["*"]
    """CORSMiddleware. List[str]. List of allowed origins (as strings) or all of them with the wildcard '*' """
    allow_credentials: bool = True
    """CORSMiddleware. Bool. Allow (True) Credentials (Authorization headers, Cookies, etc)."""
    allow_methods: List[str] = ["*"]
    """CORSMiddleware. List[str]. Specific HTTP methods (POST, PUT) or all of them with the wildcard '*' """
    allow_headers: List[str] = ["*"]
    """CORSMiddleware. List[str]. Specific HTTP headers or all of them with the wildcard '*' """
    healthdefinition: MSAHealthDefinition = MSAHealthDefinition()
    uvloop: bool = True
    sysrouter: bool = True
    servicerouter: bool = True
    starception: bool = True
    validationception: bool = True
    httpception: bool = True
    httpception_exclude: List[int] = [307, ]
    cors: bool = True
    httpsredirect: bool = False
    gzip: bool = False
    session: bool = False
    csrf: bool = True
    msgpack: bool = False
    instrument: bool = True
    static: bool = True
    pages: bool = True
    graphql: bool = False
    context: bool = False
    pagination: bool = False
    profiler: bool = False
    templates: bool = True
    templates_dir: List[str] = ["msatemplates", "msatemplates/errors"]
    profiler_output_type: str = "html"  # text or html
    profiler_single_calls: bool = True
    profiler_url: str = '/profiler'
    timing: bool = False
    limiter: bool = False
    scheduler: bool = True
    scheduler_poll_millis: int = 1000
    db: bool = True
    db_debug: bool = False
    db_crud: bool = True
    db_meta_drop: bool = False
    db_meta_create: bool = True
    db_url: str = 'sqlite+aiosqlite:///msa_sdk.db?check_same_thread=True'
    site: bool = True
    site_auth: bool = True
    site_title: str = 'Admin'
    site_copyright: str = 'Copyright © 2022 by u2d.ai'
    site_icon: str = '/msastatic/img/favicon.png'
    site_url: str = ''
    root_path: str = '/admin'
    language: str = ''  # 'zh_CN','en_US'

    @validator('root_path', 'site_url', pre=True)
    def valid_url(cls, url: str):
        return url[:-1] if url.endswith('/') else url


@lru_cache()
def get_msa_app_settings() -> MSAServiceDefinition:
    """
    This function returns a cached instance of the MSAServiceDefinition object.

    Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.
    """
    return MSAServiceDefinition()
