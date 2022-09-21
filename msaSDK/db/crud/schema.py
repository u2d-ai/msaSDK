# -*- coding: utf-8 -*-

from enum import Enum
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

from pydantic import Extra
from pydantic.generics import GenericModel

from msaSDK.utils.base_model import MSABaseModel

import json

_T = TypeVar("_T")


class MSACRUDSchema(MSABaseModel):
    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps


class MSACRUDOut(GenericModel, Generic[_T], MSACRUDSchema):
    status: int = 0
    msg: str = "success"
    data: Optional[_T] = None


class MSACRUDListSchema(GenericModel, Generic[_T], MSACRUDSchema):
    items: List[_T]
    total: Optional[int] = None
    query: Optional[Dict[str, Any]] = None
    filter: Optional[Dict[str, Any]] = None


class MSACRUDEnum(str, Enum):
    list = "list"
    create = "create"
    read = "read"
    update = "update"
    delete = "delete"


class MSACRUDPaginator:
    perPageMax: int = None

    def __init__(
        self,
        page: Union[int, str] = 1,
        perPage: Union[int, str] = 10,
        show_total: int = 1,
        orderBy: str = None,
        orderDir: str = "asc",
    ):
        self.page = page if page and int(page) > 0 else 1
        self.perPage = perPage if perPage and int(perPage) > 0 else 10
        if self.perPageMax:
            self.perPage = (
                self.perPage if self.perPage <= self.perPageMax else self.perPageMax
            )
        self.show_total = show_total
        self.orderBy = orderBy
        self.orderDir = orderDir
