""" Defines all the settings for the feature flgs, switches and conditions
"""
from functools import lru_cache
from typing import List

from sqlmodel import SQLModel

from msaSDK.storagedict import MSAMemoryDict
from msaSDK.storagedict.encoding import PickleEncoding


class MSAFeatureSettings(SQLModel):
    """
    **MSAServiceStatus** Pydantic Response Class
    """
    hirachy_seperator: str = ":"
    """MSASwitch hierarchic seperator String"""
    namespace_separator: str = '.'
    """MSAManager namespace seperator String"""
    default_namespace: List[str] = ['default']
    """MSAManager namespace seperator String"""
    storage_engine = MSAMemoryDict(encoding=PickleEncoding)
    """MSAManager storage engine, MSARedisDict, MSAMemoryDict, MSAZookeeperDict"""
    autocreate = False
    """MSAManager autocreate"""
    inputs = []
    """MSAManager inputs"""
    default = None
    """MSAManager general default"""


@lru_cache()
def get_msa_feature_settings() -> MSAFeatureSettings:
    """
    This function returns a cached instance of the MSAFeatureSettings object.
    Note:
        Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.
    """
    return MSAFeatureSettings()