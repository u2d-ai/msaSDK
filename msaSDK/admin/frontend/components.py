import os
from typing import Union, List, Optional, Any, Dict

from pydantic import Field

from .constants import LevelEnum, DisplayModeEnum, SizeEnum, TabsModeEnum
from .types import MSA_UI_API, MSAUIExpression, MSAUINode, MSAUISchemaNode, MSAUITemplate, MSABaseUIModel, \
    MSAOptionsNode, MSAUITpl
from .utils import msa_ui_templates

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Html(MSAUINode):
    """Html Node"""
    type: str = "html"
    """ Specify as html component"""
    html: str
    """ html Use MSAUITpl when you need to get variables in the data field."""


class Icon(MSAUINode):
    """icon"""
    type: str = "icon"
    """ Specify the component type"""
    className: str = None
    """ Outer CSS class name"""
    icon: str = None
    """ icon name, supports fontawesome v4 or use url"""


class Remark(MSAUINode):
    """marker"""
    type: str = "remark"
    """ remark"""
    className: str = None
    """ Outer CSS class name"""
    content: str = None
    """ Prompt text"""
    placement: str = None
    """ popup position"""
    trigger: str = None
    """ trigger condition ['hover','focus']"""
    icon: str = None
    """ "fa fa-question-circle" # Icon"""


class Badge(MSAUINode):
    """corner-icon"""
    mode: str = "dot"
    """ Corner type, can be dot/text/ribbon"""
    text: Union[str, int] = None
    """ corner text, supports strings and numbers, invalid when set under mode='dot'"""
    size: int = None
    """ corner size"""
    level: str = None
    """ Corner level, can be info/success/warning/danger, different background color after setting"""
    overflowCount: int = None
    """ 99 # Set the capping number value"""
    position: str = None
    """ "top-right" # corner position, can be top-right/top-left/bottom-right/bottom-left"""
    offset: int = None
    """ corner position, priority is greater than position, when offset is set, postion is top-right as the base for positioning number[top, left]"""
    className: str = None
    """ class name of outer dom"""
    animation: bool = None
    """ whether the corner is animated or not"""
    style: dict = None
    """ custom style for the corner"""
    visibleOn: MSAUIExpression = None
    """ Control the display and hiding of the corner"""


class Page(MSAUINode):
    """page"""
    __default_template_path__: str = f'{BASE_DIR}/templates/page.html'

    type: str = "page"
    """ Specify as Page component"""
    title: MSAUISchemaNode = None
    """ Page title"""
    subTitle: MSAUISchemaNode = None
    """ page sub-title"""
    remark: "Remark" = None
    """ A reminder icon will appear near the title, which will prompt the content when the mouse is placed on it."""
    aside: MSAUISchemaNode = None
    """ Add content to the sidebar area of the page."""
    asideResizor: bool = None
    """ Whether the width of the page's sidebar area can be adjusted"""
    asideMinWidth: int = None
    """ The minimum width of the page's sidebar area"""
    asideMaxWidth: int = None
    """ The maximum width of the page's sidebar area"""
    toolbar: MSAUISchemaNode = None
    """ Add content to the top right corner of the page, note that when there is a title, the area is in the top right corner and when there is not, the area is at the top"""
    body: MSAUISchemaNode = None
    """ Add content to the content area of the page"""
    className: str = None
    """ Outer dom class name"""
    cssVars: dict = None
    """ Custom CSS variables, please refer to styles"""
    toolbarClassName: str = None
    """ "v-middle wrapper text-right bg-light b-b" # Toolbar dom class name"""
    bodyClassName: str = None
    """ "wrapper" # Body dom class name"""
    asideClassName: str = None
    """ "w page-aside-region bg-auto" # Aside dom class name"""
    headerClassName: str = None
    """ "bg-light b-b wrapper" # Header region dom class name"""
    initApi: MSA_UI_API = None
    """ Page The api used to fetch the initial data. the returned data can be used at the entire page level."""
    initFetch: bool = None
    """ True # Whether to start fetching initApi"""
    initFetchOn: MSAUIExpression = None
    """ Whether to start fetching initApi, configured by expression"""
    interval: int = None
    """ Refresh time (min 1000)"""
    silentPolling: bool = None
    """ False # Configure whether to show loading animation when refreshing"""
    stopAutoRefreshWhen: MSAUIExpression = None
    """ Expression to configure the stop refresh condition"""
    regions: List[str] = None

    def msa_ui_html(
            self,
            template_path: str = '',
            locale: str = 'zh_CN',
            site_title: str = 'Admin',
            site_icon: str = '',
    ):
        template_path = template_path or self.__default_template_path__
        return msa_ui_templates(template_path).safe_substitute(
            {
                "MSAUISchemaJson": self.msa_ui_json(),
                "locale": locale,
                "site_title": site_title,
                "site_icon": site_icon,
            }
        )


class Divider(MSAUINode):
    type: str = "divider"
    """ Divider"""
    className: str = None
    """ class name of the outer Dom"""
    lineStyle: str = None
    """ The style of the divider line, supports dashed and solid"""


class Flex(MSAUINode):
    type: str = "flex"
    """ Specify as Flex renderer"""
    className: str = None
    """ css class name"""
    justify: str = None
    """ "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly" """
    alignItems: str = None
    """ "stretch", "start", "flex-start", "flex-end", "end", "center", "baseline" """
    style: dict = None
    """ Custom style"""
    items: List[MSAUISchemaNode] = None



class Grid(MSAUINode):
    class Column(MSAUINode):
        xs: int = None
        """ "auto" # Width percentage: 1 - 12"""
        ClassName: str = None
        """ Column class name"""
        sm: int = None
        """ "auto" # Width ratio: 1 - 12"""
        md: int = None
        """ "auto" # Width ratio: 1 - 12"""
        lg: int = None
        """ "auto" # Width ratio: 1 - 12"""
        valign: str = None
        """ 'top'|'middle'|'bottom'|'between = None # Vertical alignment of current column content"""
        body: List[MSAUISchemaNode] = None


    type: str = "grid"
    """ Specify as Grid renderer"""
    className: str = None
    """ Class name of the outer Dom"""
    gap: str = None
    """ 'xs'|'sm'|'base'|'none'|'md'|'lg = None # Horizontal spacing"""
    valign: str = None
    """ 'top'|'middle'|'bottom'|'between = None # Vertical alignment"""
    align: str = None
    """ 'left'|'right'|'between'|'center = None # horizontal alignment"""
    columns: List[MSAUISchemaNode] = None



class Panel(MSAUINode):
    type: str = "panel"
    """ Specify as Panel renderer"""
    className: str = None
    """ "panel-default" # class name of outer Dom"""
    headerClassName: str = None
    """ "panel-heading" # Class name of the header area"""
    footerClassName: str = None
    """ "panel-footer bg-light lter wrapper" # Class name of the footer region"""
    actionsClassName: str = None
    """ "panel-footer" # Class name of the actions region"""
    bodyClassName: str = None
    """ "panel-body" # Class name for the body region"""
    title: MSAUISchemaNode = None
    """ title"""
    header: MSAUISchemaNode = None
    """ header container"""
    body: MSAUISchemaNode = None
    """ content container"""
    footer: MSAUISchemaNode = None
    """ footer container"""
    affixFooter: bool = None
    """ Whether to fix the bottom container"""
    actions: List["Action"] = None
    """ Button area"""


class Tabs(MSAUINode):
    class Item(MSAUINode):
        title: str = None
        """ Tab title"""
        icon: Union[str, Icon] = None
        """ Tab's icon"""
        tab: MSAUISchemaNode = None
        """ Content area"""
        hash: str = None
        """ Set to correspond to the hash of the url"""
        reload: bool = None
        """ Set the content to be re-rendered every time, useful for crud re-pulling"""
        unmountOnExit: bool = None
        """ Destroy the current tab bar every time you exit"""
        className: str = None
        """ "bg-white b-l b-r b-b wrapper-md" # Tab area style"""
        iconPosition: str = None
        """ "left" # Tab's icon position left / right"""
        closable: bool = None
        """ False # Whether to support deletion, prioritize over component's closable"""
        disabled: bool = None
        """ False # Whether to disable"""

    type: str = "tabs"
    """ Specify as Tabs renderer"""
    className: str = None
    """ The class name of the outer Dom"""
    mode: str = None
    """ Display mode, can be line, card, radio, vertical, chrome, simple, strong, tiled, sidebar"""
    tabsClassName: str = None
    """ The class name of the Tabs Dom"""
    tabs: List[Item] = None
    """ tabs content"""
    source: str = None
    """ tabs association data, can repeat tabs after association"""
    toolbar: MSAUISchemaNode = None
    """ Toolbar in tabs"""
    toolbarClassName: str = None
    """ The class name of the toolbar in tabs"""
    mountOnEnter: bool = None
    """ False # Render only when tab is clicked"""
    unmountOnExit: bool = None
    """ False # Destroy when tab is toggled"""
    scrollable: bool = None
    """ False # whether navigation supports content overflow scrolling, not supported in vertical and chrome modes; chrome mode compresses tabs by default (property deprecated)"""
    tabsMode: TabsModeEnum = None
    """ display mode, the value can be line, card, radio, vertical, chrome, simple, strong, tiled, sidebar"""
    addable: bool = None
    """ False # If or not addable is supported"""
    addBtnText: str = None
    """ "add" # Add button text"""
    closeable: bool = None
    """ False # Whether to support delete"""
    draggable: bool = None
    """ False # Whether drag and drop is supported"""
    showTip: bool = None
    """ False # Whether to support hints"""
    showTipClassName: str = None
    """ "'' " # The class of the prompt"""
    editable: bool = None
    """ False # Whether to make the tag name editable or not"""
    sidePosition: str = None
    """ "left" # sidebar mode, tab position left / right"""


class Portlet(Tabs):
    class Item(Tabs.Item):
        toolbar: MSAUISchemaNode = None
        """ toolbar in tabs, changes with tab toggle"""

    type: str = "portlet"
    """ Specify as Portlet renderer"""
    contentClassName: str = None
    """ Class name of the Tabs content Dom"""
    tabs: List[Item] = None
    """ Contents of tabs"""
    style: Union[str, dict] = None
    """ Custom style"""
    description: MSAUITemplate = None
    """ Information on the right side of the title"""
    hideHeader: bool = None
    """ False # Hide the header"""
    divider: bool = None
    """ False # Remove the divider"""


class Horizontal(MSAUINode):
    left: int = None
    """ The width of the left label as a percentage"""
    right: int = None
    """ The width share of the right controller."""
    offset: int = None
    """ The offset of the right controller when no label is set"""


class Action(MSAUINode):
    type: str = "button"
    """ Specify as Page renderer. button action"""
    actionType: str = None
    """ [Required] This is the core configuration of the action, to specify the action's role type.
    Supports: ajax, link, url, drawer, dialog, confirm, cancel, prev, next, copy, close.
    """
    label: str = None
    """ The text of the button. Can be fetched with ${xxx}."""
    level: LevelEnum = None
    """ The style of the button, support: link, primary, secondary, info, success, warning, danger, light, dark, default."""
    size: str = None
    """ The size of the button, support: xs, sm, md, lg."""
    icon: str = None
    """ Set icon, e.g. fa fa-plus."""
    iconClassName: str = None
    """ Add a class name to the icon."""
    rightIcon: str = None
    """ Set the icon to the right of the button text, e.g. fa fa-plus."""
    rightIconClassName: str = None
    """ Add a class name to the right icon."""
    active: bool = None
    """ If or not the button is highlighted."""
    activeLevel: str = None
    """ The style of the button when it is highlighted, configured to support the same level."""
    activeClassName: str = None
    """ Add a class name to the button highlighting. "is-active" """
    block: bool = None
    """ Use display: "block" to display the button."""
    confirmText: MSAUITemplate = None
    """ When set, the action will ask the user before starting. Can be fetched with ${xxx}."""
    reload: str = None
    """ Specify the name of the target component to be refreshed after this operation (the component's name value, configured by yourself), separated by ,."""
    tooltip: str = None
    """ popup text when mouse hover, also can configure the object type: title and content. can be ${xxx}."""
    disabledTip: str = None
    """ Popup when mouse hover is disabled, you can also configure the object type: fields are title and content. available ${xxx}."""
    tooltipPlacement: str = None
    """ If tooltip or disabledTip is configured, specify the location of the tip, you can configure top, bottom, left, right."""
    close: Union[
        bool, str] = None
    """ When action is configured in dialog or drawer's actions, set to true to close the current dialog or drawer after this action."""
    required: List[
        str] = None
    """ Configure an array of strings, specifying that the form entry of the specified field name is required to pass validation before the operation can be performed in the form"""
  
    # primary:bool=None
    onClick: str = None
    """ Customize the click event by defining the click event as a string onClick, which will be converted to a JavaScript function"""
    componentId: str = None
    """ Target component ID"""
    args: Union[dict, str] = None
    """ Event arguments"""
    script: str = None
    """ Custom JS script code, which can perform any action by calling doAction, and event action intervention through the event object event"""


