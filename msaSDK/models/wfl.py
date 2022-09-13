# -*- coding: utf-8 -*-

from typing import List

from sqlmodel import SQLModel


class WFLModule(SQLModel):
    id: int = -1
    short: str = ""
    name: str = ""
    description: str = ""
    step: str = "00000"

    class Config:
        orm_mode = False


class WFLNodeType(SQLModel):
    id: int = -1
    short: str = ""
    name: str = ""
    description: str = ""
    grp: str = "00000"
    icon: str = "input"

    class Config:
        orm_mode = False


list_node_modules: List[WFLModule] = []
list_node_types: List[WFLNodeType] = []

list_node_modules.append(WFLModule(id=1, short="collect", name="Collect", description="", step="10000"))
list_node_modules.append(WFLModule(id=2, short="convert", name="Convert", description="", step="20000"))
list_node_modules.append(WFLModule(id=3, short="preprocessing", name="Pre-Processing", description="", step="30000"))
list_node_modules.append(WFLModule(id=4, short="processing", name="Processing", description="", step="50000"))
list_node_modules.append(WFLModule(id=5, short="postprocessing", name="Post-Processing", description="", step="70000"))
list_node_modules.append(WFLModule(id=6, short="format", name="Format", description="", step="80000"))
list_node_modules.append(WFLModule(id=7, short="push", name="Push", description="", step="90000"))

list_node_types.append(WFLNodeType(id=1, short="input", name="Input", description="", step="10000"))
list_node_types.append(WFLNodeType(id=2, short="triggers", name="Triggers", description="", step="20000"))
list_node_types.append(WFLNodeType(id=3, short="processors", name="Processors", description="", step="30000"))
list_node_types.append(WFLNodeType(id=4, short="operators", name="Operators", description="", step="50000"))
list_node_types.append(WFLNodeType(id=5, short="actions", name="Actions", description="", step="70000"))
list_node_types.append(WFLNodeType(id=6, short="models", name="Models", description="", step="80000"))
list_node_types.append(WFLNodeType(id=7, short="output", name="Output", description="", step="90000"))
