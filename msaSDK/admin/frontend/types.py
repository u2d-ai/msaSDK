from typing import Any, Dict, List, Union, Optional

from pydantic import Extra

from msaUtils.base_model import MSABaseModel

import json

MSAUIExpression = str
MSAUITemplate = Union[str, "MSAUITpl"]
MSAUISchemaNode = Union[
    MSAUITemplate, "MSAUINode", List["MSAUINode"], Dict[str, Any], List[Dict[str, Any]]
]
MSAOptionsNode = Union[List[Dict[str, Any]], List[str]]


class MSABaseUIModel(MSABaseModel):
    """Core Pydantic Base UI Model."""

    class Config:
        extra = Extra.allow
        json_loads = json.loads
        json_dumps = json.dumps

    def msa_ui_json(self):
        return self.json(exclude_none=True, by_alias=True)

    def msa_ui_dict(self):
        return self.dict(exclude_none=True, by_alias=True)

    def update_from_dict(self, kwargs: Dict[str, Any]):
        for k, v in kwargs.items():
            setattr(self, k, v)
        return self

    def update_from_kwargs(self, **kwargs):
        return self.update_from_dict(kwargs)


class MSABaseUIApiOut(MSABaseUIModel):
    """MSA UI Api interface output data model"""

    status: int = 0
    msg: str = ""
    data: Optional[dict] = None


class MSAUINode(MSABaseUIModel):
    """UI Node Component Configuration"""

    type: Optional[str] = None
    """Component Type"""
    visible: Optional[bool] = None
    """Enable Visible/Show"""
    hidden: Optional[bool] = None
    """Hide this node"""
    visibleOn: Optional[MSAUIExpression] = None
    """Condition for Visibility"""
    hiddenOn: Optional[MSAUIExpression] = None
    """Condition for Hiding"""
    id: Optional[str] = None
    """ID of the Node"""
    name: Optional[str] = None
    """Name of the Node"""
    onEvent: Optional[Dict] = None
    """On MSAUIEvent Handler"""


class MSAUIAPI(MSABaseUIModel):
    """Core MSA UI API"""

    url: MSAUITemplate
    """Current interface Api address"""
    method: Optional[str] = None
    """``GET`` holds request method (get, post, put, delete)"""
    data: Optional[Union[str, dict]] = None
    """Data body of the request, supports data mapping"""
    dataType: Optional[str] = None
    """Default is json can be configured as form or form-data.
    
    When the data contains a file, the form-data (multipart/form-data) format is automatically used.
    The application/x-www-form-urlencoded format when configured as form.
    """
    qsOptions: Optional[Union[str, dict]] = None
    """Useful when dataType is form or form-data.
    
    Specific parameters, set by default to: { arrayFormat: 'indices', encodeValuesOnly: true }
    """
    headers: Optional[Dict[str, Any]] = None
    """The requested headers"""
    sendOn: Optional[MSAUIExpression] = None
    """Configure the request conditions"""
    cache: Optional[int] = None
    """Set cache to set the cache time in milliseconds, within the set cache time, the same request will not be repeatedly initiated, but will get the cached request response data.
    """
    requestAdaptor: Optional[str] = None
    """send adapter , msa_ui's API configuration, if you can not configure the request structure you want, then you can configure the requestAdaptor send adapter"""
    responseData: Optional[Dict[str, Any]] = None
    """ If the data structure returned by the interface does not meet expectations, you can modify it by configuring responseData, which also supports data mapping.
    The data available for mapping is the actual data of the interface (the data part returned by the interface), with additional api variables.
    where api.query is the query parameter sent by the interface, and api.body is the raw data of the content body sent by the interface.
    """
    replaceData: Optional[bool] = None
    """Whether the returned data replaces the current data, the default is false, i.e., append, set to true is a complete replacement."""
    adaptor: Optional[str] = None
    """Receive adapter, if the interface does not meet the requirements, you can configure an adapter to handle it as msa_ui needs.
    Also supports Function or string function styles
    """
    responseType: Optional[str] = None
    """Return type, if it is a download it needs to be set to ``blob``"""
    autoRefresh: Optional[bool] = None
    """Configure whether the interface needs to be automatically refreshed."""
    trackExpression: Optional[str] = None
    """Configure track variable expression, when autoRefresh is enabled, the default is the url of the api to automatically track variable changes.
    If you want to monitor variables outside of the url, configure traceExpression.
    """


MSA_UI_API = Union[str, MSAUIAPI, dict]


class MSAUITpl(MSAUINode):
    """MSAUITpl component"""

    type: str = "tpl"
    """Specify as MSAUITpl component"""
    tpl: Optional[Any] = None
    """Configuration template"""
    className: Optional[str] = None
    """Class name of the outer Dom"""


class MSAUIEvent(MSABaseUIModel):
    """MSA UI Event Pydantic Model"""

    actionType: Optional[str] = None
    """Action name"""
    args: Optional[Dict] = None
    """Action parameter {key:value}, supports data mapping"""
    preventDefault: Optional[Union[bool, MSAUIExpression]] = None
    """False = prevent event default behavior"""
    stopPropagation: Optional[Union[bool, MSAUIExpression]] = None
    """False = Stop the execution of subsequent actions"""
    expression: Optional[Union[bool, MSAUIExpression]] = None
    """Execution condition, not set means default execution"""
    outputVar: Optional[str] = None
    """Output data variable name"""