class ActionType:
    class Ajax(Action):
        actionType: str = 'ajax'
        """ Click to display a popup box"""
        api: MSA_UI_API = None
        """ request address, refer to api format description."""
        redirect: MSAUITemplate = None
        """ Specify the path to jump to at the end of the current request, can be fetched with ${xxx}."""
        feedback: "Dialog" = None
        """ If ajax type, when the ajax returns normal, a dialog can be popped up to do other interactions. The returned data can be used in this dialog. See Dialog for format"""
        messages: dict = None
        """ success: ajax operation success prompt, can not be specified, not specified when the api return prevail. failed: ajax operation failure prompt."""

    class Dialog(Action):
        actionType: str = 'dialog'
        """ Show a popup box when clicked."""
        dialog: Union[
            "Dialog", "Service", MSAUISchemaNode]
        """ Specify the content of the popup box, see Dialog for format"""
        nextCondition: bool = None
        """ Can be used to set the next data condition, default is true."""

    class Drawer(Action):
        actionType: str = 'drawer'
        """ Show a sidebar when clicked"""
        drawer: Union[
            "Drawer", "Service", MSAUISchemaNode]
        """ Specify the content of the popup box, see Drawer for format"""

    class Copy(Action):
        actionType: str = 'copy'
        """ Copy a piece of content to the pasteboard"""
        content: MSAUITemplate
        """ Specify the content to be copied. Can be fetched with ${xxx}."""
        copyFormat: str = None
        """ The format of the copy can be set by copyFormat, default is text/html"""

    class Url(Action):
        actionType: str = 'url'
        """ Jump directly """
        url: str
        """ When the button is clicked, the specified page will be opened. Can be fetched with ${xxx}. """
        blank: bool = None
        """ false if true will open in a new tab page. """

    class Link(Action):
        actionType: str = 'link'
        link: str


class PageSchema(MSAUINode):
    label: str = None
    """ The name of the menu. """
    icon: str = 'fa fa-flash'
    """ Menu icon, e.g., 'fa fa-file'. """
    url: str = None
    """ The page routing path to enable the current page when the route hits that path. When the path is not /-headed, the parent path is connected.
        For example, if the parent path is folder and pageA is configured, then the page will be hit when the page address is /folder/pageA. 
        When the path starts with /, e.g. /crud/list, the parent path is not concatenated. 
        There is also support for routes with parameters such as /crud/view/:id, which can be fetched from the page via ${params.id}. """
    schema_: Union[Page, "Iframe"] = Field(None,
                                           alias='schema')
    """ Configuration of the page, please go to the Page page for details """
    schemaApi: MSA_UI_API = None
    """ If you want to pull through the interface, please configure it. The return path is json>data. schema and schemaApi can only be one or the other. """
    link: str = None
    """ If you want to configure an external link menu, just configure link. """
    redirect: str = None
    """ Jump, when the current page is hit, jump to the target page. """
    rewrite: str = None
    """ Change to render a page with another path, this way the page address will not be changed. """
    isDefaultPage: Union[
        str, bool] = None
    """ Useful when you need a custom 404 page, don't have more than one of these, because only the first one will work. """
    visible: str = None
    """ Some pages may not want to appear in the menu, you can configure it to false, in addition to the route with parameters do not need to be configured, directly is not visible. """
    className: str = None
    """ The class name of the menu. """
    children: List["PageSchema"] = None
    """ Submenus """
    sort: int = None
    """ Sort """

    def as_tabs_item(self, tabs_extra: Dict[str, Any] = None, item_extra: Dict[str, Any] = None):
        if self.children:
            tabs = Tabs(
                tabs=[item.as_tabs_item(tabs_extra, item_extra) for item in self.children]
            ).update_from_dict(tabs_extra or {})
        elif self.schema_:
            tab = self.schema_
            if isinstance(tab, Iframe):
                tab.height = 1080
        elif self.schemaApi:
            tab = Service(schemaApi=self.schemaApi)
        elif self.link:
            tab = Page(body=Link(href=self.link, body=self.label, blank=True))
        else:
            tab = None
        return Tabs.Item(
            title=self.label,
            icon=self.icon,
            tab=tab,
        ).update_from_dict(item_extra or {})


class App(Page):
    """multi-page app"""
    __default_template_path__: str = f'{BASE_DIR}/templates/app.html'
    type: str = "app"
    api: MSA_UI_API = None
    """ Page configuration interface, please configure if you want to pull the page configuration remotely. Return the configuration path json>data>pages, please refer to the pages property for the exact format. """
    brandName: str = None
    """ Application name """
    logo: str = "/msastatic/img/msa_logo.png"
    """ Support image address, or svg. """
    className: str = None
    """ css class name """
    header: str = None
    """ header """
    asideBefore: str = None
    """ The area in front of the page menu. """
    asideAfter: str = None
    """ The area under the page menu. """
    footer: str = None
    """ The page. """
    pages: List[PageSchema] = None
    """ Array<PageSchema> specific page configuration.
        Usually an array, the first layer of the array is grouped, usually only the label set needs to be configured, 
        if you do not want to group, directly not configured, the real pages please start configuring in the second layer, 
        that is, the first layer of children. """


class ButtonGroup(MSAUINode):
    """buttonGroup"""
    type: str = 'button-group'
    buttons: List[Action]
    """ Behavior button group """
    className: str = None
    """ the class name of the outer Dom """
    vertical: bool = None
    """ whether to use vertical mode """


class Custom(MSAUINode):
    """custom component"""
    type: str = 'custom'
    id: str = None
    """ node id """
    name: str = None
    """ node name """
    className: str = None
    """ node class """
    inline: bool = False
    """ default use div tag, if true use span tag """
    html: str = None
    """ Initialize node html """
    onMount: str = None
    """ "Function" # The function to call after the node is initialized """
    onUpdate: str = None
    """ "Function" # Function to be called when data is updated """
    onUnmount: str = None
    """ "Function" # The function called when the node is destroyed """


class Service(MSAUINode):
    """Function container"""
    type: str = "service"
    """ Specified as a service renderer """
    name: str = None
    """ node name """
    data: dict = None
    className: str = None
    """ Class name of the outer Dom """
    body: MSAUISchemaNode = None
    """ Content container """
    api: MSA_UI_API = None
    """ Initial data domain interface address """
    ws: str = None
    """ WebScocket address """
    dataProvider: str = None
    """ Data fetch function """
    initFetch: bool = None
    """ Whether to pull by default """
    schemaApi: MSA_UI_API = None
    """ Used to fetch the remote Schema interface address """
    initFetchSchema: bool = None
    """ Whether to pull Schema by default """
    messages: dict = None
    """ Message hint override, the default message reads the toast hint text returned by the interface, but it can be overridden here. """
    interval: int = None
    """ polling interval (minimum 3000) """
    silentPolling: bool = None
    """ False # Configure whether to show loading animation when polling """
    stopAutoRefreshWhen: MSAUIExpression = None
    """ Configure the conditions for stopping polling """


class Nav(MSAUINode):
    """Navigate"""

    class Link(MSAUINode):
        label: str = None
        """ Name """
        to: MSAUITemplate = None
        """ Link address """
        target: str = None
        """ "Link relationship" # """
        icon: str = None
        """ Icon """
        children: List["Link"] = None
        """ child links """
        unfolded: bool = None
        """ Initially expanded or not """
        active: bool = None
        """ Whether to highlight or not """
        activeOn: MSAUIExpression = None
        """ condition to highlight or not, leaving blank will automatically analyze the link address """
        defer: bool = None
        """ Flag if it is a lazy add-on """
        deferApi: MSA_UI_API = None
        """ Can be unconfigured, if configured priority is higher """

    type: str = "nav"
    """ Specify as Nav renderer """
    className: str = None
    """ Class name of the outer Dom """
    stacked: bool = True
    """ Set to false to display as tabs """
    source: MSA_UI_API = None
    """ Navigation can be created dynamically via variables or the MSA_UI_API interface """
    deferApi: MSA_UI_API = None
    """ Interface used to delay loading of option details, can be left unconfigured, no common source interface configured. """
    itemActions: MSAUISchemaNode = None
    """ More action related configuration """
    draggable: bool = None
    """ Whether to support drag and drop sorting """
    dragOnSameLevel: bool = None
    """ Only allows dragging within the same level """
    saveOrderApi: MSA_UI_API = None
    """ api to save sorting """
    itemBadge: Badge = None
    """ corner markers """
    links: list = None
    """ Collection of links """


class AnchorNav(MSAUINode):
    """Anchor Nav"""

    class Link(MSAUINode):
        label: str = None
        """ name """
        title: str = None
        """ area title """
        href: str = None
        """ region identifier """
        body: MSAUISchemaNode = None
        """ area content area """
        className: str = None
        """ "bg-white b-l b-r b-b wrapper-md" # region member style """

    type: str = "anchor-nav"
    """ Specify as AnchorNav renderer """
    className: str = None
    """ Class name of the outer Dom """
    linkClassName: str = None
    """ Class name of the navigating Dom """
    sectionClassName: str = None
    """ Class name of the anchor area Dom """
    links: list = None
    """ Contents of links """
    direction: str = None
    """ "vertical" # You can configure whether the navigation is displayed horizontally or vertically. The corresponding configuration items are: vertical, horizontal """
    active: str = None
    """ The area to be positioned """


class ButtonToolbar(MSAUINode):
    """ButtonToolbar"""
    type: str = 'button-toolbar'
    buttons: List[Action]
    """ Behavior button group """


class Validation(MSABaseUIModel):
    isEmail: bool = None
    """ Must be Email. """
    isUrl: bool = None
    """ Must be Url. """
    isNumeric: bool = None
    """ Must be numeric. """
    isAlpha: bool = None
    """ Must be a letter. """
    isAlphanumeric: bool = None
    """ Must be alphabetic or numeric. """
    isInt: bool = None
    """ Must be integer. """
    isFloat: bool = None
    """ Must be floating point. """
    isLength: int = None
    """ If or not the length is exactly equal to the set value. """
    minLength: int = None
    """ The minimum length. """
    maxLength: int = None
    """ The maximum length. """
    maximum: int = None
    """ The maximum value. """
    minimum: int = None
    """ The minimum value. """
    equals: str = None
    """ The current value must be exactly equal to xxx. """
    equalsField: str = None
    """ The current value must match the value of the xxx variable. """
    isJson: bool = None
    """ If or not it is a legal Json string.
    isUrlPath: bool = None """
    """ Is the url path. """
    isPhoneNumber: bool = None
    """ If or not it is a legitimate phone number """
    isTelNumber: bool = None
    """ if it is a legitimate phone number """
    isZipcode: bool = None
    """ Whether it is a zip code number """
    isId: bool = None
    """ if it is an ID number, no check """
    matchRegexp: str = None
    """ Must hit some regular. /foo/ """


