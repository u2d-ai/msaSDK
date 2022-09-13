# -*- coding: utf-8 -*-

from enum import Enum
from typing import Dict, TypeVar, Optional, Generic, List, Any, Union

from pydantic import BaseModel, Extra
from pydantic.generics import GenericModel

try:
    import ujson as json
except ImportError:
    import json

_T = TypeVar('_T')


class MSACRUDSchema(BaseModel):
    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps


class MSACRUDOut(GenericModel, Generic[_T], MSACRUDSchema):
    status: int = 0
    msg: str = 'success'
    data: Optional[_T] = None


class MSACRUDListSchema(GenericModel, Generic[_T], MSACRUDSchema):
    items: List[_T]
    total: int = None
    query: Dict[str, Any] = None
    filter: Dict[str, Any] = None


class MSACRUDEnum(str, Enum):
    list = 'list'
    create = 'create'
    read = 'read'
    update = 'update'
    delete = 'delete'


class MSACRUDPaginator:
    perPageMax: int = None

    def __init__(
            self,
            page: Union[int, str] = 1,
            perPage: Union[int, str] = 10,
            show_total: int = 1,
            orderBy: str = None,
            orderDir: str = 'asc'
    ):
        self.page = page if page and page > 0 else 1
        self.perPage = perPage if perPage and perPage > 0 else 10
        if self.perPageMax:
            self.perPage = self.perPage if self.perPage <= self.perPageMax else self.perPageMax
        self.show_total = show_total
        self.orderBy = orderBy
        self.orderDir = orderDir
