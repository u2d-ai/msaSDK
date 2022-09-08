# -*- coding: utf-8 -*-
__version__ = '0.0.3'

from functools import lru_cache
from typing import Dict, List, Optional

from fastapi_utils.api_settings import APISettings
from pydantic import BaseModel, typing, validator, root_validator, BaseSettings

from u2d_msa_sdk.models.health import MSAHealthDefinition


class MSAServiceDefinition(APISettings):
    name: str = "MSA SDK Service"
    version: str = "0.0.0"
    host: str = "127.0.0.1"
    port: int = 8090
    tags: List[str] = []
    metadata: Optional[Dict]
    healthdefinition: MSAHealthDefinition = MSAHealthDefinition()
    uvloop: bool = True
    sysrouter: bool = True
    servicerouter: bool = True
    starception: bool = True
    cors: bool = True
    redirect: bool = False
    gzip: bool = False
    session: bool = True
    csrf: bool = True
    msgpack: bool = False
    instrument: bool = True
    static: bool = True
    templates: bool = True
    pages: bool = True
    graphql: bool = False
    context: bool = False
    pagination: bool = False
    profiler: bool = False
    profiler_output_type: str = "html"  # text or html
    profiler_single_calls: bool = True
    profiler_url: str = '/profiler'
    timing: bool = False
    limiter: bool = False
    scheduler: bool = True
    scheduler_poll_millis: int = 1000
    db: bool = True
    db_crud: bool = True
    db_meta_drop: bool = False
    db_meta_create: bool = True
    db_url: str = 'sqlite+aiosqlite:///msa_sdk.db?check_same_thread=False'
    site_title: str = 'Admin'
    site_icon: str = '/msastatic/img/favicon.png'
    site_url: str = ''
    root_path: str = '/admin'
    language: str = ''  # 'zh_CN','en_US'

    @validator('root_path', 'site_url', pre=True)
    def valid_url(cls, url: str):
        return url[:-1] if url.endswith('/') else url

    @root_validator(pre=True)
    def valid_database_url(cls, values):
        if not values.get('db_url'):
            values.setdefault('db_url', 'sqlite+aiosqlite:///msa_sdk.db?check_same_thread=False')
        return values


@lru_cache()
def get_msa_app_settings() -> MSAServiceDefinition:
    """
    This function returns a cached instance of the MSAServiceDefinition object.

    Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.
    """
    return MSAServiceDefinition()