class FormItem(MSAUINode):
    """FormItemGeneral"""
    type: str = 'input-text'
    """ Specify the form item type """
    className: str = None
    """ The outermost class name of the form """
    inputClassName: str = None
    """ Form controller class name """
    labelClassName: str = None
    """ Class name of the label """
    name: str = None
    """ Field name, specifying the key of the form item when it is submitted """
    label: MSAUITemplate = None
    """ Label of the form item Template or false """
    value: Union[int, str] = None
    """ The value of the field """
    labelRemark: "Remark" = None
    """ Description of the form item label """
    description: MSAUITemplate = None
    """ Form item description """
    placeholder: str = None
    """ Form item description """
    inline: bool = None
    """ Whether inline mode """
    submitOnChange: bool = None
    """ Whether to submit the current form when the value of the form item changes. """
    disabled: bool = None
    """ Whether the current form item is disabled or not """
    disabledOn: MSAUIExpression = None
    """ The condition whether the current form item is disabled or not """
    visible: MSAUIExpression = None
    """ The condition whether the current form item is disabled or not """
    visibleOn: MSAUIExpression = None
    """ The condition if the current table item is disabled or not """
    required: bool = None
    """ Whether or not it is required. """
    requiredOn: MSAUIExpression = None
    """ Expression to configure if the current form entry is required. """
    validations: Union[
        Validation, MSAUIExpression] = None
    """ Form item value format validation, support setting multiple, multiple rules separated by English commas. """
    validateApi: MSAUIExpression = None
    """ Form validation interface """
    copyable: Union[bool, dict] = None
    """ Whether copyable boolean or {icon: string, content:string} """


class Form(MSAUINode):
    """Form"""

    class Messages(MSAUINode):
        fetchSuccess: str = None
        """ Prompt when fetch succeeds """
        fetchFailed: str = None
        """ prompt for fetch failure """
        saveSuccess: str = None
        """ Prompt for successful save """
        saveFailed: str = None
        """ Prompt for failed save """

    type: str = "form"
    """ "form" is specified as a Form renderer """
    name: str = None
    """ Set a name so that other components can communicate with it """
    mode: DisplayModeEnum = None
    """ How the form is displayed, either: normal, horizontal or inline """
    horizontal: Horizontal = None
    """ Useful when mode is horizontal. """
  
    """ Used to control label {"left": "col-sm-2", "right": "col-sm-10", "offset": "col-sm-offset-2"} """
    title: Optional[str] = None
    """ Title of the Form """
    submitText: Optional[
        str] = None
    """ "submit" # The default submit button name, if set to null, the default button can be removed. """
    className: str = None
    """ The class name of the outer Dom """
    body: List[Union[FormItem, MSAUISchemaNode]] = None
    """ Form form item collection """
    actions: List["Action"] = None
    """ Form submit button, member of Action """
    actionsClassName: str = None
    """ Class name of actions """
    messages: Messages = None
    """ Message prompt override, the default message reads the message returned by MSA_UI_API, but it can be overridden here. """
    wrapWithPanel: bool = None
    """ Whether to let Form wrap with panel, set to false and actions will be invalid. """
    panelClassName: str = None
    """ The class name of the outer panel """
    api: MSA_UI_API = None
    """ The api used by Form to save data. """
    initApi: MSA_UI_API = None
    """ The api used by Form to get the initial data. """
    rules: list = None
    """ Form combination check rules Array<{rule:string;message:string}> """
    interval: int = None
    """ Refresh time (minimum 3000) """
    silentPolling: bool = False
    """ Configure whether to show loading animation when refreshing """
    stopAutoRefreshWhen: str = None
    """ Configure the conditions for stopping the refresh via an expression """
    initAsyncApi: MSA_UI_API = None
    """ The api used by Form to get the initial data, unlike initApi, it will keep polling the request until the finished property is returned as true. """
    initFetch: bool = None
    """ When initApi or initAsyncApi is set, the request will start by default, but when set to false, the interface will not be requested from the beginning. """
    initFetchOn: str = None
    """ Use an expression to configure """
    initFinishedField: Optional[
        str] = None
    """ When initAsyncApi is set, the default is to determine if the request is completed by returning data.finished. """
  
    """ You can also set it to other xxx, and it will be retrieved from data.xxx """
    initCheckInterval: int = None
    """ After setting initAsyncApi, the default time interval for pulling """
    asyncApi: MSA_UI_API = None
    """ After this property is set, the form will continue to poll the interface after it is submitted and sent to the saved interface until the finished property is returned as true. """
    checkInterval: int = None
    """ The time interval to poll the request, default is 3 seconds. Set asyncApi to be valid """
    finishedField: Optional[
        str] = None
    """ Set this property if the field name that determines the finish is not finished, e.g. is_success """
    submitOnChange: bool = None
    """ The form is submitted when it is modified """
    submitOnInit: bool = None
    """ Submit once at the beginning """
    resetAfterSubmit: bool = None
    """ whether to reset the form after submission """
    primaryField: str = None
    """ Set primary key id, when set, only carry this data when detecting form completion (asyncApi). """
    target: str = None
    """ The default form submission saves the data itself by sending the api, but you can set the name value of another form
    or the name value of another CRUD model. If the target is a Form, the target Form will retrigger initApi and the api will get the current form data. 
    If the target is a CRUD model, the target model retriggers the search with the current Form data as the argument. When the target is a window, the current form data will be attached to the page address. """
    redirect: str = None
    """ When this property is set, the Form will automatically jump to the specified page after a successful save. Supports relative addresses, and absolute addresses (relative to the group). """
    reload: str = None
    """ Refresh the target object after the operation. Please fill in the name value set by the target component, if you fill in the name of window, the current page will be refreshed as a whole. """
    autoFocus: bool = None
    """ If or not autoFocus is enabled. """
    canAccessSuperData: bool = None
    """ Specifies whether the data from the upper level can be automatically retrieved and mapped to the form item. """
    persistData: str = None
    """ Specify a unique key to configure whether to enable local caching for the current form """
    clearPersistDataAfterSubmit: bool = None
    """ Specify whether to clear the local cache after a successful form submission """
    preventEnterSubmit: bool = None
    """ Disable carriage return to submit the form """
    trimValues: bool = None
    """ trim each value of the current form item """
    promptPageLeave: bool = None
    """ whether the form is not yet saved and will pop up before leaving the page to confirm. """
    columnCount: int = None
    """ How many columns are displayed for the form item """
    debug: bool = None


class Button(FormItem):
    """Button"""
    className: str = None
    """ Specifies the class name of the added button """
    href: str = None
    """ Click on the address of the jump, specify this property button behavior and a link consistent """
    size: str = None
    """ Set the size of the button 'xs'|'sm'|'md'|'lg' """
    actionType: str = None
    """ Set the button type 'button'|'reset'|'submit'| 'clear'| 'url' """
    level: LevelEnum = None
  
    """ Set the button style 'link'|'primary'|'enhance'|'secondary'|'info'|'success'|'warning'|'danger'|'light'| 'dark'|'default' """
    tooltip: Union[str, dict] = None
    """ bubble tip content TooltipObject """
    tooltipPlacement: str = None
    """ bubblePlacement 'top'|'right'|'bottom'|'left' """
    tooltipTrigger: str = None
    """ trigger tootip 'hover'|'focus' """
    disabled: bool = None
    """ Disable button status """
    block: bool = None
    """ option to adjust the width of the button to its parent width """
    loading: bool = None
    """ Show button loading effect """
    loadingOn: str = None
    """ Show button loading expressions """


class InputArray(FormItem):
    """arrayInputArray"""
    type: str = 'input-array'
    items: FormItem = None
    """ Configure single-item form type """
    addable: bool = None
    """ Whether addable. """
    removable: bool = None
    """ Whether removable """
    draggable: bool = False
    """ whether draggable, note that when draggable is enabled, there will be an extra $id field """
    draggableTip: str = None
    """ draggable prompt text, default is: "can be adjusted by dragging the [swap] button in each row" """
    addButtonText: str = None
    """ "Add" # Add button text """
    minLength: int = None
    """ Limit the minimum length """
    maxLength: int = None
    """ Limit the maximum length """


class Hidden(FormItem):
    """hiddenField"""
    type: str = 'hidden'


class Checkbox(FormItem):
    """Checkbox"""
    type: str = 'checkbox'
    option: str = None
    """ option description """
    trueValue: Any = None
    """ Identifies the true value """
    falseValue: Any = None
    """ Identifies a false value """


class Radios(FormItem):
    """RadioBox"""
    type: str = 'radios'
    options: List[Union[dict, str]] = None
    """ option group """
    source: MSA_UI_API = None
    """ dynamic options group """
    labelField: bool = None
    """ "label" # option label field """
    valueField: bool = None
    """ "value" # option value field """
    columnsCount: int = None
    """ 1 # How many columns to display options by, default is one column """
    inline: bool = None
    """ True # Whether to display as one line """
    selectFirst: bool = None
    """ False # Whether to select the first by default """
    autoFill: dict = None
    """ AutoFill """


class ChartRadios(Radios):
    """radio box"""
    type: str = 'chart-radios'
    config: dict = None
    """ echart chart configuration """
    showTooltipOnHighlight: bool = None
    """ False # whether to show tooltip when highlighted """
    chartValueField: str = None
    """ "value" # chart value field name """


class Checkboxes(FormItem):
    """checkboxes"""
    type: str = 'checkboxes'
    options: MSAOptionsNode = None
    """ Options group """
    source: MSA_UI_API = None
    """ dynamic options group """
    delimiter: str = None
    """ "," # Splice character """
    labelField: str = None
    """ "label" # option label field """
    valueField: str = None
    """ "value" # option value field """
    joinValues: bool = None
    """ True # splice values """
    extractValue: bool = None
    """ False # extract value """
    columnsCount: int = None
    """ 1 # How many columns to display options by, default is one column """
    checkAll: bool = None
    """ False # If or not checkAll is supported """
    inline: bool = None
    """ True # Whether to display as one line """
    defaultCheckAll: bool = None
    """ False # Whether to check all by default """
    creatable: bool = None
    """ False # New option """
    createBtnLabel: str = None
    """ "Add option" # Add option """
    addControls: List[FormItem] = None
    """ Customize the new form item """
    addApi: MSA_UI_API = None
    """ Configure the add options interface """
    editable: bool = None
    """ False # Edit options """
    editControls: List[FormItem] = None
    """ Customize edit form items """
    editApi: MSA_UI_API = None
    """ Configure the edit options interface """
    removable: bool = None
    """ False # Remove options """
    deleteApi: MSA_UI_API = None
    """ Configure the delete option interface """


class InputCity(FormItem):
    """city selector"""
    type: str = 'location-city'
    allowCity: bool = None
    """ True # Allow city selection """
    allowDistrict: bool = None
    """ True # Allow district selection """
    searchable: bool = None
    """ False # Whether or not the search box is available """
    extractValue: bool = None
    """ True # whether to extract the value, if set to false the value format will become an object containing code, province, city and district text information. """


class InputColor(FormItem):
    """color picker"""
    type: str = 'input-color'
    format: str = None
    """ "hex" # Please choose hex, hls, rgb or rgba. """
    presetColors: List[
        str] = None
    """ "selector preset color values" # default color at the bottom of the selector, if the array is empty, no default color is shown """
    allowCustomColor: bool = None
    """ True # When false, only colors can be selected, use presetColors to set the color selection range """
    clearable: bool = None
    """ "label" # whether to show clear button """
    resetValue: str = None
    """ "" # After clearing, the form item value is adjusted to this value """


