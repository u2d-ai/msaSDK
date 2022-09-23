""" Defines all the settings for the feature flgs, switches and conditions
"""
from functools import lru_cache
from typing import List, Any

from pydantic import typing, BaseModel
from msaSDK.storagedict import MSAMemoryDict
from msaSDK.storagedict.encoding import PickleEncoding


class MSAFeatureSettings(BaseModel):
    """
    **MSAServiceStatus** Pydantic Response Class
    """
    hirachy_seperator: str = ":"
    """MSASwitch hierarchic seperator String"""
    namespace_separator: str = "."
    """MSAManager namespace seperator String"""
    default_namespace: List[str] = ["default"]
    """MSAManager namespace seperator String"""
    storage_engine: Any = None
    """MSAManager storage engine, MSARedisDict, MSAMemoryDict, MSAZookeeperDict"""
    autocreate: bool = False
    """MSAManager autocreate"""
    inputs: List = []
    """MSAManager inputs"""
    default: typing.Callable = None
    """MSAManager general default"""


@lru_cache()
def get_msa_feature_settings() -> MSAFeatureSettings:
    """
    This function returns a cached instance of the MSAFeatureSettings object.
    Note:
        Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.
    """
    feature_set = MSAFeatureSettings()
    feature_set.storage_engine = MSAMemoryDict(encoding=PickleEncoding)
    return feature_set
