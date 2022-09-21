# -*- coding: utf-8 -*-

import glob
from os.path import basename, dirname, isfile, join

from ._sqlmodel import MSASQLModelCrud, MSASQLModelSelector
from .base import MSABaseCrud, MSARouterMixin
from .schema import (MSACRUDEnum, MSACRUDListSchema, MSACRUDOut,
                     MSACRUDPaginator, MSACRUDSchema)

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]