class Combo(FormItem):
    """combo"""
    type: str = 'combo'
    formClassName: str = None
    """ class name of a single group of form items """
    addButtonClassName: str = None
    """ Add button CSS class name """
    items: List[FormItem] = None
    """ Combined form items to be displayed 
    items[x].columnClassName: str = None # The class name of the column with which to configure the column width. Default is evenly distributed. 
    items[x].unique: bool = None # Set whether the current column value is unique, i.e. no duplicate selections are allowed. """
    noBorder: bool = False
    """ Whether to show border for a single group of table items """
    scaffold: dict = {}
    """ The initial value of a single table item """
    multiple: bool = False
    """ Whether or not to multi-select """
    multiLine: bool = False
    """ Default is to display a row horizontally, set it to display vertically """
    minLength: int = None
    """ The minimum number of items to add """
    maxLength: int = None
    """ The maximum number of items to add """
    flat: bool = False
    """ Whether to flatten the results (remove the name), only valid if the length of items is 1 and multiple is true. """
    joinValues: bool = True
    """ Defaults to true when flattening is on, whether to send to the backend as a delimiter, otherwise as an array. """
    delimiter: str = None
    """ "False" # What delimiter to use when flattening is on and joinValues is true. """
    addable: bool = False
    """ Whether to add """
    addButtonText: str = None
    """ "Add" # Add button text """
    removable: bool = False
    """ If or not it can be removed """
    deleteApi: MSA_UI_API = None
    """ If configured, an api will be sent before deletion, and the deletion will be completed only if the request is successful """
    deleteConfirmText: str = None
    """ "Confirm to delete?" """
    """ Only when deleteApi is configured does it take effect! Used to do user confirmation when deleting """
    draggable: bool = False
    """ whether draggable sorting is possible, note that when draggable sorting is enabled, there will be an additional $id field """
    draggableTip: str = None
    """ "Can be reordered by dragging the [swap] button in each row" # Text to indicate draggable """
    subFormMode: str = None
    """ "normal" # Optional normal, horizontal, inline """
    placeholder: str = None
    """ "``" # Show when there is no member """
    canAccessSuperData: bool = False
    """ Specifies whether the data from the upper level can be automatically fetched and mapped to form items """
    conditions: dict = None
    """ Array of rendering types containing all conditions, test in a single array is the judgment condition, items in the array are the schema rendered when the condition is met """
    typeSwitchable: bool = False
    """ whether the condition is switchable, used with conditions """
    strictMode: bool = True
    """ Default is strict mode, when set to false, when other table items are updated, the table items inside can also be retrieved in time, otherwise it will not. """
    syncFields: List[str] = []
    """ Configure sync fields. Only valid if strictMode is false. """
  
    """ If the Combo is deeper, the bottom level may not be synchronized with the outer level. But configure this property for the combo to synchronize down. Input format: ["os"] """
    nullable: bool = False
    """ Allow nullable, if the validator is configured inside the child form item and it is in single entry mode. Can allow the user to choose to clear (not filled). """


class ConditionBuilder(FormItem):
    """Combined Condition"""

    class Field(MSAUINode):
        type: str = "text"
        """ configured as "text" in the field configuration """
        label: str = None
        """ Name of the field. """
        placeholder: str = None
        """ Placeholder """
        operators: list[str] = None
        """ Configure to override if you don't want that many. """
      
        """ Defaults to ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with'] """
        defaultOp: str = None
        """ default to "equal" """

    class Text(Field):
        """text"""

    class Number(Field):
        """number"""
        type: str = 'number'
        minimum: float = None
        """ minimum """
        maximum: float = None
        """ maximum value """
        step: float = None
        """ step length """

    class Date(Field):
        """date"""
        type: str = 'date'
        defaultValue: str = None
        """ default value """
        format: str = None
        """ default "YYYY-MM-DD" value format """
        inputFormat: str = None
        """ Default "YYYY-MM-DD" date format for display. """

    class Datetime(Date):
        """datetime"""
        type: str = 'datetime'
        timeFormat: str = None
        """ Default "HH:mm" time format, determines which input boxes are available. """

    class Time(Date):
        """time"""
        type: str = 'datetime'

    class Select(Field):
        """Dropdown selection"""
        type: str = 'select'
        options: MSAOptionsNode = None
        """ list of options, Array<{label: string, value: any}> """
        source: MSA_UI_API = None
        """ Dynamic options, please configure api. """
        searchable: bool = None
        """ If or not searchable """
        autoComplete: MSA_UI_API = None
        """ AutoComplete will be called after each new input, and will return updated options according to the interface. """

    type: str = 'condition-builder'
    fields: List[
        Field] = None
    """ is an array type, each member represents an optional field, supports multiple layers, configuration example """
    className: str = None
    """ outer dom class name """
    fieldClassName: str = None
    """ The class name of the input field """
    source: str = None
    """ pull configuration items via remote """

class Editor(FormItem):
    """Code Editor"""
    type: str = 'editor'
    language: str = None
    """ "javascript" # Language highlighted by the editor, supported by the ${xxx} variable bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java 
    javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,  pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml """
    size: str = None
    """ "md" # editor height, can be md, lg, xl, xxl """
    allowFullscreen: bool = None
    """ False # switch to show full screen mode or not """
    options: dict = None
    """ other configurations of monaco editor, such as whether to display line numbers, etc., please refer to here, but can not set readOnly, read-only mode need to use disabled: true """

class Markdown(MSAUINode):
    """Markdown rendering"""
    type: str = 'markdown'
    name: str = None
    """ Field name, specifying the key of the form item when it is submitted """
    value: Union[int, str] = None
    """ The value of the field """
    className: str = None
    """ The outermost class name of the form """
    src: MSA_UI_API = None
    """ External address """
    options: dict = None
    """ html, whether html tags are supported, default false; linkify, whether to automatically recognize links, default is true; breaks, whether carriage return is line feed, default false """

class InputFile(FormItem):
    """FileUpload"""
    type: str = 'input-file'
    receiver: MSA_UI_API = None
    """ Upload file interface """
    accept: str = None
    """ "text/plain" # Only plain text is supported by default, to support other types, please configure this attribute to have the file suffix .xxx """
    asBase64: bool = None
    """ False # Assign the file as base64 to the current component """
    asBlob: bool = None
    """ False # Assign the file to the current component in binary form """
    maxSize: int = None
    """ No limit by default, when set, files larger than this value will not be allowed to be uploaded. The unit is B """
    maxLength: int = None
    """ No limit by default, when set, only the specified number of files will be allowed to be uploaded at a time. """
    multiple: bool = None
    """ False # Whether to select multiple. """
    joinValues: bool = None
    """ True # Splice values """
    extractValue: bool = None
    """ False # Extract the value """
    delimiter: str = None
    """ "," # Splice character """
    autoUpload: bool = None
    """ True # Automatically start uploading after no selection """
    hideUploadButton: bool = None
    """ False # Hide the upload button """
    stateTextMap: dict = None
    """ Upload state text, Default: {init: '', pending: 'Waiting for upload', uploading: 'Uploading', error: 'Upload error', uploaded: 'Uploaded',ready: ''} """
    fileField: str = None
    """ "file" # You can ignore this attribute if you don't want to store it yourself. """
    nameField: str = None
    """ "name" # Which field the interface returns to identify the file name """
    valueField: str = None
    """ "value" # Which field is used to identify the value of the file """
    urlField: str = None
    """ "url" # The field name of the file download address. """
    btnLabel: str = None
    """ The text of the upload button """
    downloadUrl: Union[str, bool] = None
    """ Version 1.1.6 starts to support post:http://xxx.com/${value} this way,
    The default display of the file path will support direct download, you can support adding a prefix such as: http://xx.dom/filename= , if you do not want this, you can set the current configuration item to false. """
    useChunk: bool = None
    """ The server where msa_ui is hosted restricts the file upload size to 10M, so msa_ui will automatically change to chunk upload mode when the user selects a large file. """
    chunkSize: int = None
    """ 5 * 1024 * 1024 # chunk size """
    startChunkApi: MSA_UI_API = None
    """ startChunkApi """
    chunkApi: MSA_UI_API = None
    """ chunkApi """
    finishChunkApi: MSA_UI_API = None
    """ finishChunkApi """
    autoFill: Dict[
        str, str] = None
    """ After a successful upload, you can configure autoFill to populate a form item with the values returned by the upload interface (not supported under non-form for now) """

class InputExcel(FormItem):
    """Parse Excel"""
    type: str = 'input-excel'
    allSheets: bool = None
    """ False # whether to parse all sheets """
    parseMode: str = None
    """ 'array' or 'object' parse mode """
    includeEmpty: bool = None
    """ True # whether to include null values """
    plainText: bool = None
    """ True # Whether to parse as plain text """


class InputTable(FormItem):
    """table"""
    type: str = 'input-table'
    """ Specify as Table renderer """
    showIndex: bool = None
    """ False # Show serial number """
    perPage: int = None
    """ Set how many data to display on a page. 10 """
    addable: bool = None
    """ False # Whether to add a row """
    editable: bool = None
    """ False # Whether to edit """
    removable: bool = None
    """ False # Whether to remove """
    showAddBtn: bool = None
    """ True # Whether to show the add button """
    addApi: MSA_UI_API = None
    """ The MSA_UI_API to submit when adding """
    updateApi: MSA_UI_API = None
    """ The MSA_UI_API submitted when modifying """
    deleteApi: MSA_UI_API = None
    """ MSA_UI_API submitted when deleting """
    addBtnLabel: str = None
    """ Add button name """
    addBtnIcon: str = None
    """ "plus" # Add button icon """
    copyBtnLabel: str = None
    """ Copy button text """
    copyBtnIcon: str = None
    """ "copy" # Copy the button icon """
    editBtnLabel: str = None
    """ "" # Edit button name """
    editBtnIcon: str = None
    """ "pencil" # editBtnIcon """
    deleteBtnLabel: str = None
    """ "" # Delete the button name """
    deleteBtnIcon: str = None
    """ "minus" # Delete the button icon """
    confirmBtnLabel: str = None
    """ "" # Confirm edit button name """
    confirmBtnIcon: str = None
    """ "check" # Confirm edit button icon """
    cancelBtnLabel: str = None
    """ "" # Cancel the edit button name """
    cancelBtnIcon: str = None
    """ "times" # Cancel the edit button icon """
    needConfirm: bool = None
    """ True # whether to confirm the operation, can be used to control the interaction of the form """
    canAccessSuperData: bool = None
    """ False # Whether to access parent data, that is, the same level of data in the form, usually need to be used with strictMode """
    strictMode: bool = None
    """ True # For performance, the default value changes of other form items will not update the current form, sometimes you need to enable this in order to synchronize access to other form fields. """
    columns: list = None
    """ "[]" # Column information, columns[x].quickEdit: boolean|object = None # Used in conjunction with editable being true, 
    # columns[x].quickEditOnUpdate: boolean|object = None # can be used to distinguish between new mode and update mode editing configuration """


class InputGroup(FormItem):
    """InputBoxGroup"""
    type: str = 'input-group'
    className: str = None
    """ CSS class name """
    body: List[FormItem] = None
    """ collection of form items """


class Group(InputGroup):
    """Form Item Group"""
    type: str = 'group'
    mode: DisplayModeEnum = None
    """ Display default, same mode as in Form """
    gap: str = None
    """ spacing between form items, optional: xs, sm, normal """
    direction: str = None
    """ "horizontal" # You can configure whether to display horizontally or vertically. The corresponding configuration items are: vertical, horizontal """


