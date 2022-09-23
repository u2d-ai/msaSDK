# -*- coding: utf-8 -*-
""" Healthcheck Pydantic Models

"""
from typing import Optional
from pydantic import BaseModel


class MSAHealthDefinition(BaseModel):
    """Health Service Definition"""

    path: str = "/healthcheck"
    """ Path in URL for the API"""
    interval: Optional[int] = 60
    """ Interval the Healtchcheck Thread sleeps and checks"""
    enabled: bool = True
    """ Is the healtcheck enabled True/False"""


class MSAHealthMessage(BaseModel):
    """Health Pydantic Response Service Message"""

    healthy: bool = False
    message: Optional[str]
    error: Optional[str]
