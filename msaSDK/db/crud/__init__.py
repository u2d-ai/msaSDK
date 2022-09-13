# -*- coding: utf-8 -*-

from os.path import dirname, basename, isfile, join
import glob
from ._sqlmodel import MSASQLModelCrud, MSASQLModelSelector
from .base import MSABaseCrud, MSARouterMixin
from .schema import (
    MSACRUDOut,
    MSACRUDSchema,
    MSACRUDEnum,
    MSACRUDListSchema,
    MSACRUDPaginator
)

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