class InputImage(FormItem):
    """Image Upload"""

    class CropInfo(MSABaseUIModel):
        aspectRatio: float = None
        """ Crop ratio. Floating point type, default 1 i.e. 1:1, if you want to set 16:9 please set 1.77777777777777 i.e. 16 / 9. """
        rotatable: bool = None
        """ False # If or not rotatable when cropping. """
        scalable: bool = None
        """ False # Whether to scale when cropping """
        viewMode: int = None
        """ 1 # View mode when cropping, 0 is no limit """

    class Limit(MSABaseUIModel):
        width: int = None
        """ Limit the width of the image. """
        height: int = None
        """ Limit the height of the image. """
        minWidth: int = None
        """ Limit the minimum width of the image. """
        minHeight: int = None
        """ Limit the minimum height of the image. """
        maxWidth: int = None
        """ Limit the maximum width of the image. """
        maxHeight: int = None
        """ Limit the maximum height of the image. """
        aspectRatio: float = None
        """ Limit the aspect ratio of the image, the format is floating point number, default 1 is 1:1. 
        If you want to set 16:9, please set 1.7777777777777777 i.e. 16 / 9. If you don't want to limit the ratio, please set the empty string. """

    type: str = 'input-image'
    receiver: MSA_UI_API = None
    """ Upload file interface """
    accept: str = None
    """ ".jpeg,.jpg,.png,.gif" # Supported image type formats, please configure this attribute as image suffix, e.g. .jpg, .png """
    maxSize: int = None
    """ No limit by default, when set, file size larger than this value will not be allowed to upload. The unit is B """
    maxLength: int = None
    """ No limit by default, when set, only the specified number of files will be allowed to be uploaded at once. """
    multiple: bool = None
    """ False # Whether to select multiple. """
    joinValues: bool = None
    """ True # Splice values """
    extractValue: bool = None
    """ False # Extract the value """
    delimiter: str = None
    """ "," # Splice character """
    autoUpload: bool = None
    """ True # Automatically start uploading after no selection """
    hideUploadButton: bool = None
    """ False # Hide the upload button """
    fileField: str = None
    """ "file" # You can ignore this property if you don't want to store it yourself. """
    crop: Union[bool, CropInfo] = None
    """ Used to set if crop is supported. """
    cropFormat: str = None
    """ "image/png" # Crop file format """
    cropQuality: int = None
    """ 1 # quality of the crop file format, for jpeg/webp, takes values between 0 and 1 """
    limit: Limit = None
    """ Limit the size of the image, won't allow uploads beyond that. """
    frameImage: str = None
    """ Default placeholder image address """
    fixedSize: bool = None
    """ Whether to enable fixed size, if so, set fixedSizeClassName at the same time """
    fixedSizeClassName: str = None
    """ When fixedSize is enabled, the display size is controlled by this value. """
  
    """ For example, if h-30, i.e., the height of the image box is h-30, msa_ui will automatically scale the width of the default image position, and the final uploaded image will be scaled according to this size. """
    autoFill: Dict[
        str, str] = None
    """ After successful upload, you can configure autoFill to fill the value returned by the upload interface into a form item (not supported under non-form) """


class LocationPicker(FormItem):
    """Location"""
    type: str = 'location-picker'
    vendor: str = 'baidu'
    """ map vendor, currently only implemented Baidu maps """
    ak: str = ...
    """ Baidu map ak # Register at: http://lbsyun.baidu.com/ """
    clearable: bool = None
    """ False # Whether the input box is clearable """
    placeholder: str = None
    """ "Please select a location" # Default prompt """
    coordinatesType: str = None
    """ "bd09" # Default is Baidu coordinates, can be set to 'gcj02' """


class InputNumber(FormItem):
    """Number input box"""
    type: str = 'input-number'
    min: Union[int, MSAUITemplate] = None
    """ min """
    max: Union[int, MSAUITemplate] = None
    """ max """
    step: int = None
    """ step size """
    precision: int = None
    """ precision, i.e., the number of decimal places """
    showSteps: bool = None
    """ True # Whether to show the up and down click buttons """
    prefix: str = None
    """ prefix """
    suffix: str = None
    """ suffix """
    kilobitSeparator: bool = None
    """ thousand separator """


class Picker(FormItem):
    """List Picker"""
    type: str = 'picker'
    """ List picker, similar in function to Select, but it can display more complex information. """
    size: Union[str, SizeEnum] = None
    """ Supports: xs, sm, md, lg, xl, full """
    options: MSAOptionsNode = None
    """ Options group """
    source: MSA_UI_API = None
    """ Dynamic options group """
    multiple: bool = None
    """ Whether to be multiple options. """
    delimiter: bool = None
    """ False # Splice character """
    labelField: str = None
    """ "label" # option label field """
    valueField: str = None
    """ "value" # Option value field """
    joinValues: bool = None
    """ True # splice values """
    extractValue: bool = None
    """ False # extract value """
    autoFill: dict = None
    """ AutoFill """
    modalMode: Literal["dialog", "drawer"] = None
    """ "dialog" # Set dialog or drawer to configure popup method. """
    pickerSchema: Union["CRUD", MSAUISchemaNode] = None
    """ "{mode: 'list', listItem: {title: '${label}'}}" i.e. rendering with List type to display list information. See CRUD for more configuration """
    embed: bool = None
    """ False # Whether to use inline mode """


class Switch(FormItem):
    """switch"""
    type: str = 'switch'
    option: str = None
    """ option description """
    onText: str = None
    """ Text when on """
    offText: str = None
    """ Text when off """
    trueValue: Any = None
    """ "True" # Identifies a true value """
    falseValue: Any = None
    """ "false" # Identifies a false value """


class Static(FormItem):
    """Static display/label"""
    type: str = 'static'
    """ support for displaying other non-form items by configuring the type as static-xxx component static-json|static-datetime """

    class Json(FormItem):
        type: str = 'static-json'
        value: Union[dict, str]

    class Datetime(FormItem):
        """Show date"""
        type: str = 'static-datetime'
        value: Union[int, str]
        """ support 10-bit timestamp: 1593327764 """


class InputText(FormItem):
    """input-box"""
    type: str = 'input-text'
    """ input-text|input-url|input-email|input-password|divider """
    options: Union[List[str], List[dict]] = None
    """ option group """
    source: Union[str, MSA_UI_API] = None
    """ dynamic options group """
    autoComplete: Union[str, MSA_UI_API] = None
    """ autoComplete """
    multiple: bool = None
    """ Whether to multi-select """
    delimiter: str = None
    """ Splice character "," """
    labelField: str = None
    """ option label field "label" """
    valueField: str = None
    """ option value field "value" """
    joinValues: bool = None
    """ True # Splice values """
    extractValue: bool = None
    """ extract value """
    addOn: MSAUISchemaNode = None
    """ Input box add-on, such as with a prompt text, or with a submit button. """
    trimContents: bool = None
    """ Whether to remove the first and last blank text. """
    creatable: bool = None
    """ If or not creatable, default is yes, unless set to false which means that only the value in the option can be selected. """
    clearable: bool = None
    """ Whether to clear or not """
    resetValue: str = None
    """ Set the value given by this configuration item after clearing. """
    prefix: str = None
    """ prefix """
    suffix: str = None
    """ suffix """
    showCounter: bool = None
    """ Whether to show the counter """
    minLength: int = None
    """ Limit the minimum number of words """
    maxLength: int = None
    """ Limit the maximum number of words """


class InputPassword(InputText):
    """Password input box"""
    type: str = 'input-password'


class InputRichText(FormItem):
    """rich-text editor"""
    type: str = 'input-rich-text'
    saveAsUbb: bool = None
    """ whether to save as ubb format """
    receiver: MSA_UI_API = None
    """ '' # default image save MSA_UI_API """
    videoReceiver: MSA_UI_API = None
    """ '' # Default video saving MSA_UI_API """
    size: str = None
    """ Size of the box, can be set to md or lg """
    options: dict = None
    """ Need to refer to tinymce or froala's documentation """
    buttons: list[
        str] = None
    """ froala specific, configure the buttons to be displayed, tinymce can set the toolbar string with the preceding options """
    vendor: str = None
    """ "vendor": "froala" , configured to use the froala editor """


class Select(FormItem):
    """dropdown box"""
    type: str = 'select'
    options: MSAOptionsNode = None
    """ options group """
    source: MSA_UI_API = None
    """ dynamic options group """
    autoComplete: MSA_UI_API = None
    """ auto prompt complement """
    delimiter: Union[bool, str] = None
    """ False # Splice character """
    labelField: str = None
    """ "label" # option label field """
    valueField: str = None
    """ "value" # option value field """
    joinValues: bool = None
    """ True # splice values """
    extractValue: bool = None
    """ False # extract value """
    checkAll: bool = None
    """ False # Whether to support select all """
    checkAllLabel: str = None
    """ "Select All" # Text to select all """
    checkAllBySearch: bool = None
    """ False # Only check all items that are hit when there is a search """
    defaultCheckAll: bool = None
    """ False # defaultCheckAll or not """
    creatable: bool = None
    """ False # Add option """
    multiple: bool = None
    """ False # Multi-select """
    searchable: bool = None
    """ False # Searchable """
    createBtnLabel: str = None
    """ "Add option" # Add option """
    addControls: List[FormItem] = None
    """ Customize the new form item """
    addApi: MSA_UI_API = None
    """ Configure the add options interface """
    editable: bool = None
    """ False # Edit options """
    editControls: List[FormItem] = None
    """ Customize edit form items """
    editApi: MSA_UI_API = None
    """ Configure the edit options interface """
    removable: bool = None
    """ False # Remove options """
    deleteApi: MSA_UI_API = None
    """ Configure the delete option interface """
    autoFill: dict = None
    """ AutoFill """
    menuTpl: str = None
    """ Support for configuring custom menus """
    clearable: bool = None
    """ Whether clearing is supported in radio mode """
    hideSelected: bool = None
    """ False # Hide the selected option """
    mobileClassName: str = None
    """ Mobile floating class name """
    selectMode: str = None
    """ Optional: group, table, tree, chained, associated, respectively: list form, table form, tree select form, tree select form
    cascade selection form, association selection form (the difference with cascade selection is that the cascade is infinite, while the association is only one level, the left side of the association can be a tree). """
    searchResultMode: str = None
    """ If not set, the value of selectMode will be used, can be configured separately, refer to selectMode, determine the display of search results. """
    columns: List[
        dict] = None
    """ When the display form is table can be used to configure which columns to display, similar to the columns in the table configuration, but only the display function. """
    leftOptions: List[dict] = None
    """ Used to configure the left set of options when the display is associated. """
    leftMode: str = None
    """ Configure the left option set when the display is associated, supports list or tree. default is list. rightMode: str = None # Configure the left option set when the display is associated. """
    rightMode: str = None
    """ Used to configure the right option set when the display is associated, optionally: list, table, tree, chained. """


class NestedSelect(Select):
    """Cascading selector"""
    type: str = 'nested-select'
    cascade: bool = None
    """ False # When set true, child nodes are not automatically selected when the parent node is selected. """
    withChildren: bool = None
    """ False # When set true, the value of the parent node will contain the value of the child node when selected, otherwise only the value of the parent node will be kept. """
    onlyChildren: bool = None
    """ False # When multi-select, when the parent node is selected, the value will include only its children in the value. """
    searchPromptText: str = None
    """ "Enter content to search" # Search box placeholder text """
    noResultsText: str = None
    """ "No results found" # Text when no results are found """
    hideNodePathLabel: bool = None
    """ False # Whether to hide the path of the selected node in the selection box label information """
    onlyLeaf: bool = None
    """ False # Only allow leaf nodes to be selected """


class Textarea(FormItem):
    """Multi-line text input box"""
    type: str = 'textarea'
    minRows: int = None
    """ minimum number of rows """
    maxRows: int = None
    """ maximum number of lines """
    trimContents: bool = None
    """ whether to remove first and last blank text """
    readOnly: bool = None
    """ whether to read only """
    showCounter: bool = True
    """ Whether to show the counter """
    minLength: int = None
    """ Limit the minimum number of words """
    maxLength: int = None
    """ Limit the maximum number of words """


class InputMonth(FormItem):
    """month"""
    type: str = 'input-month'
    value: str = None
    """ Default value """
    format: str = None
    """ "X" # month selector value format, see moment for more format types """
    inputFormat: str = None
    """ "YYYY-MM" # Month selector display format, i.e. timestamp format, see moment for more format types """
    placeholder: str = None
    """ "Please select a month" # Placeholder text """
    clearable: bool = None
    """ True # clearable or not """


class InputTime(FormItem):
    """time"""
    type: str = 'input-time'
    value: str = None
    """ Default value """
    timeFormat: str = None
    """ "HH:mm" # time selector value format, see moment for more format types """
    format: str = None
    """ "X" # Time picker value format, see moment for more format types """
    inputFormat: str = None
    """ "HH:mm" # Time picker display format, i.e. timestamp format, see moment for more format types """
    placeholder: str = None
    """ "Please select time" # Placeholder text """
    clearable: bool = None
    """ True # clearable or not """
    timeConstraints: dict = None
    """ True # See also: react-datetime """


class InputDatetime(FormItem):
    """date"""
    type: str = 'input-datetime'
    value: str = None
    """ Default value """
    format: str = None
    """ "X" # Date time selector value format, see documentation for more format types """
    inputFormat: str = None
    """ "YYYY-MM-DD HH:mm:ss" # Date and time picker display format, i.e. timestamp format, see documentation for more format types """
    placeholder: str = None
    """ "Please select the date and time" # Placeholder text """
    shortcuts: str = None
    """ Date and time shortcuts """
    minDate: str = None
    """ Limit the minimum date and time """
    maxDate: str = None
    """ Limit the maximum date and time """
    utc: bool = None
    """ False # Save utc value """
    clearable: bool = None
    """ True # clearable or not """
    embed: bool = None
    """ False # Whether to inline """
    timeConstraints: dict = None
    """ True # See also: react-datetime """


