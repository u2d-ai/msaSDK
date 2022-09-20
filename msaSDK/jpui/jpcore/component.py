"""
Created on 2022-09-02
modified version, original from JustPy
@author: wf (modification swelcker)
"""
from msaSDK.jpui.jpcore.tailwind import Tailwind


# @TODO refactor as per #528
class Component(Tailwind):
    """
    keep track of ids an instances
    """
    next_id = 1
    instances = {}
