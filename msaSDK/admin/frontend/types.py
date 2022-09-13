from typing import Dict, Any, Union, List

from pydantic import BaseModel, Extra

try:
    import ujson as json
except ImportError:
    import json

MSAUIExpression = str
MSAUITemplate = Union[str, "MSAUITpl"]
MSAUISchemaNode = Union[MSAUITemplate, "MSAUINode", List["MSAUINode"], Dict[str, Any], List[Dict[str, Any]]]
MSAOptionsNode = Union[List[Dict[str, Any]], List[str]]


class MSABaseUIModel(BaseModel):
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
    msg: str = ''
    data: dict = None


class MSAUINode(MSABaseUIModel):
    """UI Node Component Configuration"""
    type: str = None
    """Component Type"""
    visible: bool = None
    """Enable Visible/Show"""
    hidden: bool = None
    """Hide this node"""
    visibleOn: MSAUIExpression = None
    """Condition for Visibility"""
    hiddenOn: MSAUIExpression = None
    """Condition for Hiding"""
    id: str = None
    """ID of the Node"""
    name: str = None
    """Name of the Node"""
    onEvent: dict = None
    """On MSAUIEvent Handler"""


class MSAUIAPI(MSABaseUIModel):
    """ Core MSA UI API"""
    url: MSAUITemplate
    """Current interface Api address"""
    method: str = None
    """``GET`` holds request method (get, post, put, delete)"""
    data: Union[str, dict] = None
    """Data body of the request, supports data mapping"""
    dataType: str = None
    """Default is json can be configured as form or form-data.
    
    When the data contains a file, the form-data (multipart/form-data) format is automatically used.
    The application/x-www-form-urlencoded format when configured as form.
    """
    qsOptions: Union[str, dict] = None
    """Useful when dataType is form or form-data.
    
    Specific parameters, set by default to: { arrayFormat: 'indices', encodeValuesOnly: true }
    """
    headers: Dict[str, Any] = None
    """The requested headers"""
    sendOn: MSAUIExpression = None
    """Configure the request conditions"""
    cache: int = None
    """Set cache to set the cache time in milliseconds, within the set cache time, the same request will not be repeatedly initiated, but will get the cached request response data.
    """
    requestAdaptor: str = None
    """send adapter , msa_ui's API configuration, if you can not configure the request structure you want, then you can configure the requestAdaptor send adapter"""
    responseData: Dict[str, Any] = None
    """ If the data structure returned by the interface does not meet expectations, you can modify it by configuring responseData, which also supports data mapping.
    The data available for mapping is the actual data of the interface (the data part returned by the interface), with additional api variables.
    where api.query is the query parameter sent by the interface, and api.body is the raw data of the content body sent by the interface.
    """
    replaceData: bool = None
    """Whether the returned data replaces the current data, the default is false, i.e., append, set to true is a complete replacement."""
    adaptor: str = None
    """Receive adapter, if the interface does not meet the requirements, you can configure an adapter to handle it as msa_ui needs.
    Also supports Function or string function styles
    """
    responseType: str = None
    """Return type, if it is a download it needs to be set to ``blob``"""
    autoRefresh: bool = None
    """Configure whether the interface needs to be automatically refreshed."""
    trackExpression: str = None
    """Configure track variable expression, when autoRefresh is enabled, the default is the url of the api to automatically track variable changes.
    If you want to monitor variables outside of the url, configure traceExpression.
    """


MSA_UI_API = Union[str, MSAUIAPI, dict]


class MSAUITpl(MSAUINode):
    """MSAUITpl component"""
    type: str = "tpl"
    """Specify as MSAUITpl component"""
    tpl: str
    """Configuration template"""
    className: str = None
    """Class name of the outer Dom"""


class MSAUIEvent(MSABaseUIModel):
    """MSA UI Event Pydantic Model"""
    actionType: str = None
    """Action name"""
    args: dict = None
    """Action parameter {key:value}, supports data mapping"""
    preventDefault: Union[
        bool, MSAUIExpression] = None
    """False = prevent event default behavior"""
    stopPropagation: Union[
        bool, MSAUIExpression] = None
    """False = Stop the execution of subsequent actions"""
    expression: Union[bool, MSAUIExpression] = None
    """Execution condition, not set means default execution"""
    outputVar: str = None
    """Output data variable name"""