class InputDate(FormItem):
    """date"""
    type: str = 'input-date'
    value: str = None
    """ Default value """
    format: str = None
    """ "X" # Date picker value format, see documentation for more format types """
    inputFormat: str = None
    """ "YYYY-DD-MM" # Date picker display format, i.e. timestamp format, see documentation for more format types """
    placeholder: str = None
    """ "Please select a date" # Placeholder text """
    shortcuts: str = None
    """ Date shortcuts """
    minDate: str = None
    """ Restrict the minimum date """
    maxDate: str = None
    """ Limit the maximum date """
    utc: bool = None
    """ False # Save utc value """
    clearable: bool = None
    """ True # clearable or not """
    embed: bool = None
    """ False # Whether to inline mode """
    timeConstraints: dict = None
    """ True # See also: react-datetime """
    closeOnSelect: bool = None
    """ False # Whether to close the selection box immediately after tapping a date """
    schedules: Union[
        list, str] = None
    """ Show schedules in calendar, can set static data or take data from context, className reference background color """
    scheduleClassNames: List[str] = None
    """ "['bg-warning','bg-danger','bg-success','bg-info','bg-secondary']" """
  
    """ The color to display the schedule in the calendar, referencing the background color """
    scheduleAction: MSAUISchemaNode = None
    """ Custom schedule display """
    largeMode: bool = None
    """ False # Zoom mode """


class InputTimeRange(FormItem):
    """TimeRange"""
    type: str = 'input-time-range'
    timeFormat: str = None
    """ "HH:mm" # time range selector value format """
    format: str = None
    """ "HH:mm" # time range selector value format """
    inputFormat: str = None
    """ "HH:mm" # Time range selector display format """
    placeholder: str = None
    """ "Please select a time range" # Placeholder text """
    clearable: bool = None
    """ True # clearable or not """
    embed: bool = None
    """ False # Whether inline mode """


class InputDatetimeRange(InputTimeRange):
    """DateTimeRange"""
    type: str = 'input-datetime-range'
    ranges: Union[
        str, List[str]] = None
    """ "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter" Date range shortcut. 
        optional: today,yesterday,1dayago,7daysago,30daysago,90daysago,prevweek,thismonth,thisquarter,prevmonth,prevquarter """
    minDate: str = None
    """ Limit the minimum date and time, use the same as limit range """
    maxDate: str = None
    """ Limit the maximum date and time, use the same as limit range """
    utc: bool = None
    """ False # Save UTC value """


class InputDateRange(InputDatetimeRange):
    """dateRange"""
    type: str = 'input-date-range'
    minDuration: str = None
    """ Limit the minimum span, e.g. 2days """
    maxDuration: str = None
    """ Limit the maximum span, e.g. 1year """


class InputMonthRange(InputDateRange):
    """MonthRange"""
    type: str = 'input-month-range'


class Transfer(FormItem):
    """shuttle"""
    type: Literal['transfer', 'transfer-picker', 'tabs-transfer', 'tabs-transfer-picker'] = 'transfer'
    options: MSAOptionsNode = None
    """ options group """
    source: MSA_UI_API = None
    """ dynamic options group """
    delimiter: str = None
    """ "False" # Splice character """
    joinValues: bool = None
    """ True # Splice values """
    extractValue: bool = None
    """ False # extract value """
    searchable: bool = None
    """ False # When set to true means that options can be retrieved by partial input. """
    searchApi: MSA_UI_API = None
    """ You can set an api if you want to search through the interface. """
    statistics: bool = None
    """ True # Whether to display statistics """
    selectTitle: str = None
    """ "Please select" # The title text on the left side """
    resultTitle: str = None
    """ "Current selection" # The title text of the right result """
    sortable: bool = None
    """ False # Results can be sorted by dragging and dropping """
    selectMode: str = None
    """ "list" # Optional: list, table, tree, cascaded, associated. respectively: list form, table form, tree selection form, tree selection form 
    cascade selection form, associated selection form (the difference with cascade selection is that cascade is infinite, while associated is only one level, and the left side of associated can be a tree). """
    searchResultMode: str = None
    """ If not set will use the value of selectMode, can be configured separately, refer to selectMode, determine the search results display form. """
    columns: List[
        dict] = None
    """ When the display form is table can be used to configure which columns to display, similar to the columns in the table configuration, but only the display function. """
    leftOptions: List[dict] = None
    """ Used to configure the left set of options when the display is associated. """
    leftMode: str = None
    """ Configure the left option set when the display is associated, supports list or tree. default is list. rightMode: str = None # Configure the left option set when the display is associated. """
    rightMode: str = None
    """ Use to configure the right option set when the display is associated, options are: list, table, tree, chained. """
    menuTpl: MSAUISchemaNode = None
    """ Used to customize the option display. """
    valueTpl: MSAUISchemaNode = None
    """ Used to customize the display of values """


class TransferPicker(Transfer):
    """shuttlePicker"""
    type: str = 'transfer-picker'


class TabsTransfer(Transfer):
    """Combination shuttle"""
    type: str = 'tabs-transfer'


class TabsTransferPicker(Transfer):
    """Combination shuttle selector"""
    type: str = 'tabs-transfer-picker'


class InputTree(FormItem):
    """tree selector box"""
    type: str = 'input-tree'
    options: MSAOptionsNode = None
    """ options group """
    source: MSA_UI_API = None
    """ dynamic options group """
    autoComplete: MSA_UI_API = None
    """ auto prompt complement """
    multiple: bool = None
    """ False # Whether to multiple select """
    delimiter: str = None
    """ "False" # Splice character """
    labelField: str = None
    """ "label" # option label field """
    valueField: str = None
    """ "value" # option value field """
    iconField: str = None
    """ "icon" # Icon value field """
    joinValues: bool = None
    """ True # join values """
    extractValue: bool = None
    """ False # extract value """
    creatable: bool = None
    """ False # Add options """
    addControls: List[FormItem] = None
    """ Customize the new form items """
    addApi: MSA_UI_API = None
    """ Configure the add options interface """
    editable: bool = None
    """ False # Edit options """
    editControls: List[FormItem] = None
    """ Customize edit form items """
    editApi: MSA_UI_API = None
    """ Configure the edit options interface """
    removable: bool = None
    """ False # Remove options """
    deleteApi: MSA_UI_API = None
    """ Configure the delete option interface """
    searchable: bool = None
    """ False # Searchable or not, only works if type is tree-select """
    hideRoot: bool = None
    """ True # If you want to show a top node, set to false """
    rootLabel: bool = None
    """ "top" # Useful when hideRoot is not false, to set the text of the top node. """
    showIcon: bool = None
    """ True # Whether to show the icon """
    showRadio: bool = None
    """ False # Whether to show radio buttons, multiple is valid when false. """
    initiallyOpen: bool = None
    """ True # Set whether to expand all levels by default. """
    unfoldedLevel: int = None
    """ 0 # Set the number of levels to be expanded by default, only effective if initiallyOpen is not true. """
    cascade: bool = None
    """ False # Do not automatically select children when parent is selected. """
    withChildren: bool = None
    """ False # When the parent node is selected, the value will contain the value of the child node, otherwise only the value of the parent node will be kept. """
    onlyChildren: bool = None
    """ False # Whether to add only its children to the value when the parent node is selected in multiple selection. """
    rootCreatable: bool = None
    """ False # Whether top-level nodes can be created """
    rootCreateTip: str = None
    """ "Add first-level node" # Hover tip for creating top-level nodes """
    minLength: int = None
    """ Minimum number of selected nodes """
    maxLength: int = None
    """ Maximum number of nodes to select """
    treeContainerClassName: str = None
    """ tree outermost container class name """
    enableNodePath: bool = None
    """ False # Whether to enable node path mode """
    pathSeparator: str = None
    """ "/" # Separator for node paths, takes effect when enableNodePath is true """
    deferApi: MSA_UI_API = None
    """ For lazy loading, please configure defer to true, then configure deferApi to complete lazy loading """
    selectFirst: bool = None


class TreeSelect(InputTree):
    """Tree Selector"""
    type: str = 'tree-select'
    hideNodePathLabel: bool = None
    """ Whether to hide the path of the selected node in the selection box label information """


class Image(MSAUINode):
    """image"""
    type: str = 'image'
    """ "image" if in Table, Card and List; "static-image" if used as a static display in Form """
    className: str = None
    """ Outer CSS class name """
    imageClassName: str = None
    """ Image CSS class name """
    thumbClassName: str = None
    """ Image thumbnail CSS class name """
    height: int = None
    """ Image thumbnail height """
    width: int = None
    """ Image scaling width """
    title: str = None
    """ title """
    imageCaption: str = None
    """ description """
    placeholder: str = None
    """ Placeholder text """
    defaultImage: str = None
    """ Image to display when no data is available """
    src: str = None
    """ Thumbnail address """
    href: MSAUITemplate = None
    """ External link address """
    originalSrc: str = None
    """ Original image address """
    enlargeAble: bool = None
    """ Support for enlarge preview """
    enlargeTitle: str = None
    """ The title of the enlarged preview """
    enlargeCaption: str = None
    """ Description of the enlarged preview """
    thumbMode: str = None
    """ "contain" # Preview mode, optional: 'w-full', 'h-full', 'contain', 'cover' """
    thumbRatio: str = None
    """ "1:1" # The ratio of the preview image, optional: '1:1', '4:3', '16:9' """
    imageMode: str = None
    """ "thumb" # Image display mode, optional: 'thumb', 'original' i.e.: thumbnail mode or original image mode """


class Images(MSAUINode):
    """images collection"""
    type: str = "images"
    """ "images" if in Table, Card and List; "static-images" if used as a static display in Form """
    className: str = None
    """ Outer CSS class name """
    defaultImage: str = None
    """ Default image to display """
    value: Union[str, List[str], List[dict]] = None
    """ array of images """
    source: str = None
    """ data source """
    delimiter: str = None
    """ "," # separator to split when value is a string """
    src: str = None
    """ Address of the preview image, supports data mapping to get the image variables in the object """
    originalSrc: str = None
    """ The address of the original image, supports data mapping to get the image variables in the object """
    enlargeAble: bool = None
    """ Support enlarge preview """
    thumbMode: str = None
    """ "contain" # preview image mode, optional: 'w-full', 'h-full', 'contain', 'cover' """
    thumbRatio: str = None
    """ "1:1" # Preview ratio, optional: '1:1', '4:3', '16:9' """


class Carousel(MSAUINode):
    """Rotating image"""

    class Item(MSAUINode):
        image: str = None
        """ Image link """
        href: str = None
        """ link to the image's open URL """
        imageClassName: str = None
        """ Image class name """
        title: str = None
        """ Image title """
        titleClassName: str = None
        """ Image title class name """
        description: str = None
        """ Image description """
        descriptionClassName: str = None
        """ Image description class name """
        html: str = None
        """ HTML customization, same as Tpl """

    type: str = "carousel"
    """ Specify as Carousel renderer """
    className: str = None
    """ "panel-default" # class name of outer Dom """
    options: List[Item] = None
    """ "[]" # Rotating panel data """
    itemSchema: dict = None
    """ Custom schema to display data """
    auto: bool = True
    """ whether to rotate automatically """
    interval: str = None
    """ "5s" # toggle animation interval """
    duration: str = None
    """ "0.5s" # the duration of the toggle animation """
    width: str = None
    """ "auto" # width """
    height: str = None
    """ "200px" # height """
    controls: list[str] = None
    """ "['dots','arrows']" # Show left and right arrows, bottom dots index """
    controlsTheme: str = None
    """ "light" # Color of left and right arrows, bottom dot index, default light, dark mode available """
    animation: str = None
    """ "fade" # Toggle animation effect, default fade, also slide mode """
    thumbMode: str = None
    """ "cover"|"contain" # default image zoom mode """


class CRUD(MSAUINode):
    """add-delete"""

    class Messages(MSAUINode):
        fetchFailed: str = None
        """ prompt when fetch fails """
        saveOrderFailed: str = None
        """ Hint for failed save order """
        saveOrderSuccess: str = None
        """ prompt for order success """
        quickSaveFailed: str = None
        """ prompt for quick save failure """
        quickSaveSuccess: str = None
        """ QuickSaveSuccess hint """

    type: str = "crud"
    """ type specifies the CRUD renderer """
    mode: str = None
    """ "table" # "table", "cards" or "list" """
    title: str = None
    """ "" # can be set to empty, when set to empty, there is no title bar """
    className: str = None
    """ class name of the table's outer Dom """
    api: MSA_UI_API = None
    """ The api used by CRUD to get the list data. """
    loadDataOnce: bool = None
    """ Whether to load all data at once (front-end paging) """
    loadDataOnceFetchOnFilter: bool = None
    """ True # Whether to re-request the api when filtering when loadDataOnce is enabled """
    source: str = None
    """ Data mapping interface to return the value of a field, not set will default to use the interface to return ${items} or ${rows}, can also be set to the content of the upper-level data source """
    filter: Union[
        MSAUISchemaNode, Form] = None
    """ Set a filter that will bring the data to the current mode to refresh the list when the form is submitted. """
    filterTogglable: bool = None
    """ False # Whether to make the filter visible or invisible """
    filterDefaultVisible: bool = None
    """ True # Sets whether the filter is visible by default. """
    initFetch: bool = None
    """ True # Whether to pull data when initializing, only for cases with filter, no filter will pull data initially """
    interval: int = None
    """ Refresh time (minimum 1000) """
    silentPolling: bool = None
    """ Configure whether to hide loading animation when refreshing """
    stopAutoRefreshWhen: str = None
    """ Configure the conditions for stopping the refresh via an expression """
    stopAutoRefreshWhenModalIsOpen: bool = None
    """ Turn off auto refresh when there is a popup box, and resume when the popup box is closed """
    syncLocation: bool = None
    """ False # Whether to sync the parameters of the filter condition to the address bar, !!! !!! may change the data type after turning on, can't pass fastpi data verification """
    draggable: bool = None
    """ Whether to sort by drag and drop """
    itemDraggableOn: bool = None
    """ Use an expression to configure whether draggable is sortable or not """
    saveOrderApi: MSA_UI_API = None
    """ The api to save the sorting. """
    quickSaveApi: MSA_UI_API = None
    """ The MSA_UI_API used for batch saving after quick editing. """
    quickSaveItemApi: MSA_UI_API = None
    """ The MSA_UI_API used when the quick edit is configured to save in time. """
    bulkActions: List[Action] = None
    """ List of bulk actions, configured so that the form can be checked. """
    defaultChecked: bool = None
    """ Default whether to check all when bulk actions are available. """
    messages: Messages = None
    """ Override the message prompt, if not specified, the message returned by the api will be used """
    primaryField: str = None
    """ Set the ID field name.' id' """
    perPage: int = None
    """ Set how many data to display on a page. 10 """
    defaultParams: dict = None
    """ Set the default filter default parameters, which will be sent to the backend together with the query """
    pageField: str = None
    """ Set the pagination page number field name. "page" """
    perPageField: str = None
    """ "perPage" # Set the field name of how many data to display on a paginated page. Note: Best used in conjunction with defaultParams, see the following example. """
    perPageAvailable: List[
        int] = None
    """ [5, 10, 20, 50, 100] # Set how many data dropdown boxes are available for displaying on a page. """
    orderField: str = None
    """ Set the name of the field used to determine the position, after setting the new order will be assigned to the field. """
    hideQuickSaveBtn: bool = None
    """ Hide the top quick save prompt """
    autoJumpToTopOnPagerChange: bool = None
    """ Whether to auto jump to the top when the page is cut. """
    syncResponse2Query: bool = None
    """ True # Sync the return data to the filter. """
    keepItemSelectionOnPageChange: bool = None
    """ True """
  
    """ Keep item selection. By default, after paging and searching, user-selected items will be cleared. Turning on this option will keep user selection, allowing cross-page batch operations. """
    labelTpl: str = None
    """ Single description template, keepItemSelectionOnPageChange """
  
    """ When set to true, all selected items will be listed, this option can be used to customize the item display text. """
    headerToolbar: list = None
    """ ['bulkActions','pagination'] # top toolbar configuration """
    footerToolbar: list = None
    """ ['statistics','pagination'] # Bottom toolbar configuration """
    alwaysShowPagination: bool = None
    """ whether to always show pagination """
    affixHeader: bool = None
    """ True # Whether to fix the table header (under table) """
    autoGenerateFilter: bool = None
    """ Whether to enable the query area, which will automatically generate a query form based on the value of the searchable property of the column element """
    itemAction: Action = None
    """ Implement a custom action when a row is clicked, supports all configurations in action, such as pop-up boxes, refreshing other components, etc. """


class TableColumn(MSAUINode):
    """columnConfiguration"""
    type: str = None
    """ Literal['text','audio','image','link','tpl','mapping','carousel','date', 'progress','status','switch','list','json','operation'] """
    label: MSAUITemplate = None
    """ the text content of the table header """
    name: str = None
    """ Data associated by name """
    tpl: MSAUITemplate = None
    """ Template """
    fixed: str = None
    """ Whether to fix the front row left|right|none """
    popOver: Union[bool, dict] = None
    """ popup box """
    quickEdit: Union[bool, dict] = None
    """ QuickEdit """
    copyable: Union[bool, dict] = None
    """ whether copyable boolean or {icon: string, content:string} """
    sortable: bool = None
    """ False # Whether to sort """
    searchable: Union[bool, MSAUISchemaNode] = None
    """ False # Whether to search quickly boolean|Schema """
    width: Union[str, int] = None
    """ Column width """
    remark: Remark = None
    """ Prompt message"""
    breakpoint: str = None
    """ *,ls"""


class ColumnOperation(TableColumn):
    """operationColumn"""
    type: str = 'operation'
    label: MSAUITemplate = None
    """ "operation" """
    toggled: bool = None
    """ True"""
    buttons: List[Union[Action, MSAUINode]] = None


class ColumnImage(Image, TableColumn):
    """Image Column"""
    pass


class ColumnImages(Images, TableColumn):
    """Image collection Column"""
    pass


class Table(MSAUINode):
    """table"""

    type: str = "table"
    """ Specify as table renderer"""
    title: str = None
    """ title"""
    source: str = None
    """ "${items}" # data source, bound to the current environment variable"""
    affixHeader: bool = None
    """ True # Whether to fix the table header"""
    columnsTogglable: Union[
        str, bool] = None
    """ "auto" # Show column display switch, auto i.e.: automatically on when the number of columns is greater than or equal to 5"""
    placeholder: str = None
    """ "No data yet" # Text alert when there is no data"""
    className: str = None
    """ "panel-default" # Outer CSS class name"""
    tableClassName: str = None
    """ "table-db table-striped" # Table CSS class name"""
    headerClassName: str = None
    """ "Action.md-table-header" # top outer CSS class name"""
    footerClassName: str = None
    """ "Action.md-table-footer" # bottom outer CSS class name"""
    toolbarClassName: str = None
    """ "Action.md-table-toolbar" # Toolbar CSS class name"""
    columns: List[Union[TableColumn, MSAUISchemaNode]] = None
    """ Used to set column information"""
    combineNum: int = None
    """ Automatically merge cells"""
    itemActions: List[Action] = None
    """ Hover row action button group"""
    itemCheckableOn: MSAUIExpression = None
    """ condition to configure whether the current row is checkable, use expression"""
    itemDraggableOn: MSAUIExpression = None
    """ condition to configure whether the current row is draggable or not, use the expression"""
    checkOnItemClick: bool = None
    """ False # Whether the current row can be checked by clicking on the data row"""
    rowClassName: str = None
    """ Add a CSS class name to the row"""
    rowClassNameExpr: MSAUITemplate = None
    """ Add a CSS class name to the row via a template"""
    prefixRow: list = None
    """ Top summary row"""
    affixRow: list = None
    """ Bottom summary row"""
    itemBadge: "Badge" = None
    """ Row corner configuration"""
    autoFillHeight: bool = None
    """ Content area adaptive height"""
    footable: Union[
        bool, dict] = None
    """ When there are too many columns, there is no way to display all the content, so you can let some of the information displayed at the bottom, which allows users to expand to see the details.
    The configuration is very simple, just turn on the footable property and add a breakpoint property to * for the columns you want to display at the bottom."""


class Chart(MSAUINode):
    """chart: https://echarts.apache.org/zh/option.html#title"""
    type: str = "chart"
    """ Specify as chart renderer"""
    className: str = None
    """ class name of the outer Dom"""
    body: MSAUISchemaNode = None
    """ Content container"""
    api: MSA_UI_API = None
    """ Configuration item interface address"""
    source: dict = None
    """ Get the value of a variable in the data chain as a configuration via data mapping"""
    initFetch: bool = None
    """ Whether to request the interface when the component is initialized"""
    interval: int = None
    """ Refresh time (min 1000)"""
    config: Union[
        dict, str] = None
    """ Set the configuration of eschars, when it is string, you can set function and other configuration items"""
    style: dict = None
    """ Set the style of the root element"""
    width: str = None
    """ Set the width of the root element"""
    height: str = None
    """ Set the height of the root element"""
    replaceChartOption: bool = None
    """ False # Does each update completely override the configuration item or append it?"""
    trackExpression: str = None
    """ Update the chart when the value of this expression has changed"""


class Code(MSAUINode):
    """Code highlighting"""
    type: str = "code"
    className: str = None
    """ Outer CSS class name """
    value: str = None
    """ The value of the displayed color"""
    name: str = None
    """ Used as a variable mapping when in other components"""
    language: str = None
    """ The highlighting language used, default is plaintext"""
    tabSize: int = None
    """ 4 # Default tab size"""
    editorTheme: str = None
    """ "'vs'" # theme, and 'vs-dark'"""
    wordWrap: str = None
    """ "True" # whether to wrap the line"""


class Json(MSAUINode):
    """JSON display component"""
    type: str = "json"
    """ "json" if in Table, Card and List; "static-json" if used as a static display in Form"""
    className: str = None
    """ Outer CSS class name"""
    value: Union[dict, str] = None
    """ json value, parse automatically if it is a string"""
    source: str = None
    """ Get the value in the data chain by data mapping"""
    placeholder: str = None
    """ Placeholder text"""
    levelExpand: int = None
    """ 1 # Default level of expansion"""
    jsonTheme: str = None
    """ "twilight" # theme, optional twilight and eighties"""
    mutable: bool = None
    """ False # whether to modify"""
    displayDataTypes: bool = None
    """ False # Whether to display data types"""


class Link(MSAUINode):
    """link"""
    type: str = "link"
    """ "link" if in Table, Card and List; "static-link" if used as a static display in Form"""
    body: str = None
    """ text inside the tag"""
    href: str = None
    """ Link address"""
    blank: bool = None
    """ whether to open in a new tab"""
    htmlTarget: str = None
    """ target of a tag, takes precedence over the blank attribute"""
    title: str = None
    """ the title of a tag"""
    disabled: bool = None
    """ Disable hyperlinks"""
    icon: str = None
    """ hyperlink icon to enhance display"""
    rightIcon: str = None
    """ right icon"""


class Log(MSAUINode):
    """LiveLog"""
    type: str = "log"
    source: MSA_UI_API = None
    """ support variable, can be initially set to null, so that it will not be loaded initially, but will be loaded when the variable has a value"""
    height: int = None
    """ 500 # height of display area"""
    className: str = None
    """ Outer CSS class name"""
    autoScroll: bool = None
    """ True # whether to auto-scroll"""
    placeholder: str = None
    """ Text in load"""
    encoding: str = None
    """ "utf-8" # Returns the character encoding of the content"""


class Mapping(MSAUINode):
    """mapping"""
    type: str = "mapping"
    """ "mapping" if in Table, Card and List; "static-mapping" if used as a static display in Form"""
    className: str = None
    """ Outer CSS class name"""
    placeholder: str = None
    """ Placeholder text"""
    map: dict = None
    """ Mapping configuration"""
    source: MSA_UI_API = None
    """ MSA_UI_API or data mapping"""


class Property(MSAUINode):
    """Property table"""

    class Item(MSAUINode):
        label: MSAUITemplate = None
        """ property name"""
        content: MSAUITemplate = None
        """ attribute value"""
        span: int = None
        """ attribute value across several columns"""
        visibleOn: MSAUIExpression = None
        """ Show expressions"""
        hiddenOn: MSAUIExpression = None
        """ Hide the expression"""

    type: str = 'property'
    className: str = None
    """ the class name of the outer dom"""
    style: dict = None
    """ The style of the outer dom"""
    labelStyle: dict = None
    """ Style of the property name"""
    contentStyle: dict = None
    """ The style of the property value"""
    column: int = None
    """ 3 # how many columns per row"""
    mode: str = None
    """ 'table' # display mode, currently only 'table' and 'simple'"""
    separator: str = None
    """ ',' # separator between attribute name and value in 'simple' mode"""
    source: MSAUITemplate = None
    """ Data source"""
    title: str = None
    """ title"""
    items: List[Item] = None
    """ data items"""


class QRCode(MSAUINode):
    """QR Code"""
    type: str = "qr-code"
    """ Specified as a QRCode renderer"""
    value: MSAUITemplate
    """ The text to be displayed after scanning the QR code, to display a page enter the full url ("http://..." or "https://..." ), supports the use of templates"""
    className: str = None
    """ Class name of the outer Dom"""
    qrcodeClassName: str = None
    """ class name of the QR code SVG"""
    codeSize: int = None
    """ 128 # The width and height of the QR code"""
    backgroundColor: str = None
    """ "#fff" # QR code background color"""
    foregroundColor: str = None
    """ "#000" # The foreground color of the QR code"""
    level: str = None
    """ "L" # QR code complexity level, there are four ('L' 'M' 'Q' 'H')"""


class Video(MSAUINode):
    """video"""
    type: str = "video"
    """ Specify as video renderer"""
    className: str = None
    """ class name of the outer Dom"""
    src: str = None
    """ video address"""
    isLive: bool = None
    """ False # whether it is live, need to add on when the video is live, supports flv and hls formats"""
    videoType: str = None
    """ Specify the format of the live video"""
    poster: str = None
    """ video cover address"""
    muted: bool = None
    """ whether to mute"""
    autoPlay: bool = None
    """ Whether to auto play"""
    rates: List[float] = None
    """ multiplier in the format [1.0, 1.5, 2.0]"""


class Alert(MSAUINode):
    """alert"""
    type: str = "alert"
    """ Specify as alert renderer"""
    className: str = None
    """ class name of the outer Dom"""
    level: str = None
    """ "info" # level, can be: info, success, warning or danger"""
    body: MSAUISchemaNode = None
    """ Display content"""
    showCloseButton: bool = None
    """ False # whether to show the close button"""
    closeButtonClassName: str = None
    """ CSS class name of the close button"""
    showIcon: bool = None
    """ False # Whether to show icon"""
    icon: str = None
    """ Custom icon"""
    iconClassName: str = None
    """ CSS class name of the icon"""


class Dialog(MSAUINode):
    """Dialog"""
    type: str = "dialog"
    """ Specify as Dialog renderer"""
    title: MSAUISchemaNode = None
    """ popup layer title"""
    body: MSAUISchemaNode = None
    """ Add content to the Dialog content area"""
    size: Union[str, SizeEnum] = None
    """ Specify dialog size, supports: xs, sm, md, lg, xl, full"""
    bodyClassName: str = None
    """ "modal-body" # The style class name of the Dialog body area"""
    closeOnEsc: bool = None
    """ False # Whether to close the Dialog by pressing Esc"""
    showCloseButton: bool = None
    """ True # Whether to show the close button in the upper right corner"""
    showErrorMsg: bool = None
    """ True # Whether to show the error message in the lower left corner of the popup box"""
    disabled: bool = None
    """ False # If this property is set, the Dialog is read only and no action is submitted."""
    actions: List[
        Action] = None
    """ If you want to not show the bottom button, you can configure: [] "[Confirm] and [Cancel]" """
    data: dict = None
    """ Support data mapping, if not set will default to inherit data from the context of the trigger button."""


class Drawer(MSAUINode):
    """drawer"""
    type: str = "drawer"
    """ "drawer" is specified as the Drawer renderer"""
    title: MSAUISchemaNode = None
    """ popup layer title"""
    body: MSAUISchemaNode = None
    """ Add content to the Drawer content area"""
    size: Union[str, SizeEnum] = None
    """ Specify Drawer size, supports: xs, sm, md, lg"""
    position: str = None
    """ 'left' # Position"""
    bodyClassName: str = None
    """ "modal-body" # The style class name of the Drawer body area"""
    closeOnEsc: bool = None
    """ False # Whether or not to support closing the Drawer by pressing Esc"""
    closeOnOutside: bool = None
    """ False # Whether to close the Drawer by clicking outside the content area"""
    overlay: bool = None
    """ True # Whether or not to show the mask"""
    resizable: bool = None
    """ False # Whether the Drawer size can be changed by dragging and dropping"""
    actions: List[Action] = None
    """ Can be set without, only two buttons by default. "[Confirm] and [Cancel]" """
    data: dict = None
    """ Support data mapping, if not set will default to inherit data from the context of the trigger button."""


class Iframe(MSAUINode):
    """Iframe"""
    type: str = "iframe"
    """ Specify as iFrame renderer"""
    className: str = None
    """ The class name of the iFrame"""
    frameBorder: list = None
    """ frameBorder"""
    style: dict = None
    """ Style object"""
    src: str = None
    """ iframe address"""
    height: Union[int, str] = None
    """ "100%" # iframe height"""
    width: Union[int, str] = None
    """ "100%" # iframe width"""


class Spinner(MSAUINode):
    """loading"""
    type: str = "spinner"


class TableCRUD(CRUD, Table):
    """TableCRUD"""


class Avatar(MSAUINode):
    """Avatar"""
    type: str = "avatar"
    className: str = None
    """ class name of the outer dom"""
    fit: str = None
    """ "cover" # image scaling type"""
    src: str = None
    """ Image address"""
    text: str = None
    """ Text"""
    icon: str = None
    """ Icon"""
    shape: str = None
    """ "circle" # The shape, which can also be square"""
    size: int = None
    """ 40 # size"""
    style: dict = None
    """ The style of the outer dom"""


class Audio(MSAUINode):
    """audio"""
    type: str = "audio"
    """ Specify as audio renderer"""
    className: str = None
    """ the class name of the outer Dom"""
    inline: bool = None
    """ True # whether inline mode is used"""
    src: str = None
    """ Audio address"""
    loop: bool = None
    """ False # Whether to loop"""
    autoPlay: bool = None
    """ False # Whether to play automatically"""
    rates: List[float] = None
    """ "[]" # Configurable audio playback multiplier e.g. [1.0, 1.5, 2.0]"""
    controls: List[str] = None
    """ "['rates','play','time','process','volume']" # Internal module customization"""


class Status(MSAUINode):
    """status"""
    type: str = "status"
    """ Specify as Status renderer"""
    className: str = None
    """ class name of the outer Dom"""
    placeholder: str = None
    """ Placeholder text"""
    map: dict = None
    """ Mapping icon"""
    labelMap: dict = None
    """ Mapping text"""


class Tasks(MSAUINode):
    """A collection of task actions"""
    class Item(MSAUINode):
        label: str = None
        """ Task name"""
        key: str = None
        """ Task key value, please distinguish it uniquely"""
        remark: str = None
        """ Current task status, supports html"""
        status: str = None
        """ Task status: 0: initial, inoperable. 1: ready, operable. 2: in progress, not yet finished. 3: with errors, not retryable. 4: has ended normally. 5: with errors, and retryable."""

    type: str = "tasks"
    """ Specify as Tasks renderer"""
    className: str = None
    """ Class name of the outer Dom"""
    tableClassName: str = None
    """ Class name of the table Dom"""
    items: List[Item] = None
    """ List of tasks"""
    checkApi: MSA_UI_API = None
    """ Return a list of tasks, see items for the returned data."""
    submitApi: MSA_UI_API = None
    """ The MSA_UI_API used to submit the task"""
    reSubmitApi: MSA_UI_API = None
    """ This MSA_UI_API is used when submitting if the task fails and can be retried"""
    interval: int = None
    """ 3000 # When there is a task in progress, it will be detected again at regular intervals, and the time interval is configured by this, default 3s."""
    taskNameLabel: str = None
    """ "Task name" # Description of the task name column"""
    operationLabel: str = None
    """ "operation" # Description of the operation column"""
    statusLabel: str = None
    """ "Status" # Status column description"""
    remarkLabel: str = None
    """ "Remarks" # Remarks column description"""
    btnText: str = None
    """ "Go Live" # Action button text"""
    retryBtnText: str = None
    """ "Retry" # Retry action button text"""
    btnClassName: str = None
    """ "btn-sm btn-default" # Configure the container button className"""
    retryBtnClassName: str = None
    """ "btn-sm btn-danger" # Configure the container retry button className"""
    statusLabelMap: List[str] = None
    """ Configuration of the class name corresponding to the status display ["label-warning", "label-info", "label-success", "label-danger", "label-default", "label-danger"] """
    statusTextMap: List[
        str] = None
    """ "["Not Started", "Ready", "In Progress", "Error", "Completed", "Error"]" # Status display corresponding to the text display configuration"""


class Wizard(MSAUINode):
    """Wizard"""

    class Step(MSAUINode):
        title: str = None
        """ Step title"""
        mode: str = None
        """ Show default, same as mode in Form, choose: normal, horizontal or inline."""
        horizontal: Horizontal = None
        """ When in horizontal mode, used to control the left/right aspect ratio"""
        api: MSA_UI_API = None
        """ The current step saves the interface, can be unconfigured."""
        initApi: MSA_UI_API = None
        """ The current step data initialization interface."""
        initFetch: bool = None
        """ Whether the current step data initialization interface is initially pulling."""
        initFetchOn: MSAUIExpression = None
        """ Whether the current step data initialization interface is pulling initially, using an expression to determine."""
        body: List[FormItem] = None
        """ A collection of form items for the current step, see FormItem."""

    type: str = "wizard"
    """ Specify as a Wizard component"""
    mode: str = None
    """ Display mode, choose: horizontal or vertical"""
    api: MSA_UI_API = None
    """ The interface saved in the last step."""
    initApi: MSA_UI_API = None
    """ Initialize the data interface"""
    initFetch: MSA_UI_API = None
    """ Initialize whether to pull data."""
    initFetchOn: MSAUIExpression = None
    """ Initially pull data or not, configured by expression"""
    actionPrevLabel: str = None
    """ "Previous" # Previous button text"""
    actionNextLabel: str = None
    """ "Next" # Next button text"""
    actionNextSaveLabel: str = None
    """ "Save and Next" # Save and Next button text"""
    actionFinishLabel: str = None
    """ "Finish" # Finish button text"""
    className: str = None
    """ Outer CSS class name"""
    actionClassName: str = None
    """ "btn-sm btn-default" # Button CSS class name"""
    reload: str = None
    """ Refresh the target object after the operation. Please fill in the name value set by the target component, if it is window then the whole current page will be refreshed."""
    redirect: MSAUITemplate = None
    """ "3000" # Jump after the operation."""
    target: str = None
    """ "False" # You can submit the data to another component instead of saving it yourself. Please fill in the name value set by the target component.
    If you fill in window, the data will be synced to the address bar, and the component that depends on the data will be refreshed automatically."""
    steps: List[Step] = None
    """ Array to configure step information"""
    startStep: int = None
    """ "1" # Start default value, from which step to start. Templates can be supported, but only if the template is rendered and the current step is set when the component is created, and when the component is refreshed later
    The current step will not change according to startStep"""


PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
MSAUITpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()
