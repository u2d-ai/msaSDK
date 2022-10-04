import os
from typing import Any, Dict, List, Optional, Union

from pydantic import Field

from .constants import DisplayModeEnum, LevelEnum, SizeEnum, TabsModeEnum
from .types import (MSA_UI_API, MSABaseUIModel, MSAOptionsNode,
                    MSAUIExpression, MSAUINode, MSAUISchemaNode, MSAUITemplate,
                    MSAUITpl)
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
    className: Optional[str] = None
    """ Outer CSS class name"""
    icon: Optional[str] = None
    """ icon name, supports fontawesome v4 or use url"""


class Remark(MSAUINode):
    """marker"""

    type: str = "remark"
    """ remark"""
    className: Optional[str] = None
    """ Outer CSS class name"""
    content: Optional[str] = None
    """ Prompt text"""
    placement: Optional[str] = None
    """ popup position"""
    trigger: Optional[str] = None
    """ trigger condition ['hover','focus']"""
    icon: Optional[str] = None
    """ "fa fa-question-circle" # Icon"""


class Badge(MSAUINode):
    """corner-icon"""

    mode: str = "dot"
    """ Corner type, can be dot/text/ribbon"""
    text: Optional[Union[str, int]] = None
    """ corner text, supports strings and numbers, invalid when set under mode='dot'"""
    size: Optional[int] = None
    """ corner size"""
    level: Optional[str] = None
    """ Corner level, can be info/success/warning/danger, different background color after setting"""
    overflowCount: Optional[int] = None
    """ 99 # Set the capping number value"""
    position: Optional[str] = None
    """ "top-right" # corner position, can be top-right/top-left/bottom-right/bottom-left"""
    offset: Optional[int] = None
    """ corner position, priority is greater than position, when offset is set, postion is top-right as the base for positioning number[top, left]"""
    className: Optional[str] = None
    """ class name of outer dom"""
    animation: Optional[bool] = None
    """ whether the corner is animated or not"""
    style: Optional[Dict] = None
    """ custom style for the corner"""
    visibleOn: Optional[MSAUIExpression] = None
    """ Control the display and hiding of the corner"""


class Page(MSAUINode):
    """page"""

    __default_template_path__: str = f"{BASE_DIR}/templates/page.html"

    type: str = "page"
    """ Specify as Page component"""
    title: Optional[MSAUISchemaNode] = None
    """ Page title"""
    subTitle: Optional[MSAUISchemaNode] = None
    """ page sub-title"""
    remark: Optional["Remark"] = None
    """ A reminder icon will appear near the title, which will prompt the content when the mouse is placed on it."""
    aside: Optional[MSAUISchemaNode] = None
    """ Add content to the sidebar area of the page."""
    asideResizor: Optional[bool] = None
    """ Whether the width of the page's sidebar area can be adjusted"""
    asideMinWidth: Optional[int] = None
    """ The minimum width of the page's sidebar area"""
    asideMaxWidth: Optional[int] = None
    """ The maximum width of the page's sidebar area"""
    toolbar: Optional[MSAUISchemaNode] = None
    """ Add content to the top right corner of the page, note that when there is a title, the area is in the top right corner and when there is not, the area is at the top"""
    body: Optional[MSAUISchemaNode] = None
    """ Add content to the content area of the page"""
    className: Optional[str] = None
    """ Outer dom class name"""
    cssVars: Optional[Dict] = None
    """ Custom CSS variables, please refer to styles"""
    toolbarClassName: Optional[str] = None
    """ "v-middle wrapper text-right bg-light b-b" # Toolbar dom class name"""
    bodyClassName: Optional[str] = None
    """ "wrapper" # Body dom class name"""
    asideClassName: Optional[str] = None
    """ "w page-aside-region bg-auto" # Aside dom class name"""
    headerClassName: Optional[str] = None
    """ "bg-light b-b wrapper" # Header region dom class name"""
    initApi: Optional[MSA_UI_API] = None
    """ Page The api used to fetch the initial data. the returned data can be used at the entire page level."""
    initFetch: Optional[bool] = None
    """ True # Whether to start fetching initApi"""
    initFetchOn: Optional[MSAUIExpression] = None
    """ Whether to start fetching initApi, configured by expression"""
    interval: Optional[int] = None
    """ Refresh time (min 1000)"""
    silentPolling: Optional[bool] = None
    """ False # Configure whether to show loading animation when refreshing"""
    stopAutoRefreshWhen: Optional[MSAUIExpression] = None
    """ Expression to configure the stop refresh condition"""
    regions: Optional[List[str]] = None

    def msa_ui_html(
        self,
        template_path: str = "",
        locale: str = "zh_CN",
        site_title: str = "Admin",
        site_icon: str = "",
        cdn: str = "https://unpkg.com",
        pkg: str = "amis@2.3.0",
        theme: str = "cxd",
    ):
        template_path = template_path or self.__default_template_path__
        theme_css = f'<link href="{cdn}/{pkg}/sdk/{theme}.css" rel="stylesheet"/>' if theme != "cxd" else ""
        return msa_ui_templates(template_path).safe_substitute(
            {
                "MSAUISchemaJson": self.msa_ui_json(),
                "locale": locale.replace("_", "-"),  # Fix #50
                "cdn": cdn,
                "pkg": pkg,
                "site_title": site_title,
                "site_icon": site_icon,
                "theme": theme,
                "theme_css": theme_css,
            }
        )


class Divider(MSAUINode):
    type: str = "divider"
    """ Divider"""
    className: Optional[str] = None
    """ class name of the outer Dom"""
    lineStyle: Optional[str] = None
    """ The style of the divider line, supports dashed and solid"""


class Flex(MSAUINode):
    type: str = "flex"
    """ Specify as Flex renderer"""
    className: Optional[str] = None
    """ css class name"""
    justify: Optional[str] = None
    """ "start", "flex-start", "center", "end", "flex-end", "space-around", "space-between", "space-evenly" """
    alignItems: Optional[str] = None
    """ "stretch", "start", "flex-start", "flex-end", "end", "center", "baseline" """
    style: Optional[Dict] = None
    """ Custom style"""
    items: Optional[List[MSAUISchemaNode]] = None


class Grid(MSAUINode):
    class Column(MSAUINode):
        xs: Optional[int] = None
        """ "auto" # Width percentage: 1 - 12"""
        ClassName: Optional[str] = None
        """ Column class name"""
        sm: Optional[int] = None
        """ "auto" # Width ratio: 1 - 12"""
        md: Optional[int] = None
        """ "auto" # Width ratio: 1 - 12"""
        lg: Optional[int] = None
        """ "auto" # Width ratio: 1 - 12"""
        valign: Optional[str] = None
        """ 'top'|'middle'|'bottom'|'between = None # Vertical alignment of current column content"""
        body: Optional[List[MSAUISchemaNode]] = None

    type: str = "grid"
    """ Specify as Grid renderer"""
    className: Optional[str] = None
    """ Class name of the outer Dom"""
    gap: Optional[str] = None
    """ 'xs'|'sm'|'base'|'none'|'md'|'lg = None # Horizontal spacing"""
    valign: Optional[str] = None
    """ 'top'|'middle'|'bottom'|'between = None # Vertical alignment"""
    align: Optional[str] = None
    """ 'left'|'right'|'between'|'center = None # horizontal alignment"""
    columns: Optional[List[MSAUISchemaNode]] = None


class Panel(MSAUINode):
    type: str = "panel"
    """ Specify as Panel renderer"""
    className: Optional[str] = None
    """ "panel-default" # class name of outer Dom"""
    headerClassName: Optional[str] = None
    """ "panel-heading" # Class name of the header area"""
    footerClassName: Optional[str] = None
    """ "panel-footer bg-light lter wrapper" # Class name of the footer region"""
    actionsClassName: Optional[str] = None
    """ "panel-footer" # Class name of the actions region"""
    bodyClassName: Optional[str] = None
    """ "panel-body" # Class name for the body region"""
    title: Optional[MSAUISchemaNode] = None
    """ title"""
    header: Optional[MSAUISchemaNode] = None
    """ header container"""
    body: Optional[MSAUISchemaNode] = None
    """ content container"""
    footer: Optional[MSAUISchemaNode] = None
    """ footer container"""
    affixFooter: Optional[bool] = None
    """ Whether to fix the bottom container"""
    actions: Optional[List["Action"]] = None
    """ Button area"""


class Tabs(MSAUINode):
    class Item(MSAUINode):
        title: Optional[str] = None
        """ Tab title"""
        icon: Optional[Union[str, Icon]] = None
        """ Tab's icon"""
        tab: Optional[MSAUISchemaNode] = None
        """ Content area"""
        hash: Optional[str] = None
        """ Set to correspond to the hash of the url"""
        reload: Optional[bool] = None
        """ Set the content to be re-rendered every time, useful for crud re-pulling"""
        unmountOnExit: Optional[bool] = None
        """ Destroy the current tab bar every time you exit"""
        className: Optional[str] = None
        """ "bg-white b-l b-r b-b wrapper-md" # Tab area style"""
        iconPosition: Optional[str] = None
        """ "left" # Tab's icon position left / right"""
        closable: Optional[bool] = None
        """ False # Whether to support deletion, prioritize over component's closable"""
        disabled: Optional[bool] = None
        """ False # Whether to disable"""

    type: str = "tabs"
    """ Specify as Tabs renderer"""
    className: Optional[str] = None
    """ The class name of the outer Dom"""
    mode: Optional[str] = None
    """ Display mode, can be line, card, radio, vertical, chrome, simple, strong, tiled, sidebar"""
    tabsClassName: Optional[str] = None
    """ The class name of the Tabs Dom"""
    tabs: Optional[List[Item]] = None
    """ tabs content"""
    source: Optional[str] = None
    """ tabs association data, can repeat tabs after association"""
    toolbar: Optional[MSAUISchemaNode] = None
    """ Toolbar in tabs"""
    toolbarClassName: Optional[str] = None
    """ The class name of the toolbar in tabs"""
    mountOnEnter: Optional[bool] = None
    """ False # Render only when tab is clicked"""
    unmountOnExit: Optional[bool] = None
    """ False # Destroy when tab is toggled"""
    scrollable: Optional[bool] = None
    """ False # whether navigation supports content overflow scrolling, not supported in vertical and chrome modes; chrome mode compresses tabs by default (property deprecated)"""
    tabsMode: Optional[TabsModeEnum] = None
    """ display mode, the value can be line, card, radio, vertical, chrome, simple, strong, tiled, sidebar"""
    addable: Optional[bool] = None
    """ False # If or not addable is supported"""
    addBtnText: Optional[str] = None
    """ "add" # Add button text"""
    closeable: Optional[bool] = None
    """ False # Whether to support delete"""
    draggable: Optional[bool] = None
    """ False # Whether drag and drop is supported"""
    showTip: Optional[bool] = None
    """ False # Whether to support hints"""
    showTipClassName: Optional[str] = None
    """ "'' " # The class of the prompt"""
    editable: Optional[bool] = None
    """ False # Whether to make the tag name editable or not"""
    sidePosition: Optional[str] = None
    """ "left" # sidebar mode, tab position left / right"""


class Portlet(Tabs):
    class Item(Tabs.Item):
        toolbar: Optional[MSAUISchemaNode] = None
        """ toolbar in tabs, changes with tab toggle"""

    type: str = "portlet"
    """ Specify as Portlet renderer"""
    contentClassName: Optional[str] = None
    """ Class name of the Tabs content Dom"""
    tabs: Optional[List[Item]] = None
    """ Contents of tabs"""
    style: Optional[Union[str, dict] ] = None
    """ Custom style"""
    description: Optional[MSAUITemplate] = None
    """ Information on the right side of the title"""
    hideHeader: Optional[bool] = None
    """ False # Hide the header"""
    divider: Optional[bool] = None
    """ False # Remove the divider"""


class Horizontal(MSAUINode):
    left: Optional[int] = None
    """ The width of the left label as a percentage"""
    right: Optional[int] = None
    """ The width share of the right controller."""
    offset: Optional[int] = None
    """ The offset of the right controller when no label is set"""


class Action(MSAUINode):
    type: str = "button"
    """ Specify as Page renderer. button action"""
    actionType: Optional[str] = None
    """ [Required] This is the core configuration of the action, to specify the action's role type.
    Supports: ajax, link, url, drawer, dialog, confirm, cancel, prev, next, copy, close.
    """
    label: Optional[str] = None
    """ The text of the button. Can be fetched with ${xxx}."""
    level: Optional[LevelEnum] = None
    """ The style of the button, support: link, primary, secondary, info, success, warning, danger, light, dark, default."""
    size: Optional[str] = None
    """ The size of the button, support: xs, sm, md, lg."""
    icon: Optional[str] = None
    """ Set icon, e.g. fa fa-plus."""
    iconClassName: Optional[str] = None
    """ Add a class name to the icon."""
    rightIcon: Optional[str] = None
    """ Set the icon to the right of the button text, e.g. fa fa-plus."""
    rightIconClassName: Optional[str] = None
    """ Add a class name to the right icon."""
    active: Optional[bool] = None
    """ If or not the button is highlighted."""
    activeLevel: Optional[str] = None
    """ The style of the button when it is highlighted, configured to support the same level."""
    activeClassName: Optional[str] = None
    """ Add a class name to the button highlighting. "is-active" """
    block: Optional[bool] = None
    """ Use display: "block" to display the button."""
    confirmText: Optional[MSAUITemplate] = None
    """ When set, the action will ask the user before starting. Can be fetched with ${xxx}."""
    reload: Optional[str] = None
    """ Specify the name of the target component to be refreshed after this operation (the component's name value, configured by yourself), separated by ,."""
    tooltip: Optional[str] = None
    """ popup text when mouse hover, also can configure the object type: title and content. can be ${xxx}."""
    disabledTip: Optional[str] = None
    """ Popup when mouse hover is disabled, you can also configure the object type: fields are title and content. available ${xxx}."""
    tooltipPlacement: Optional[str] = None
    """ If tooltip or disabledTip is configured, specify the location of the tip, you can configure top, bottom, left, right."""
    close: Optional[Union[bool, str]] = None
    """ When action is configured in dialog or drawer's actions, set to true to close the current dialog or drawer after this action."""
    required: Optional[List[str]] = None
    """ Configure an array of strings, specifying that the form entry of the specified field name is required to pass validation before the operation can be performed in the form"""

    # primary:bool=None
    onClick: Optional[str] = None
    """ Customize the click event by defining the click event as a string onClick, which will be converted to a JavaScript function"""
    componentId: Optional[str] = None
    """ Target component ID"""
    args: Optional[Union[dict, str]] = None
    """ Event arguments"""
    script: Optional[str] = None
    """ Custom JS script code, which can perform any action by calling doAction, and event action intervention through the event object event"""


class ActionType:
    class Ajax(Action):
        actionType: str = "ajax"
        """ Click to display a popup box"""
        api: Optional[MSA_UI_API] = None
        """ request address, refer to api format description."""
        redirect: Optional[MSAUITemplate] = None
        """ Specify the path to jump to at the end of the current request, can be fetched with ${xxx}."""
        feedback: Optional["Dialog"] = None
        """ If ajax type, when the ajax returns normal, a dialog can be popped up to do other interactions. The returned data can be used in this dialog. See Dialog for format"""
        messages: Optional[Dict] = None
        """ success: ajax operation success prompt, can not be specified, not specified when the api return prevail. failed: ajax operation failure prompt."""

    class Dialog(Action):
        actionType: str = "dialog"
        """ Show a popup box when clicked."""
        dialog: Union["Dialog", "Service", MSAUISchemaNode]
        """ Specify the content of the popup box, see Dialog for format"""
        nextCondition: Optional[bool] = None
        """ Can be used to set the next data condition, default is true."""

    class Drawer(Action):
        actionType: str = "drawer"
        """ Show a sidebar when clicked"""
        drawer: Union["Drawer", "Service", MSAUISchemaNode]
        """ Specify the content of the popup box, see Drawer for format"""

    class Copy(Action):
        actionType: str = "copy"
        """ Copy a piece of content to the pasteboard"""
        content: MSAUITemplate
        """ Specify the content to be copied. Can be fetched with ${xxx}."""
        copyFormat: Optional[str] = None
        """ The format of the copy can be set by copyFormat, default is text/html"""

    class Url(Action):
        actionType: str = "url"
        """ Jump directly """
        url: str
        """ When the button is clicked, the specified page will be opened. Can be fetched with ${xxx}. """
        blank: Optional[bool] = None
        """ false if true will open in a new tab page. """

    class Link(Action):
        actionType: str = "link"
        link: str


class PageSchema(MSAUINode):
    label: Optional[str] = None
    """ The name of the menu. """
    icon: str = "fa fa-flash"
    """ Menu icon, e.g., 'fa fa-file'. """
    url: Optional[str] = None
    """ The page routing path to enable the current page when the route hits that path. When the path is not /-headed, the parent path is connected.
        For example, if the parent path is folder and pageA is configured, then the page will be hit when the page address is /folder/pageA. 
        When the path starts with /, e.g. /crud/list, the parent path is not concatenated. 
        There is also support for routes with parameters such as /crud/view/:id, which can be fetched from the page via ${params.id}. """
    schema_: Union[Page, "Iframe"] = Field(None, alias="schema")
    """ Configuration of the page, please go to the Page page for details """
    schemaApi: Optional[MSA_UI_API] = None
    """ If you want to pull through the interface, please configure it. The return path is json>data. schema and schemaApi can only be one or the other. """
    link: Optional[str] = None
    """ If you want to configure an external link menu, just configure link. """
    redirect: Optional[str] = None
    """ Jump, when the current page is hit, jump to the target page. """
    rewrite: Optional[str] = None
    """ Change to render a page with another path, this way the page address will not be changed. """
    isDefaultPage: Optional[Union[str, bool]] = None
    """ Useful when you need a custom 404 page, don't have more than one of these, because only the first one will work. """
    visible: Optional[str] = None
    """ Some pages may not want to appear in the menu, you can configure it to false, in addition to the route with parameters do not need to be configured, directly is not visible. """
    className: Optional[str] = None
    """ The class name of the menu. """
    children: Optional[List["PageSchema"]] = None
    """ Submenus """
    sort: Optional[int] = None
    """ Sort """

    def as_tabs_item(
        self, tabs_extra: Dict[str, Any] = None, item_extra: Dict[str, Any] = None
    ):
        if self.children:
            tabs = Tabs(
                tabs=[
                    item.as_tabs_item(tabs_extra, item_extra) for item in self.children
                ]
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

    __default_template_path__: str = f"{BASE_DIR}/templates/app.html"
    type: str = "app"
    api: Optional[MSA_UI_API] = None
    """ Page configuration interface, please configure if you want to pull the page configuration remotely. Return the configuration path json>data>pages, please refer to the pages property for the exact format. """
    brandName: Optional[str] = None
    """ Application name """
    logo: str = "/msastatic/img/msaSDK_logo.png"
    """ Support image address, or svg. """
    className: Optional[str] = None
    """ css class name """
    header: Optional[str] = None
    """ header """
    asideBefore: Optional[str] = None
    """ The area in front of the page menu. """
    asideAfter: Optional[str] = None
    """ The area under the page menu. """
    footer: Optional[str] = None
    """ The page. """
    pages: Optional[List[PageSchema]] = None
    """ Array<PageSchema> specific page configuration.
        Usually an array, the first layer of the array is grouped, usually only the label set needs to be configured, 
        if you do not want to group, directly not configured, the real pages please start configuring in the second layer, 
        that is, the first layer of children. """


class ButtonGroup(MSAUINode):
    """buttonGroup"""

    type: str = "button-group"
    buttons: List[Action]
    """ Behavior button group """
    className: Optional[str] = None
    """ the class name of the outer Dom """
    vertical: Optional[bool] = None
    """ whether to use vertical mode """


class Custom(MSAUINode):
    """custom component"""

    type: str = "custom"
    id: Optional[str] = None
    """ node id """
    name: Optional[str] = None
    """ node name """
    className: Optional[str] = None
    """ node class """
    inline: bool = False
    """ default use div tag, if true use span tag """
    html: Optional[str] = None
    """ Initialize node html """
    onMount: Optional[str] = None
    """ "Function" # The function to call after the node is initialized """
    onUpdate: Optional[str] = None
    """ "Function" # Function to be called when data is updated """
    onUnmount: Optional[str] = None
    """ "Function" # The function called when the node is destroyed """


class Service(MSAUINode):
    """Function container"""

    type: str = "service"
    """ Specified as a service renderer """
    name: Optional[str] = None
    """ node name """
    data: Optional[Dict] = None
    className: Optional[str] = None
    """ Class name of the outer Dom """
    body: Optional[MSAUISchemaNode] = None
    """ Content container """
    api: Optional[MSA_UI_API] = None
    """ Initial data domain interface address """
    ws: Optional[str] = None
    """ WebScocket address """
    dataProvider: Optional[str] = None
    """ Data fetch function """
    initFetch: Optional[bool] = None
    """ Whether to pull by default """
    schemaApi: Optional[MSA_UI_API] = None
    """ Used to fetch the remote Schema interface address """
    initFetchSchema: Optional[bool] = None
    """ Whether to pull Schema by default """
    messages: Optional[Dict] = None
    """ Message hint override, the default message reads the toast hint text returned by the interface, but it can be overridden here. """
    interval: Optional[int] = None
    """ polling interval (minimum 3000) """
    silentPolling: Optional[bool] = None
    """ False # Configure whether to show loading animation when polling """
    stopAutoRefreshWhen: Optional[MSAUIExpression] = None
    """ Configure the conditions for stopping polling """


class Nav(MSAUINode):
    """Navigate"""

    class Link(MSAUINode):
        label: Optional[str] = None
        """ Name """
        to: Optional[MSAUITemplate] = None
        """ Link address """
        target: Optional[str] = None
        """ "Link relationship" # """
        icon: Optional[str] = None
        """ Icon """
        children: Optional[List["Link"]] = None
        """ child links """
        unfolded: Optional[bool] = None
        """ Initially expanded or not """
        active: Optional[bool] = None
        """ Whether to highlight or not """
        activeOn: Optional[MSAUIExpression] = None
        """ condition to highlight or not, leaving blank will automatically analyze the link address """
        defer: Optional[bool] = None
        """ Flag if it is a lazy add-on """
        deferApi: Optional[MSA_UI_API] = None
        """ Can be unconfigured, if configured priority is higher """

    type: str = "nav"
    """ Specify as Nav renderer """
    className: Optional[str] = None
    """ Class name of the outer Dom """
    stacked: bool = True
    """ Set to false to display as tabs """
    source: Optional[MSA_UI_API] = None
    """ Navigation can be created dynamically via variables or the MSA_UI_API interface """
    deferApi: Optional[MSA_UI_API] = None
    """ Interface used to delay loading of option details, can be left unconfigured, no common source interface configured. """
    itemActions: Optional[MSAUISchemaNode] = None
    """ More action related configuration """
    draggable: Optional[bool] = None
    """ Whether to support drag and drop sorting """
    dragOnSameLevel: Optional[bool] = None
    """ Only allows dragging within the same level """
    saveOrderApi: Optional[MSA_UI_API] = None
    """ api to save sorting """
    itemBadge: Optional[Badge] = None
    """ corner markers """
    links: Optional[list] = None
    """ Collection of links """


class AnchorNav(MSAUINode):
    """Anchor Nav"""

    class Link(MSAUINode):
        label: Optional[str] = None
        """ name """
        title: Optional[str] = None
        """ area title """
        href: Optional[str] = None
        """ region identifier """
        body: Optional[MSAUISchemaNode] = None
        """ area content area """
        className: Optional[str] = None
        """ "bg-white b-l b-r b-b wrapper-md" # region member style """

    type: str = "anchor-nav"
    """ Specify as AnchorNav renderer """
    className: Optional[str] = None
    """ Class name of the outer Dom """
    linkClassName: Optional[str] = None
    """ Class name of the navigating Dom """
    sectionClassName: Optional[str] = None
    """ Class name of the anchor area Dom """
    links: Optional[List] = None
    """ Contents of links """
    direction: Optional[str] = None
    """ "vertical" # You can configure whether the navigation is displayed horizontally or vertically. The corresponding configuration items are: vertical, horizontal """
    active: Optional[str] = None
    """ The area to be positioned """


class ButtonToolbar(MSAUINode):
    """ButtonToolbar"""

    type: str = "button-toolbar"
    buttons: List[Action]
    """ Behavior button group """


class Validation(MSABaseUIModel):
    isEmail: Optional[bool] = None
    """ Must be Email. """
    isUrl: Optional[bool] = None
    """ Must be Url. """
    isNumeric: Optional[bool] = None
    """ Must be numeric. """
    isAlpha: Optional[bool] = None
    """ Must be a letter. """
    isAlphanumeric: Optional[bool] = None
    """ Must be alphabetic or numeric. """
    isInt: Optional[bool] = None
    """ Must be integer. """
    isFloat: Optional[bool] = None
    """ Must be floating point. """
    isLength: Optional[int] = None
    """ If or not the length is exactly equal to the set value. """
    minLength: Optional[int] = None
    """ The minimum length. """
    maxLength: Optional[int] = None
    """ The maximum length. """
    maximum: Optional[int] = None
    """ The maximum value. """
    minimum: Optional[int] = None
    """ The minimum value. """
    equals: Optional[str] = None
    """ The current value must be exactly equal to xxx. """
    equalsField: Optional[str] = None
    """ The current value must match the value of the xxx variable. """
    isJson: Optional[bool] = None
    """ If or not it is a legal Json string.
    isUrlPath: Optional[bool] = None """
    """ Is the url path. """
    isPhoneNumber: Optional[bool] = None
    """ If or not it is a legitimate phone number """
    isTelNumber: Optional[bool] = None
    """ if it is a legitimate phone number """
    isZipcode: Optional[bool] = None
    """ Whether it is a zip code number """
    isId: Optional[bool] = None
    """ if it is an ID number, no check """
    matchRegexp: Optional[str] = None
    """ Must hit some regular. /foo/ """


class FormItem(MSAUINode):
    """FormItemGeneral"""

    type: str = "input-text"
    """ Specify the form item type """
    className: Optional[str] = None
    """ The outermost class name of the form """
    inputClassName: Optional[str] = None
    """ Form controller class name """
    labelClassName: Optional[str] = None
    """ Class name of the label """
    name: Optional[str] = None
    """ Field name, specifying the key of the form item when it is submitted """
    label: Optional[MSAUITemplate] = None
    """ Label of the form item Template or false """
    value: Optional[Union[int, str]] = None
    """ The value of the field """
    labelRemark: Optional["Remark"] = None
    """ Description of the form item label """
    description: Optional[MSAUITemplate] = None
    """ Form item description """
    placeholder: Optional[str] = None
    """ Form item description """
    inline: Optional[bool] = None
    """ Whether inline mode """
    submitOnChange: Optional[bool] = None
    """ Whether to submit the current form when the value of the form item changes. """
    disabled: Optional[bool] = None
    """ Whether the current form item is disabled or not """
    disabledOn: Optional[MSAUIExpression] = None
    """ The condition whether the current form item is disabled or not """
    visible: Optional[MSAUIExpression] = None
    """ The condition whether the current form item is disabled or not """
    visibleOn: Optional[MSAUIExpression] = None
    """ The condition if the current table item is disabled or not """
    required: Optional[bool] = None
    """ Whether or not it is required. """
    requiredOn: Optional[MSAUIExpression] = None
    """ Expression to configure if the current form entry is required. """
    validations: Optional[Union[Validation, MSAUIExpression]] = None
    """ Form item value format validation, support setting multiple, multiple rules separated by English commas. """
    validateApi: Optional[MSAUIExpression] = None
    """ Form validation interface """
    copyable: Optional[Union[bool, dict]] = None
    """ Whether copyable boolean or {icon: string, content:string} """


class Form(MSAUINode):
    """Form"""

    class Messages(MSAUINode):
        fetchSuccess: Optional[str] = None
        """ Prompt when fetch succeeds """
        fetchFailed: Optional[str] = None
        """ prompt for fetch failure """
        saveSuccess: Optional[str] = None
        """ Prompt for successful save """
        saveFailed: Optional[str] = None
        """ Prompt for failed save """

    type: str = "form"
    """ "form" is specified as a Form renderer """
    name: Optional[str] = None
    """ Set a name so that other components can communicate with it """
    mode: Optional[DisplayModeEnum] = None
    """ How the form is displayed, either: normal, horizontal or inline """
    horizontal: Optional[Horizontal] = None
    """ Useful when mode is horizontal. """

    """ Used to control label {"left": "col-sm-2", "right": "col-sm-10", "offset": "col-sm-offset-2"} """
    title: Optional[str] = None
    """ Title of the Form """
    submitText: Optional[str] = None
    """ "submit" # The default submit button name, if set to null, the default button can be removed. """
    className: Optional[str] = None
    """ The class name of the outer Dom """
    body: Optional[List[Union[FormItem, MSAUISchemaNode]]] = None
    """ Form form item collection """
    actions: Optional[List["Action"]] = None
    """ Form submit button, member of Action """
    actionsClassName: Optional[str] = None
    """ Class name of actions """
    messages: Optional[Messages] = None
    """ Message prompt override, the default message reads the message returned by MSA_UI_API, but it can be overridden here. """
    wrapWithPanel: Optional[bool] = None
    """ Whether to let Form wrap with panel, set to false and actions will be invalid. """
    panelClassName: Optional[str] = None
    """ The class name of the outer panel """
    api: Optional[MSA_UI_API] = None
    """ The api used by Form to save data. """
    initApi: Optional[MSA_UI_API] = None
    """ The api used by Form to get the initial data. """
    rules: Optional[List] = None
    """ Form combination check rules Array<{rule:string;message:string}> """
    interval: Optional[int] = None
    """ Refresh time (minimum 3000) """
    silentPolling: bool = False
    """ Configure whether to show loading animation when refreshing """
    stopAutoRefreshWhen: Optional[str] = None
    """ Configure the conditions for stopping the refresh via an expression """
    initAsyncApi: Optional[MSA_UI_API] = None
    """ The api used by Form to get the initial data, unlike initApi, it will keep polling the request until the finished property is returned as true. """
    initFetch: Optional[bool] = None
    """ When initApi or initAsyncApi is set, the request will start by default, but when set to false, the interface will not be requested from the beginning. """
    initFetchOn: Optional[str] = None
    """ Use an expression to configure """
    initFinishedField: Optional[str] = None
    """ When initAsyncApi is set, the default is to determine if the request is completed by returning data.finished. """

    """ You can also set it to other xxx, and it will be retrieved from data.xxx """
    initCheckInterval: Optional[int] = None
    """ After setting initAsyncApi, the default time interval for pulling """
    asyncApi: Optional[MSA_UI_API] = None
    """ After this property is set, the form will continue to poll the interface after it is submitted and sent to the saved interface until the finished property is returned as true. """
    checkInterval: Optional[int] = None
    """ The time interval to poll the request, default is 3 seconds. Set asyncApi to be valid """
    finishedField: Optional[str] = None
    """ Set this property if the field name that determines the finish is not finished, e.g. is_success """
    submitOnChange: Optional[bool] = None
    """ The form is submitted when it is modified """
    submitOnInit: Optional[bool] = None
    """ Submit once at the beginning """
    resetAfterSubmit: Optional[bool] = None
    """ whether to reset the form after submission """
    primaryField: Optional[str] = None
    """ Set primary key id, when set, only carry this data when detecting form completion (asyncApi). """
    target: Optional[str] = None
    """ The default form submission saves the data itself by sending the api, but you can set the name value of another form
    or the name value of another CRUD model. If the target is a Form, the target Form will retrigger initApi and the api will get the current form data. 
    If the target is a CRUD model, the target model retriggers the search with the current Form data as the argument. When the target is a window, the current form data will be attached to the page address. """
    redirect: Optional[str] = None
    """ When this property is set, the Form will automatically jump to the specified page after a successful save. Supports relative addresses, and absolute addresses (relative to the group). """
    reload: Optional[str] = None
    """ Refresh the target object after the operation. Please fill in the name value set by the target component, if you fill in the name of window, the current page will be refreshed as a whole. """
    autoFocus: Optional[bool] = None
    """ If or not autoFocus is enabled. """
    canAccessSuperData: Optional[bool] = None
    """ Specifies whether the data from the upper level can be automatically retrieved and mapped to the form item. """
    persistData: Optional[str] = None
    """ Specify a unique key to configure whether to enable local caching for the current form """
    clearPersistDataAfterSubmit: Optional[bool] = None
    """ Specify whether to clear the local cache after a successful form submission """
    preventEnterSubmit: Optional[bool] = None
    """ Disable carriage return to submit the form """
    trimValues: Optional[bool] = None
    """ trim each value of the current form item """
    promptPageLeave: Optional[bool] = None
    """ whether the form is not yet saved and will pop up before leaving the page to confirm. """
    columnCount: Optional[int] = None
    """ How many columns are displayed for the form item """
    debug: Optional[bool] = None


class Button(FormItem):
    """Button"""

    className: Optional[str] = None
    """ Specifies the class name of the added button """
    href: Optional[str] = None
    """ Click on the address of the jump, specify this property button behavior and a link consistent """
    size: Optional[str] = None
    """ Set the size of the button 'xs'|'sm'|'md'|'lg' """
    actionType: Optional[str] = None
    """ Set the button type 'button'|'reset'|'submit'| 'clear'| 'url' """
    level: Optional[LevelEnum] = None

    """ Set the button style 'link'|'primary'|'enhance'|'secondary'|'info'|'success'|'warning'|'danger'|'light'| 'dark'|'default' """
    tooltip: Optional[Union[str, dict] ] = None
    """ bubble tip content TooltipObject """
    tooltipPlacement: Optional[str] = None
    """ bubblePlacement 'top'|'right'|'bottom'|'left' """
    tooltipTrigger: Optional[str] = None
    """ trigger tootip 'hover'|'focus' """
    disabled: Optional[bool] = None
    """ Disable button status """
    block: Optional[bool] = None
    """ option to adjust the width of the button to its parent width """
    loading: Optional[bool] = None
    """ Show button loading effect """
    loadingOn: Optional[str] = None
    """ Show button loading expressions """


class InputArray(FormItem):
    """arrayInputArray"""

    type: str = "input-array"
    items: Optional[FormItem] = None
    """ Configure single-item form type """
    addable: Optional[bool] = None
    """ Whether addable. """
    removable: Optional[bool] = None
    """ Whether removable """
    draggable: bool = False
    """ whether draggable, note that when draggable is enabled, there will be an extra $id field """
    draggableTip: Optional[str] = None
    """ draggable prompt text, default is: "can be adjusted by dragging the [swap] button in each row" """
    addButtonText: Optional[str] = None
    """ "Add" # Add button text """
    minLength: Optional[int] = None
    """ Limit the minimum length """
    maxLength: Optional[int] = None
    """ Limit the maximum length """


class Hidden(FormItem):
    """hiddenField"""

    type: str = "hidden"


class Checkbox(FormItem):
    """Checkbox"""

    type: str = "checkbox"
    option: Optional[str] = None
    """ option description """
    trueValue: Any = None
    """ Identifies the true value """
    falseValue: Any = None
    """ Identifies a false value """


class Radios(FormItem):
    """RadioBox"""

    type: str = "radios"
    options: Optional[List[Union[dict, str]]] = None
    """ option group """
    source: Optional[MSA_UI_API] = None
    """ dynamic options group """
    labelField: Optional[bool] = None
    """ "label" # option label field """
    valueField: Optional[bool] = None
    """ "value" # option value field """
    columnsCount: Optional[int] = None
    """ 1 # How many columns to display options by, default is one column """
    inline: Optional[bool] = None
    """ True # Whether to display as one line """
    selectFirst: Optional[bool] = None
    """ False # Whether to select the first by default """
    autoFill: Optional[Dict] = None
    """ AutoFill """


class ChartRadios(Radios):
    """radio box"""

    type: str = "chart-radios"
    config: Optional[Dict] = None
    """ echart chart configuration """
    showTooltipOnHighlight: Optional[bool] = None
    """ False # whether to show tooltip when highlighted """
    chartValueField: Optional[str] = None
    """ "value" # chart value field name """


class Checkboxes(FormItem):
    """checkboxes"""

    type: str = "checkboxes"
    options: Optional[MSAOptionsNode] = None
    """ Options group """
    source: Optional[MSA_UI_API] = None
    """ dynamic options group """
    delimiter: Optional[str] = None
    """ "," # Splice character """
    labelField: Optional[str] = None
    """ "label" # option label field """
    valueField: Optional[str] = None
    """ "value" # option value field """
    joinValues: Optional[bool] = None
    """ True # splice values """
    extractValue: Optional[bool] = None
    """ False # extract value """
    columnsCount: Optional[int] = None
    """ 1 # How many columns to display options by, default is one column """
    checkAll: Optional[bool] = None
    """ False # If or not checkAll is supported """
    inline: Optional[bool] = None
    """ True # Whether to display as one line """
    defaultCheckAll: Optional[bool] = None
    """ False # Whether to check all by default """
    creatable: Optional[bool] = None
    """ False # New option """
    createBtnLabel: Optional[str] = None
    """ "Add option" # Add option """
    addControls: Optional[List[FormItem]] = None
    """ Customize the new form item """
    addApi: Optional[MSA_UI_API] = None
    """ Configure the add options interface """
    editable: Optional[bool] = None
    """ False # Edit options """
    editControls: Optional[List[FormItem]] = None
    """ Customize edit form items """
    editApi: Optional[MSA_UI_API] = None
    """ Configure the edit options interface """
    removable: Optional[bool] = None
    """ False # Remove options """
    deleteApi: Optional[MSA_UI_API] = None
    """ Configure the delete option interface """


class InputCity(FormItem):
    """city selector"""

    type: str = "location-city"
    allowCity: Optional[bool] = None
    """ True # Allow city selection """
    allowDistrict: Optional[bool] = None
    """ True # Allow district selection """
    searchable: Optional[bool] = None
    """ False # Whether or not the search box is available """
    extractValue: Optional[bool] = None
    """ True # whether to extract the value, if set to false the value format will become an object containing code, province, city and district text information. """


class InputColor(FormItem):
    """color picker"""

    type: str = "input-color"
    format: Optional[str] = None
    """ "hex" # Please choose hex, hls, rgb or rgba. """
    presetColors: Optional[List[str]] = None
    """ "selector preset color values" # default color at the bottom of the selector, if the array is empty, no default color is shown """
    allowCustomColor: Optional[bool] = None
    """ True # When false, only colors can be selected, use presetColors to set the color selection range """
    clearable: Optional[bool] = None
    """ "label" # whether to show clear button """
    resetValue: Optional[str] = None
    """ "" # After clearing, the form item value is adjusted to this value """


class Combo(FormItem):
    """combo"""

    type: str = "combo"
    formClassName: Optional[str] = None
    """ class name of a single group of form items """
    addButtonClassName: Optional[str] = None
    """ Add button CSS class name """
    items: Optional[List[FormItem]] = None
    """ Combined form items to be displayed 
    items[x].columnClassName: Optional[str] = None # The class name of the column with which to configure the column width. Default is evenly distributed. 
    items[x].unique: Optional[bool] = None # Set whether the current column value is unique, i.e. no duplicate selections are allowed. """
    noBorder: bool = False
    """ Whether to show border for a single group of table items """
    scaffold: dict = {}
    """ The initial value of a single table item """
    multiple: bool = False
    """ Whether or not to multi-select """
    multiLine: bool = False
    """ Default is to display a row horizontally, set it to display vertically """
    minLength: Optional[int] = None
    """ The minimum number of items to add """
    maxLength: Optional[int] = None
    """ The maximum number of items to add """
    flat: bool = False
    """ Whether to flatten the results (remove the name), only valid if the length of items is 1 and multiple is true. """
    joinValues: bool = True
    """ Defaults to true when flattening is on, whether to send to the backend as a delimiter, otherwise as an array. """
    delimiter: Optional[str] = None
    """ "False" # What delimiter to use when flattening is on and joinValues is true. """
    addable: bool = False
    """ Whether to add """
    addButtonText: Optional[str] = None
    """ "Add" # Add button text """
    removable: bool = False
    """ If or not it can be removed """
    deleteApi: Optional[MSA_UI_API] = None
    """ If configured, an api will be sent before deletion, and the deletion will be completed only if the request is successful """
    deleteConfirmText: Optional[str] = None
    """ "Confirm to delete?" """
    """ Only when deleteApi is configured does it take effect! Used to do user confirmation when deleting """
    draggable: bool = False
    """ whether draggable sorting is possible, note that when draggable sorting is enabled, there will be an additional $id field """
    draggableTip: Optional[str] = None
    """ "Can be reordered by dragging the [swap] button in each row" # Text to indicate draggable """
    subFormMode: Optional[str] = None
    """ "normal" # Optional normal, horizontal, inline """
    placeholder: Optional[str] = None
    """ "``" # Show when there is no member """
    canAccessSuperData: bool = False
    """ Specifies whether the data from the upper level can be automatically fetched and mapped to form items """
    conditions: Optional[Dict] = None
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
        label: Optional[str] = None
        """ Name of the field. """
        placeholder: Optional[str] = None
        """ Placeholder """
        operators: Optional[List[str]] = None
        """ Configure to override if you don't want that many. """

        """ Defaults to ['equal','not_equal','is_empty','is_not_empty','like','not_like','starts_with','ends_with'] """
        defaultOp: Optional[str] = None
        """ default to "equal" """

    class Text(Field):
        """text"""

    class Number(Field):
        """number"""

        type: str = "number"
        minimum: Optional[float] = None
        """ minimum """
        maximum: Optional[float] = None
        """ maximum value """
        step: Optional[float] = None
        """ step length """

    class Date(Field):
        """date"""

        type: str = "date"
        defaultValue: Optional[str] = None
        """ default value """
        format: Optional[str] = None
        """ default "YYYY-MM-DD" value format """
        inputFormat: Optional[str] = None
        """ Default "YYYY-MM-DD" date format for display. """

    class Datetime(Date):
        """datetime"""

        type: str = "datetime"
        timeFormat: Optional[str] = None
        """ Default "HH:mm" time format, determines which input boxes are available. """

    class Time(Date):
        """time"""

        type: str = "datetime"

    class Select(Field):
        """Dropdown selection"""

        type: str = "select"
        options: Optional[MSAOptionsNode] = None
        """ list of options, Array<{label: string, value: any}> """
        source: Optional[MSA_UI_API] = None
        """ Dynamic options, please configure api. """
        searchable: Optional[bool] = None
        """ If or not searchable """
        autoComplete: Optional[MSA_UI_API] = None
        """ AutoComplete will be called after each new input, and will return updated options according to the interface. """

    type: str = "condition-builder"
    fields: Optional[List[Field]] = None
    """ is an array type, each member represents an optional field, supports multiple layers, configuration example """
    className: Optional[str] = None
    """ outer dom class name """
    fieldClassName: Optional[str] = None
    """ The class name of the input field """
    source: Optional[str] = None
    """ pull configuration items via remote """


class Editor(FormItem):
    """Code Editor"""

    type: str = "editor"
    language: Optional[str] = None
    """ "javascript" # Language highlighted by the editor, supported by the ${xxx} variable bat, c, coffeescript, cpp, csharp, css, dockerfile, fsharp, go, handlebars, html, ini, java 
    javascript, json, less, lua, markdown, msdax, objective-c, php, plaintext, postiats, powershell,  pug, python, r, razor, ruby, sb, scss, shell, sol, sql, swift, typescript, vb, xml, yaml """
    size: Optional[str] = None
    """ "md" # editor height, can be md, lg, xl, xxl """
    allowFullscreen: Optional[bool] = None
    """ False # switch to show full screen mode or not """
    options: Optional[Dict] = None
    """ other configurations of monaco editor, such as whether to display line numbers, etc., please refer to here, but can not set readOnly, read-only mode need to use disabled: true """


class Markdown(MSAUINode):
    """Markdown rendering"""

    type: str = "markdown"
    name: Optional[str] = None
    """ Field name, specifying the key of the form item when it is submitted """
    value: Optional[Union[int, str]] = None
    """ The value of the field """
    className: Optional[str] = None
    """ The outermost class name of the form """
    src: Optional[MSA_UI_API] = None
    """ External address """
    options: Optional[Dict] = None
    """ html, whether html tags are supported, default false; linkify, whether to automatically recognize links, default is true; breaks, whether carriage return is line feed, default false """


class InputFile(FormItem):
    """FileUpload"""

    type: str = "input-file"
    receiver: Optional[MSA_UI_API] = None
    """ Upload file interface """
    accept: Optional[str] = None
    """ "text/plain" # Only plain text is supported by default, to support other types, please configure this attribute to have the file suffix .xxx """
    asBase64: Optional[bool] = None
    """ False # Assign the file as base64 to the current component """
    asBlob: Optional[bool] = None
    """ False # Assign the file to the current component in binary form """
    maxSize: Optional[int] = None
    """ No limit by default, when set, files larger than this value will not be allowed to be uploaded. The unit is B """
    maxLength: Optional[int] = None
    """ No limit by default, when set, only the specified number of files will be allowed to be uploaded at a time. """
    multiple: Optional[bool] = None
    """ False # Whether to select multiple. """
    joinValues: Optional[bool] = None
    """ True # Splice values """
    extractValue: Optional[bool] = None
    """ False # Extract the value """
    delimiter: Optional[str] = None
    """ "," # Splice character """
    autoUpload: Optional[bool] = None
    """ True # Automatically start uploading after no selection """
    hideUploadButton: Optional[bool] = None
    """ False # Hide the upload button """
    stateTextMap: Optional[Dict] = None
    """ Upload state text, Default: {init: '', pending: 'Waiting for upload', uploading: 'Uploading', error: 'Upload error', uploaded: 'Uploaded',ready: ''} """
    fileField: Optional[str] = None
    """ "file" # You can ignore this attribute if you don't want to store it yourself. """
    nameField: Optional[str] = None
    """ "name" # Which field the interface returns to identify the file name """
    valueField: Optional[str] = None
    """ "value" # Which field is used to identify the value of the file """
    urlField: Optional[str] = None
    """ "url" # The field name of the file download address. """
    btnLabel: Optional[str] = None
    """ The text of the upload button """
    downloadUrl: Optional[Union[str, bool]] = None
    """ Version 1.1.6 starts to support post:http://xxx.com/${value} this way,
    The default display of the file path will support direct download, you can support adding a prefix such as: http://xx.dom/filename= , if you do not want this, you can set the current configuration item to false. """
    useChunk: Optional[bool] = None
    """ The server where msa_ui is hosted restricts the file upload size to 10M, so msa_ui will automatically change to chunk upload mode when the user selects a large file. """
    chunkSize: Optional[int] = None
    """ 5 * 1024 * 1024 # chunk size """
    startChunkApi: Optional[MSA_UI_API] = None
    """ startChunkApi """
    chunkApi: Optional[MSA_UI_API] = None
    """ chunkApi """
    finishChunkApi: Optional[MSA_UI_API] = None
    """ finishChunkApi """
    autoFill: Optional[Dict[str, str]] = None
    """ After a successful upload, you can configure autoFill to populate a form item with the values returned by the upload interface (not supported under non-form for now) """


class InputExcel(FormItem):
    """Parse Excel"""

    type: str = "input-excel"
    allSheets: Optional[bool] = None
    """ False # whether to parse all sheets """
    parseMode: Optional[str] = None
    """ 'array' or 'object' parse mode """
    includeEmpty: Optional[bool] = None
    """ True # whether to include null values """
    plainText: Optional[bool] = None
    """ True # Whether to parse as plain text """


class InputTable(FormItem):
    """table"""

    type: str = "input-table"
    """ Specify as Table renderer """
    showIndex: Optional[bool] = None
    """ False # Show serial number """
    perPage: Optional[int] = None
    """ Set how many data to display on a page. 10 """
    addable: Optional[bool] = None
    """ False # Whether to add a row """
    editable: Optional[bool] = None
    """ False # Whether to edit """
    removable: Optional[bool] = None
    """ False # Whether to remove """
    showAddBtn: Optional[bool] = None
    """ True # Whether to show the add button """
    addApi: Optional[MSA_UI_API] = None
    """ The MSA_UI_API to submit when adding """
    updateApi: Optional[MSA_UI_API] = None
    """ The MSA_UI_API submitted when modifying """
    deleteApi: Optional[MSA_UI_API] = None
    """ MSA_UI_API submitted when deleting """
    addBtnLabel: Optional[str] = None
    """ Add button name """
    addBtnIcon: Optional[str] = None
    """ "plus" # Add button icon """
    copyBtnLabel: Optional[str] = None
    """ Copy button text """
    copyBtnIcon: Optional[str] = None
    """ "copy" # Copy the button icon """
    editBtnLabel: Optional[str] = None
    """ "" # Edit button name """
    editBtnIcon: Optional[str] = None
    """ "pencil" # editBtnIcon """
    deleteBtnLabel: Optional[str] = None
    """ "" # Delete the button name """
    deleteBtnIcon: Optional[str] = None
    """ "minus" # Delete the button icon """
    confirmBtnLabel: Optional[str] = None
    """ "" # Confirm edit button name """
    confirmBtnIcon: Optional[str] = None
    """ "check" # Confirm edit button icon """
    cancelBtnLabel: Optional[str] = None
    """ "" # Cancel the edit button name """
    cancelBtnIcon: Optional[str] = None
    """ "times" # Cancel the edit button icon """
    needConfirm: Optional[bool] = None
    """ True # whether to confirm the operation, can be used to control the interaction of the form """
    canAccessSuperData: Optional[bool] = None
    """ False # Whether to access parent data, that is, the same level of data in the form, usually need to be used with strictMode """
    strictMode: Optional[bool] = None
    """ True # For performance, the default value changes of other form items will not update the current form, sometimes you need to enable this in order to synchronize access to other form fields. """
    columns: Optional[List] = None
    """ "[]" # Column information, columns[x].quickEdit: boolean|object = None # Used in conjunction with editable being true, 
    # columns[x].quickEditOnUpdate: boolean|object = None # can be used to distinguish between new mode and update mode editing configuration """


class InputGroup(FormItem):
    """InputBoxGroup"""

    type: str = "input-group"
    className: Optional[str] = None
    """ CSS class name """
    body: Optional[List[FormItem]] = None
    """ collection of form items """


class Group(InputGroup):
    """Form Item Group"""

    type: str = "group"
    mode: Optional[DisplayModeEnum] = None
    """ Display default, same mode as in Form """
    gap: Optional[str] = None
    """ spacing between form items, optional: xs, sm, normal """
    direction: Optional[str] = None
    """ "horizontal" # You can configure whether to display horizontally or vertically. The corresponding configuration items are: vertical, horizontal """


class InputImage(FormItem):
    """Image Upload"""

    class CropInfo(MSABaseUIModel):
        aspectRatio: Optional[float] = None
        """ Crop ratio. Floating point type, default 1 i.e. 1:1, if you want to set 16:9 please set 1.77777777777777 i.e. 16 / 9. """
        rotatable: Optional[bool] = None
        """ False # If or not rotatable when cropping. """
        scalable: Optional[bool] = None
        """ False # Whether to scale when cropping """
        viewMode: Optional[int] = None
        """ 1 # View mode when cropping, 0 is no limit """

    class Limit(MSABaseUIModel):
        width: Optional[int] = None
        """ Limit the width of the image. """
        height: Optional[int] = None
        """ Limit the height of the image. """
        minWidth: Optional[int] = None
        """ Limit the minimum width of the image. """
        minHeight: Optional[int] = None
        """ Limit the minimum height of the image. """
        maxWidth: Optional[int] = None
        """ Limit the maximum width of the image. """
        maxHeight: Optional[int] = None
        """ Limit the maximum height of the image. """
        aspectRatio: Optional[float] = None
        """ Limit the aspect ratio of the image, the format is floating point number, default 1 is 1:1. 
        If you want to set 16:9, please set 1.7777777777777777 i.e. 16 / 9. If you don't want to limit the ratio, please set the empty string. """

    type: str = "input-image"
    receiver: Optional[MSA_UI_API] = None
    """ Upload file interface """
    accept: Optional[str] = None
    """ ".jpeg,.jpg,.png,.gif" # Supported image type formats, please configure this attribute as image suffix, e.g. .jpg, .png """
    maxSize: Optional[int] = None
    """ No limit by default, when set, file size larger than this value will not be allowed to upload. The unit is B """
    maxLength: Optional[int] = None
    """ No limit by default, when set, only the specified number of files will be allowed to be uploaded at once. """
    multiple: Optional[bool] = None
    """ False # Whether to select multiple. """
    joinValues: Optional[bool] = None
    """ True # Splice values """
    extractValue: Optional[bool] = None
    """ False # Extract the value """
    delimiter: Optional[str] = None
    """ "," # Splice character """
    autoUpload: Optional[bool] = None
    """ True # Automatically start uploading after no selection """
    hideUploadButton: Optional[bool] = None
    """ False # Hide the upload button """
    fileField: Optional[str] = None
    """ "file" # You can ignore this property if you don't want to store it yourself. """
    crop: Optional[Union[bool, CropInfo]] = None
    """ Used to set if crop is supported. """
    cropFormat: Optional[str] = None
    """ "image/png" # Crop file format """
    cropQuality: Optional[int] = None
    """ 1 # quality of the crop file format, for jpeg/webp, takes values between 0 and 1 """
    limit: Optional[Limit] = None
    """ Limit the size of the image, won't allow uploads beyond that. """
    frameImage: Optional[str] = None
    """ Default placeholder image address """
    fixedSize: Optional[bool] = None
    """ Whether to enable fixed size, if so, set fixedSizeClassName at the same time """
    fixedSizeClassName: Optional[str] = None
    """ When fixedSize is enabled, the display size is controlled by this value. """

    """ For example, if h-30, i.e., the height of the image box is h-30, msa_ui will automatically scale the width of the default image position, and the final uploaded image will be scaled according to this size. """
    autoFill: Optional[Dict[str, str]] = None
    """ After successful upload, you can configure autoFill to fill the value returned by the upload interface into a form item (not supported under non-form) """


class LocationPicker(FormItem):
    """Location"""

    type: str = "location-picker"
    vendor: str = "baidu"
    """ map vendor, currently only implemented Baidu maps """
    ak: str = ...
    """ Baidu map ak # Register at: http://lbsyun.baidu.com/ """
    clearable: Optional[bool] = None
    """ False # Whether the input box is clearable """
    placeholder: Optional[str] = None
    """ "Please select a location" # Default prompt """
    coordinatesType: Optional[str] = None
    """ "bd09" # Default is Baidu coordinates, can be set to 'gcj02' """


class InputNumber(FormItem):
    """Number input box"""

    type: str = "input-number"
    min: Optional[Union[int, MSAUITemplate]] = None
    """ min """
    max: Optional[Union[int, MSAUITemplate]] = None
    """ max """
    step: Optional[int] = None
    """ step size """
    precision: Optional[int] = None
    """ precision, i.e., the number of decimal places """
    showSteps: Optional[bool] = None
    """ True # Whether to show the up and down click buttons """
    prefix: Optional[str] = None
    """ prefix """
    suffix: Optional[str] = None
    """ suffix """
    kilobitSeparator: Optional[bool] = None
    """ thousand separator """


class Picker(FormItem):
    """List Picker"""

    type: str = "picker"
    """ List picker, similar in function to Select, but it can display more complex information. """
    size: Optional[Union[str, SizeEnum]] = None
    """ Supports: xs, sm, md, lg, xl, full """
    options: Optional[MSAOptionsNode] = None
    """ Options group """
    source: Optional[MSA_UI_API] = None
    """ Dynamic options group """
    multiple: Optional[bool] = None
    """ Whether to be multiple options. """
    delimiter: Optional[bool] = None
    """ False # Splice character """
    labelField: Optional[str] = None
    """ "label" # option label field """
    valueField: Optional[str] = None
    """ "value" # Option value field """
    joinValues: Optional[bool] = None
    """ True # splice values """
    extractValue: Optional[bool] = None
    """ False # extract value """
    autoFill: Optional[Dict] = None
    """ AutoFill """
    modalMode: Optional[Literal["dialog", "drawer"]] = None
    """ "dialog" # Set dialog or drawer to configure popup method. """
    pickerSchema: Optional[Union["CRUD", MSAUISchemaNode]] = None
    """ "{mode: 'list', listItem: {title: '${label}'}}" i.e. rendering with List type to display list information. See CRUD for more configuration """
    embed: Optional[bool] = None
    """ False # Whether to use inline mode """


class Switch(FormItem):
    """switch"""

    type: str = "switch"
    option: Optional[str] = None
    """ option description """
    onText: Optional[str] = None
    """ Text when on """
    offText: Optional[str] = None
    """ Text when off """
    trueValue: Optional[Any] = None
    """ "True" # Identifies a true value """
    falseValue: Optional[Any] = None
    """ "false" # Identifies a false value """


class Static(FormItem):
    """Static display/label"""

    type: str = "static"
    """ support for displaying other non-form items by configuring the type as static-xxx component static-json|static-datetime """

    class Json(FormItem):
        type: str = "static-json"
        value: Union[dict, str]

    class Datetime(FormItem):
        """Show date"""

        type: str = "static-datetime"
        value: Union[int, str]
        """ support 10-bit timestamp: 1593327764 """


class InputText(FormItem):
    """input-box"""

    type: str = "input-text"
    """ input-text|input-url|input-email|input-password|divider """
    options: Optional[Union[List[str], List[dict]]] = None
    """ option group """
    source: Optional[Union[str, MSA_UI_API]] = None
    """ dynamic options group """
    autoComplete: Optional[Union[str, MSA_UI_API]] = None
    """ autoComplete """
    multiple: Optional[bool] = None
    """ Whether to multi-select """
    delimiter: Optional[str] = None
    """ Splice character "," """
    labelField: Optional[str] = None
    """ option label field "label" """
    valueField: Optional[str] = None
    """ option value field "value" """
    joinValues: Optional[bool] = None
    """ True # Splice values """
    extractValue: Optional[bool] = None
    """ extract value """
    addOn: Optional[MSAUISchemaNode] = None
    """ Input box add-on, such as with a prompt text, or with a submit button. """
    trimContents: Optional[bool] = None
    """ Whether to remove the first and last blank text. """
    creatable: Optional[bool] = None
    """ If or not creatable, default is yes, unless set to false which means that only the value in the option can be selected. """
    clearable: Optional[bool] = None
    """ Whether to clear or not """
    resetValue: Optional[str] = None
    """ Set the value given by this configuration item after clearing. """
    prefix: Optional[str] = None
    """ prefix """
    suffix: Optional[str] = None
    """ suffix """
    showCounter: Optional[bool] = None
    """ Whether to show the counter """
    minLength: Optional[int] = None
    """ Limit the minimum number of words """
    maxLength: Optional[int] = None
    """ Limit the maximum number of words """


class InputPassword(InputText):
    """Password input box"""

    type: str = "input-password"


class InputRichText(FormItem):
    """rich-text editor"""

    type: str = "input-rich-text"
    saveAsUbb: Optional[bool] = None
    """ whether to save as ubb format """
    receiver: Optional[MSA_UI_API] = None
    """ '' # default image save MSA_UI_API """
    videoReceiver: Optional[MSA_UI_API] = None
    """ '' # Default video saving MSA_UI_API """
    size: Optional[str] = None
    """ Size of the box, can be set to md or lg """
    options: Optional[Dict] = None
    """ Need to refer to tinymce or froala's documentation """
    buttons: Optional[List[str]] = None
    """ froala specific, configure the buttons to be displayed, tinymce can set the toolbar string with the preceding options """
    vendor: Optional[str] = None
    """ "vendor": "froala" , configured to use the froala editor """


class Select(FormItem):
    """dropdown box"""

    type: str = "select"
    options: Optional[MSAOptionsNode] = None
    """ options group """
    source: Optional[MSA_UI_API] = None
    """ dynamic options group """
    autoComplete: Optional[MSA_UI_API] = None
    """ auto prompt complement """
    delimiter: Optional[Union[bool, str]] = None
    """ False # Splice character """
    labelField: Optional[str] = None
    """ "label" # option label field """
    valueField: Optional[str] = None
    """ "value" # option value field """
    joinValues: Optional[bool] = None
    """ True # splice values """
    extractValue: Optional[bool] = None
    """ False # extract value """
    checkAll: Optional[bool] = None
    """ False # Whether to support select all """
    checkAllLabel: Optional[str] = None
    """ "Select All" # Text to select all """
    checkAllBySearch: Optional[bool] = None
    """ False # Only check all items that are hit when there is a search """
    defaultCheckAll: Optional[bool] = None
    """ False # defaultCheckAll or not """
    creatable: Optional[bool] = None
    """ False # Add option """
    multiple: Optional[bool] = None
    """ False # Multi-select """
    searchable: Optional[bool] = None
    """ False # Searchable """
    createBtnLabel: Optional[str] = None
    """ "Add option" # Add option """
    addControls: Optional[List[FormItem]] = None
    """ Customize the new form item """
    addApi: Optional[MSA_UI_API] = None
    """ Configure the add options interface """
    editable: Optional[bool] = None
    """ False # Edit options """
    editControls: Optional[List[FormItem]] = None
    """ Customize edit form items """
    editApi: Optional[MSA_UI_API] = None
    """ Configure the edit options interface """
    removable: Optional[bool] = None
    """ False # Remove options """
    deleteApi: Optional[MSA_UI_API] = None
    """ Configure the delete option interface """
    autoFill: Optional[Dict] = None
    """ AutoFill """
    menuTpl: Optional[str] = None
    """ Support for configuring custom menus """
    clearable: Optional[bool] = None
    """ Whether clearing is supported in radio mode """
    hideSelected: Optional[bool] = None
    """ False # Hide the selected option """
    mobileClassName: Optional[str] = None
    """ Mobile floating class name """
    selectMode: Optional[str] = None
    """ Optional: group, table, tree, chained, associated, respectively: list form, table form, tree select form, tree select form
    cascade selection form, association selection form (the difference with cascade selection is that the cascade is infinite, while the association is only one level, the left side of the association can be a tree). """
    searchResultMode: Optional[str] = None
    """ If not set, the value of selectMode will be used, can be configured separately, refer to selectMode, determine the display of search results. """
    columns: Optional[List[dict]] = None
    """ When the display form is table can be used to configure which columns to display, similar to the columns in the table configuration, but only the display function. """
    leftOptions: Optional[List[dict]] = None
    """ Used to configure the left set of options when the display is associated. """
    leftMode: Optional[str] = None
    """ Configure the left option set when the display is associated, supports list or tree. default is list. rightMode: Optional[str] = None # Configure the left option set when the display is associated. """
    rightMode: Optional[str] = None
    """ Used to configure the right option set when the display is associated, optionally: list, table, tree, chained. """


class NestedSelect(Select):
    """Cascading selector"""

    type: str = "nested-select"
    cascade: Optional[bool] = None
    """ False # When set true, child nodes are not automatically selected when the parent node is selected. """
    withChildren: Optional[bool] = None
    """ False # When set true, the value of the parent node will contain the value of the child node when selected, otherwise only the value of the parent node will be kept. """
    onlyChildren: Optional[bool] = None
    """ False # When multi-select, when the parent node is selected, the value will include only its children in the value. """
    searchPromptText: Optional[str] = None
    """ "Enter content to search" # Search box placeholder text """
    noResultsText: Optional[str] = None
    """ "No results found" # Text when no results are found """
    hideNodePathLabel: Optional[bool] = None
    """ False # Whether to hide the path of the selected node in the selection box label information """
    onlyLeaf: Optional[bool] = None
    """ False # Only allow leaf nodes to be selected """


class Textarea(FormItem):
    """Multi-line text input box"""

    type: str = "textarea"
    minRows: Optional[int] = None
    """ minimum number of rows """
    maxRows: Optional[int] = None
    """ maximum number of lines """
    trimContents: Optional[bool] = None
    """ whether to remove first and last blank text """
    readOnly: Optional[bool] = None
    """ whether to read only """
    showCounter: bool = True
    """ Whether to show the counter """
    minLength: Optional[int] = None
    """ Limit the minimum number of words """
    maxLength: Optional[int] = None
    """ Limit the maximum number of words """


class InputMonth(FormItem):
    """month"""

    type: str = "input-month"
    value: Optional[str] = None
    """ Default value """
    format: Optional[str] = None
    """ "X" # month selector value format, see moment for more format types """
    inputFormat: Optional[str] = None
    """ "YYYY-MM" # Month selector display format, i.e. timestamp format, see moment for more format types """
    placeholder: Optional[str] = None
    """ "Please select a month" # Placeholder text """
    clearable: Optional[bool] = None
    """ True # clearable or not """


class InputTime(FormItem):
    """time"""

    type: str = "input-time"
    value: Optional[str] = None
    """ Default value """
    timeFormat: Optional[str] = None
    """ "HH:mm" # time selector value format, see moment for more format types """
    format: Optional[str] = None
    """ "X" # Time picker value format, see moment for more format types """
    inputFormat: Optional[str] = None
    """ "HH:mm" # Time picker display format, i.e. timestamp format, see moment for more format types """
    placeholder: Optional[str] = None
    """ "Please select time" # Placeholder text """
    clearable: Optional[bool] = None
    """ True # clearable or not """
    timeConstraints: Optional[Dict] = None
    """ True # See also: react-datetime """


class InputDatetime(FormItem):
    """date"""

    type: str = "input-datetime"
    value: Optional[str] = None
    """ Default value """
    format: Optional[str] = None
    """ "X" # Date time selector value format, see documentation for more format types """
    inputFormat: Optional[str] = None
    """ "YYYY-MM-DD HH:mm:ss" # Date and time picker display format, i.e. timestamp format, see documentation for more format types """
    placeholder: Optional[str] = None
    """ "Please select the date and time" # Placeholder text """
    shortcuts: Optional[str] = None
    """ Date and time shortcuts """
    minDate: Optional[str] = None
    """ Limit the minimum date and time """
    maxDate: Optional[str] = None
    """ Limit the maximum date and time """
    utc: Optional[bool] = None
    """ False # Save utc value """
    clearable: Optional[bool] = None
    """ True # clearable or not """
    embed: Optional[bool] = None
    """ False # Whether to inline """
    timeConstraints: Optional[Dict] = None
    """ True # See also: react-datetime """


class InputDate(FormItem):
    """date"""

    type: str = "input-date"
    value: Optional[str] = None
    """ Default value """
    format: Optional[str] = None
    """ "X" # Date picker value format, see documentation for more format types """
    inputFormat: Optional[str] = None
    """ "YYYY-DD-MM" # Date picker display format, i.e. timestamp format, see documentation for more format types """
    placeholder: Optional[str] = None
    """ "Please select a date" # Placeholder text """
    shortcuts: Optional[str] = None
    """ Date shortcuts """
    minDate: Optional[str] = None
    """ Restrict the minimum date """
    maxDate: Optional[str] = None
    """ Limit the maximum date """
    utc: Optional[bool] = None
    """ False # Save utc value """
    clearable: Optional[bool] = None
    """ True # clearable or not """
    embed: Optional[bool] = None
    """ False # Whether to inline mode """
    timeConstraints: Optional[Dict] = None
    """ True # See also: react-datetime """
    closeOnSelect: Optional[bool] = None
    """ False # Whether to close the selection box immediately after tapping a date """
    schedules: Optional[Union[list, str]] = None
    """ Show schedules in calendar, can set static data or take data from context, className reference background color """
    scheduleClassNames: Optional[List[str]] = None
    """ "['bg-warning','bg-danger','bg-success','bg-info','bg-secondary']" """

    """ The color to display the schedule in the calendar, referencing the background color """
    scheduleAction: Optional[MSAUISchemaNode] = None
    """ Custom schedule display """
    largeMode: Optional[bool] = None
    """ False # Zoom mode """


class InputTimeRange(FormItem):
    """TimeRange"""

    type: str = "input-time-range"
    timeFormat: Optional[str] = None
    """ "HH:mm" # time range selector value format """
    format: Optional[str] = None
    """ "HH:mm" # time range selector value format """
    inputFormat: Optional[str] = None
    """ "HH:mm" # Time range selector display format """
    placeholder: Optional[str] = None
    """ "Please select a time range" # Placeholder text """
    clearable: Optional[bool] = None
    """ True # clearable or not """
    embed: Optional[bool] = None
    """ False # Whether inline mode """


class InputDatetimeRange(InputTimeRange):
    """DateTimeRange"""

    type: str = "input-datetime-range"
    ranges: Optional[Union[str, List[str]]] = None
    """ "yesterday,7daysago,prevweek,thismonth,prevmonth,prevquarter" Date range shortcut. 
        optional: today,yesterday,1dayago,7daysago,30daysago,90daysago,prevweek,thismonth,thisquarter,prevmonth,prevquarter """
    minDate: Optional[str] = None
    """ Limit the minimum date and time, use the same as limit range """
    maxDate: Optional[str] = None
    """ Limit the maximum date and time, use the same as limit range """
    utc: Optional[bool] = None
    """ False # Save UTC value """


class InputDateRange(InputDatetimeRange):
    """dateRange"""

    type: str = "input-date-range"
    minDuration: Optional[str] = None
    """ Limit the minimum span, e.g. 2days """
    maxDuration: Optional[str] = None
    """ Limit the maximum span, e.g. 1year """


class InputMonthRange(InputDateRange):
    """MonthRange"""

    type: str = "input-month-range"


class Transfer(FormItem):
    """shuttle"""

    type: Literal[
        "transfer", "transfer-picker", "tabs-transfer", "tabs-transfer-picker"
    ] = "transfer"
    options: Optional[MSAOptionsNode] = None
    """ options group """
    source: Optional[MSA_UI_API] = None
    """ dynamic options group """
    delimiter: Optional[str] = None
    """ "False" # Splice character """
    joinValues: Optional[bool] = None
    """ True # Splice values """
    extractValue: Optional[bool] = None
    """ False # extract value """
    searchable: Optional[bool] = None
    """ False # When set to true means that options can be retrieved by partial input. """
    searchApi: Optional[MSA_UI_API] = None
    """ You can set an api if you want to search through the interface. """
    statistics: Optional[bool] = None
    """ True # Whether to display statistics """
    selectTitle: Optional[str] = None
    """ "Please select" # The title text on the left side """
    resultTitle: Optional[str] = None
    """ "Current selection" # The title text of the right result """
    sortable: Optional[bool] = None
    """ False # Results can be sorted by dragging and dropping """
    selectMode: Optional[str] = None
    """ "list" # Optional: list, table, tree, cascaded, associated. respectively: list form, table form, tree selection form, tree selection form 
    cascade selection form, associated selection form (the difference with cascade selection is that cascade is infinite, while associated is only one level, and the left side of associated can be a tree). """
    searchResultMode: Optional[str] = None
    """ If not set will use the value of selectMode, can be configured separately, refer to selectMode, determine the search results display form. """
    columns: Optional[List[dict]] = None
    """ When the display form is table can be used to configure which columns to display, similar to the columns in the table configuration, but only the display function. """
    leftOptions: Optional[List[dict]] = None
    """ Used to configure the left set of options when the display is associated. """
    leftMode: Optional[str] = None
    """ Configure the left option set when the display is associated, supports list or tree. default is list. rightMode: Optional[str] = None # Configure the left option set when the display is associated. """
    rightMode: Optional[str] = None
    """ Use to configure the right option set when the display is associated, options are: list, table, tree, chained. """
    menuTpl: Optional[MSAUISchemaNode] = None
    """ Used to customize the option display. """
    valueTpl: Optional[MSAUISchemaNode] = None
    """ Used to customize the display of values """


class TransferPicker(Transfer):
    """shuttlePicker"""

    type: str = "transfer-picker"


class TabsTransfer(Transfer):
    """Combination shuttle"""

    type: str = "tabs-transfer"


class TabsTransferPicker(Transfer):
    """Combination shuttle selector"""

    type: str = "tabs-transfer-picker"


class InputTree(FormItem):
    """tree selector box"""

    type: str = "input-tree"
    options: Optional[MSAOptionsNode] = None
    """ options group """
    source: Optional[MSA_UI_API] = None
    """ dynamic options group """
    autoComplete: Optional[MSA_UI_API] = None
    """ auto prompt complement """
    multiple: Optional[bool] = None
    """ False # Whether to multiple select """
    delimiter: Optional[str] = None
    """ "False" # Splice character """
    labelField: Optional[str] = None
    """ "label" # option label field """
    valueField: Optional[str] = None
    """ "value" # option value field """
    iconField: Optional[str] = None
    """ "icon" # Icon value field """
    joinValues: Optional[bool] = None
    """ True # join values """
    extractValue: Optional[bool] = None
    """ False # extract value """
    creatable: Optional[bool] = None
    """ False # Add options """
    addControls: Optional[List[FormItem]] = None
    """ Customize the new form items """
    addApi: Optional[MSA_UI_API] = None
    """ Configure the add options interface """
    editable: Optional[bool] = None
    """ False # Edit options """
    editControls: Optional[List[FormItem]] = None
    """ Customize edit form items """
    editApi: Optional[MSA_UI_API] = None
    """ Configure the edit options interface """
    removable: Optional[bool] = None
    """ False # Remove options """
    deleteApi: Optional[MSA_UI_API] = None
    """ Configure the delete option interface """
    searchable: Optional[bool] = None
    """ False # Searchable or not, only works if type is tree-select """
    hideRoot: Optional[bool] = None
    """ True # If you want to show a top node, set to false """
    rootLabel: Optional[bool] = None
    """ "top" # Useful when hideRoot is not false, to set the text of the top node. """
    showIcon: Optional[bool] = None
    """ True # Whether to show the icon """
    showRadio: Optional[bool] = None
    """ False # Whether to show radio buttons, multiple is valid when false. """
    initiallyOpen: Optional[bool] = None
    """ True # Set whether to expand all levels by default. """
    unfoldedLevel: Optional[int] = None
    """ 0 # Set the number of levels to be expanded by default, only effective if initiallyOpen is not true. """
    cascade: Optional[bool] = None
    """ False # Do not automatically select children when parent is selected. """
    withChildren: Optional[bool] = None
    """ False # When the parent node is selected, the value will contain the value of the child node, otherwise only the value of the parent node will be kept. """
    onlyChildren: Optional[bool] = None
    """ False # Whether to add only its children to the value when the parent node is selected in multiple selection. """
    rootCreatable: Optional[bool] = None
    """ False # Whether top-level nodes can be created """
    rootCreateTip: Optional[str] = None
    """ "Add first-level node" # Hover tip for creating top-level nodes """
    minLength: Optional[int] = None
    """ Minimum number of selected nodes """
    maxLength: Optional[int] = None
    """ Maximum number of nodes to select """
    treeContainerClassName: Optional[str] = None
    """ tree outermost container class name """
    enableNodePath: Optional[bool] = None
    """ False # Whether to enable node path mode """
    pathSeparator: Optional[str] = None
    """ "/" # Separator for node paths, takes effect when enableNodePath is true """
    deferApi: Optional[MSA_UI_API] = None
    """ For lazy loading, please configure defer to true, then configure deferApi to complete lazy loading """
    selectFirst: Optional[bool] = None


class TreeSelect(InputTree):
    """Tree Selector"""

    type: str = "tree-select"
    hideNodePathLabel: Optional[bool] = None
    """ Whether to hide the path of the selected node in the selection box label information """


class Image(MSAUINode):
    """image"""

    type: str = "image"
    """ "image" if in Table, Card and List; "static-image" if used as a static display in Form """
    className: Optional[str] = None
    """ Outer CSS class name """
    imageClassName: Optional[str] = None
    """ Image CSS class name """
    thumbClassName: Optional[str] = None
    """ Image thumbnail CSS class name """
    height: Optional[int] = None
    """ Image thumbnail height """
    width: Optional[int] = None
    """ Image scaling width """
    title: Optional[str] = None
    """ title """
    imageCaption: Optional[str] = None
    """ description """
    placeholder: Optional[str] = None
    """ Placeholder text """
    defaultImage: Optional[str] = None
    """ Image to display when no data is available """
    src: Optional[str] = None
    """ Thumbnail address """
    href: Optional[MSAUITemplate] = None
    """ External link address """
    originalSrc: Optional[str] = None
    """ Original image address """
    enlargeAble: Optional[bool] = None
    """ Support for enlarge preview """
    enlargeTitle: Optional[str] = None
    """ The title of the enlarged preview """
    enlargeCaption: Optional[str] = None
    """ Description of the enlarged preview """
    thumbMode: Optional[str] = None
    """ "contain" # Preview mode, optional: 'w-full', 'h-full', 'contain', 'cover' """
    thumbRatio: Optional[str] = None
    """ "1:1" # The ratio of the preview image, optional: '1:1', '4:3', '16:9' """
    imageMode: Optional[str] = None
    """ "thumb" # Image display mode, optional: 'thumb', 'original' i.e.: thumbnail mode or original image mode """


class Images(MSAUINode):
    """images collection"""

    type: str = "images"
    """ "images" if in Table, Card and List; "static-images" if used as a static display in Form """
    className: Optional[str] = None
    """ Outer CSS class name """
    defaultImage: Optional[str] = None
    """ Default image to display """
    value: Optional[Union[str, List[str], List[dict]]] = None
    """ array of images """
    source: Optional[str] = None
    """ data source """
    delimiter: Optional[str] = None
    """ "," # separator to split when value is a string """
    src: Optional[str] = None
    """ Address of the preview image, supports data mapping to get the image variables in the object """
    originalSrc: Optional[str] = None
    """ The address of the original image, supports data mapping to get the image variables in the object """
    enlargeAble: Optional[bool] = None
    """ Support enlarge preview """
    thumbMode: Optional[str] = None
    """ "contain" # preview image mode, optional: 'w-full', 'h-full', 'contain', 'cover' """
    thumbRatio: Optional[str] = None
    """ "1:1" # Preview ratio, optional: '1:1', '4:3', '16:9' """


class Carousel(MSAUINode):
    """Rotating image"""

    class Item(MSAUINode):
        image: Optional[str] = None
        """ Image link """
        href: Optional[str] = None
        """ link to the image's open URL """
        imageClassName: Optional[str] = None
        """ Image class name """
        title: Optional[str] = None
        """ Image title """
        titleClassName: Optional[str] = None
        """ Image title class name """
        description: Optional[str] = None
        """ Image description """
        descriptionClassName: Optional[str] = None
        """ Image description class name """
        html: Optional[str] = None
        """ HTML customization, same as Tpl """

    type: str = "carousel"
    """ Specify as Carousel renderer """
    className: Optional[str] = None
    """ "panel-default" # class name of outer Dom """
    options: Optional[List[Item]] = None
    """ "[]" # Rotating panel data """
    itemSchema: Optional[Dict] = None
    """ Custom schema to display data """
    auto: bool = True
    """ whether to rotate automatically """
    interval: Optional[str] = None
    """ "5s" # toggle animation interval """
    duration: Optional[str] = None
    """ "0.5s" # the duration of the toggle animation """
    width: Optional[str] = None
    """ "auto" # width """
    height: Optional[str] = None
    """ "200px" # height """
    controls: Optional[List[str]] = None
    """ "['dots','arrows']" # Show left and right arrows, bottom dots index """
    controlsTheme: Optional[str] = None
    """ "light" # Color of left and right arrows, bottom dot index, default light, dark mode available """
    animation: Optional[str] = None
    """ "fade" # Toggle animation effect, default fade, also slide mode """
    thumbMode: Optional[str] = None
    """ "cover"|"contain" # default image zoom mode """


class CRUD(MSAUINode):
    """add-delete"""

    class Messages(MSAUINode):
        fetchFailed: Optional[str] = None
        """ prompt when fetch fails """
        saveOrderFailed: Optional[str] = None
        """ Hint for failed save order """
        saveOrderSuccess: Optional[str] = None
        """ prompt for order success """
        quickSaveFailed: Optional[str] = None
        """ prompt for quick save failure """
        quickSaveSuccess: Optional[str] = None
        """ QuickSaveSuccess hint """

    type: str = "crud"
    """ type specifies the CRUD renderer """
    mode: Optional[str] = None
    """ "table" # "table", "cards" or "list" """
    title: Optional[str] = None
    """ "" # can be set to empty, when set to empty, there is no title bar """
    className: Optional[str] = None
    """ class name of the table's outer Dom """
    api: Optional[MSA_UI_API] = None
    """ The api used by CRUD to get the list data. """
    loadDataOnce: Optional[bool] = None
    """ Whether to load all data at once (front-end paging) """
    loadDataOnceFetchOnFilter: Optional[bool] = None
    """ True # Whether to re-request the api when filtering when loadDataOnce is enabled """
    source: Optional[str] = None
    """ Data mapping interface to return the value of a field, not set will default to use the interface to return ${items} or ${rows}, can also be set to the content of the upper-level data source """
    filter: Optional[Union[MSAUISchemaNode, Form]] = None
    """ Set a filter that will bring the data to the current mode to refresh the list when the form is submitted. """
    filterTogglable: Optional[bool] = None
    """ False # Whether to make the filter visible or invisible """
    filterDefaultVisible: Optional[bool] = None
    """ True # Sets whether the filter is visible by default. """
    initFetch: Optional[bool] = None
    """ True # Whether to pull data when initializing, only for cases with filter, no filter will pull data initially """
    interval: Optional[int] = None
    """ Refresh time (minimum 1000) """
    silentPolling: Optional[bool] = None
    """ Configure whether to hide loading animation when refreshing """
    stopAutoRefreshWhen: Optional[str] = None
    """ Configure the conditions for stopping the refresh via an expression """
    stopAutoRefreshWhenModalIsOpen: Optional[bool] = None
    """ Turn off auto refresh when there is a popup box, and resume when the popup box is closed """
    syncLocation: Optional[bool] = None
    """ False # Whether to sync the parameters of the filter condition to the address bar, !!! !!! may change the data type after turning on, can't pass fastpi data verification """
    draggable: Optional[bool] = None
    """ Whether to sort by drag and drop """
    itemDraggableOn: Optional[bool] = None
    """ Use an expression to configure whether draggable is sortable or not """
    saveOrderApi: Optional[MSA_UI_API] = None
    """ The api to save the sorting. """
    quickSaveApi: Optional[MSA_UI_API] = None
    """ The MSA_UI_API used for batch saving after quick editing. """
    quickSaveItemApi: Optional[MSA_UI_API] = None
    """ The MSA_UI_API used when the quick edit is configured to save in time. """
    bulkActions: Optional[List[Action]] = None
    """ List of bulk actions, configured so that the form can be checked. """
    defaultChecked: Optional[bool] = None
    """ Default whether to check all when bulk actions are available. """
    messages: Optional[Messages] = None
    """ Override the message prompt, if not specified, the message returned by the api will be used """
    primaryField: Optional[str] = None
    """ Set the ID field name.' id' """
    perPage: Optional[int] = None
    """ Set how many data to display on a page. 10 """
    defaultParams: Optional[Dict] = None
    """ Set the default filter default parameters, which will be sent to the backend together with the query """
    pageField: Optional[str] = None
    """ Set the pagination page number field name. "page" """
    perPageField: Optional[str] = None
    """ "perPage" # Set the field name of how many data to display on a paginated page. Note: Best used in conjunction with defaultParams, see the following example. """
    perPageAvailable: Optional[List[int]] = None
    """ [5, 10, 20, 50, 100] # Set how many data dropdown boxes are available for displaying on a page. """
    orderField: Optional[str] = None
    """ Set the name of the field used to determine the position, after setting the new order will be assigned to the field. """
    hideQuickSaveBtn: Optional[bool] = None
    """ Hide the top quick save prompt """
    autoJumpToTopOnPagerChange: Optional[bool] = None
    """ Whether to auto jump to the top when the page is cut. """
    syncResponse2Query: Optional[bool] = None
    """ True # Sync the return data to the filter. """
    keepItemSelectionOnPageChange: Optional[bool] = None
    """ True """

    """ Keep item selection. By default, after paging and searching, user-selected items will be cleared. Turning on this option will keep user selection, allowing cross-page batch operations. """
    labelTpl: Optional[str] = None
    """ Single description template, keepItemSelectionOnPageChange """

    """ When set to true, all selected items will be listed, this option can be used to customize the item display text. """
    headerToolbar: Optional[List] = None
    """ ['bulkActions','pagination'] # top toolbar configuration """
    footerToolbar: Optional[List] = None
    """ ['statistics','pagination'] # Bottom toolbar configuration """
    alwaysShowPagination: Optional[bool] = None
    """ whether to always show pagination """
    affixHeader: Optional[bool] = None
    """ True # Whether to fix the table header (under table) """
    autoGenerateFilter: Optional[bool] = None
    """ Whether to enable the query area, which will automatically generate a query form based on the value of the searchable property of the column element """
    itemAction: Optional[Action] = None
    """ Implement a custom action when a row is clicked, supports all configurations in action, such as pop-up boxes, refreshing other components, etc. """


class TableColumn(MSAUINode):
    """columnConfiguration"""

    type: Optional[str] = None
    """ Literal['text','audio','image','link','tpl','mapping','carousel','date', 'progress','status','switch','list','json','operation'] """
    label: Optional[MSAUITemplate] = None
    """ the text content of the table header """
    name: Optional[str] = None
    """ Data associated by name """
    tpl: Optional[MSAUITemplate] = None
    """ Template """
    fixed: Optional[str] = None
    """ Whether to fix the front row left|right|none """
    popOver: Optional[Union[bool, dict]] = None
    """ popup box """
    quickEdit: Optional[Union[bool, dict]] = None
    """ QuickEdit """
    copyable: Optional[Union[bool, dict]] = None
    """ whether copyable boolean or {icon: string, content:string} """
    sortable: Optional[bool] = None
    """ False # Whether to sort """
    searchable: Optional[Union[bool, MSAUISchemaNode]] = None
    """ False # Whether to search quickly boolean|Schema """
    width: Optional[Union[str, int]] = None
    """ Column width """
    remark: Optional[Remark] = None
    """ Prompt message"""
    breakpoint: Optional[str] = None
    """ *,ls"""


class ColumnOperation(TableColumn):
    """operationColumn"""

    type: str = "operation"
    label: Optional[MSAUITemplate] = None
    """ "operation" """
    toggled: Optional[bool] = None
    """ True"""
    buttons: Optional[List[Union[Action, MSAUINode]]] = None


class ColumnImage(Image, TableColumn):
    """Image Column"""


class ColumnImages(Images, TableColumn):
    """Image collection Column"""


class Table(MSAUINode):
    """table"""

    type: str = "table"
    """ Specify as table renderer"""
    title: Optional[str] = None
    """ title"""
    source: Optional[str] = None
    """ "${items}" # data source, bound to the current environment variable"""
    affixHeader: Optional[bool] = None
    """ True # Whether to fix the table header"""
    columnsTogglable: Optional[Union[str, bool]] = None
    """ "auto" # Show column display switch, auto i.e.: automatically on when the number of columns is greater than or equal to 5"""
    placeholder: Optional[str] = None
    """ "No data yet" # Text alert when there is no data"""
    className: Optional[str] = None
    """ "panel-default" # Outer CSS class name"""
    tableClassName: Optional[str] = None
    """ "table-sqlite_db table-striped" # Table CSS class name"""
    headerClassName: Optional[str] = None
    """ "Action.md-table-header" # top outer CSS class name"""
    footerClassName: Optional[str] = None
    """ "Action.md-table-footer" # bottom outer CSS class name"""
    toolbarClassName: Optional[str] = None
    """ "Action.md-table-toolbar" # Toolbar CSS class name"""
    columns: Optional[List[Union[TableColumn, MSAUISchemaNode]]] = None
    """ Used to set column information"""
    combineNum: Optional[int] = None
    """ Automatically merge cells"""
    itemActions: Optional[List[Action]] = None
    """ Hover row action button group"""
    itemCheckableOn: Optional[MSAUIExpression] = None
    """ condition to configure whether the current row is checkable, use expression"""
    itemDraggableOn: Optional[MSAUIExpression] = None
    """ condition to configure whether the current row is draggable or not, use the expression"""
    checkOnItemClick: Optional[bool] = None
    """ False # Whether the current row can be checked by clicking on the data row"""
    rowClassName: Optional[str] = None
    """ Add a CSS class name to the row"""
    rowClassNameExpr: Optional[MSAUITemplate] = None
    """ Add a CSS class name to the row via a template"""
    prefixRow: Optional[List] = None
    """ Top summary row"""
    affixRow: Optional[List] = None
    """ Bottom summary row"""
    itemBadge: Optional["Badge"] = None
    """ Row corner configuration"""
    autoFillHeight: Optional[bool] = None
    """ Content area adaptive height"""
    footable: Optional[Union[bool, dict]] = None
    """ When there are too many columns, there is no way to display all the content, so you can let some of the information displayed at the bottom, which allows users to expand to see the details.
    The configuration is very simple, just turn on the footable property and add a breakpoint property to * for the columns you want to display at the bottom."""


class Chart(MSAUINode):
    """chart: https://echarts.apache.org/zh/option.html#title"""

    type: str = "chart"
    """ Specify as chart renderer"""
    className: Optional[str] = None
    """ class name of the outer Dom"""
    body: Optional[MSAUISchemaNode] = None
    """ Content container"""
    api: Optional[MSA_UI_API] = None
    """ Configuration item interface address"""
    source: Optional[Dict] = None
    """ Get the value of a variable in the data chain as a configuration via data mapping"""
    initFetch: Optional[bool] = None
    """ Whether to request the interface when the component is initialized"""
    interval: Optional[int] = None
    """ Refresh time (min 1000)"""
    config: Optional[Union[dict, str]] = None
    """ Set the configuration of eschars, when it is string, you can set function and other configuration items"""
    style: Optional[Dict] = None
    """ Set the style of the root element"""
    width: Optional[str] = None
    """ Set the width of the root element"""
    height: Optional[str] = None
    """ Set the height of the root element"""
    replaceChartOption: Optional[bool] = None
    """ False # Does each update completely override the configuration item or append it?"""
    trackExpression: Optional[str] = None
    """ Update the chart when the value of this expression has changed"""


class Code(MSAUINode):
    """Code highlighting"""

    type: str = "code"
    className: Optional[str] = None
    """ Outer CSS class name """
    value: Optional[str] = None
    """ The value of the displayed color"""
    name: Optional[str] = None
    """ Used as a variable mapping when in other components"""
    language: Optional[str] = None
    """ The highlighting language used, default is plaintext"""
    tabSize: Optional[int] = None
    """ 4 # Default tab size"""
    editorTheme: Optional[str] = None
    """ "'vs'" # theme, and 'vs-dark'"""
    wordWrap: Optional[str] = None
    """ "True" # whether to wrap the line"""


class Json(MSAUINode):
    """JSON display component"""

    type: str = "json"
    """ "json" if in Table, Card and List; "static-json" if used as a static display in Form"""
    className: Optional[str] = None
    """ Outer CSS class name"""
    value: Optional[Union[dict, str]] = None
    """ json value, parse automatically if it is a string"""
    source: Optional[str] = None
    """ Get the value in the data chain by data mapping"""
    placeholder: Optional[str] = None
    """ Placeholder text"""
    levelExpand: Optional[int] = None
    """ 1 # Default level of expansion"""
    jsonTheme: Optional[str] = None
    """ "twilight" # theme, optional twilight and eighties"""
    mutable: Optional[bool] = None
    """ False # whether to modify"""
    displayDataTypes: Optional[bool] = None
    """ False # Whether to display data types"""


class Link(MSAUINode):
    """link"""

    type: str = "link"
    """ "link" if in Table, Card and List; "static-link" if used as a static display in Form"""
    body: Optional[str] = None
    """ text inside the tag"""
    href: Optional[str] = None
    """ Link address"""
    blank: Optional[bool] = None
    """ whether to open in a new tab"""
    htmlTarget: Optional[str] = None
    """ target of a tag, takes precedence over the blank attribute"""
    title: Optional[str] = None
    """ the title of a tag"""
    disabled: Optional[bool] = None
    """ Disable hyperlinks"""
    icon: Optional[str] = None
    """ hyperlink icon to enhance display"""
    rightIcon: Optional[str] = None
    """ right icon"""


class Log(MSAUINode):
    """LiveLog"""

    type: str = "log"
    source: Optional[MSA_UI_API] = None
    """ support variable, can be initially set to null, so that it will not be loaded initially, but will be loaded when the variable has a value"""
    height: Optional[int] = None
    """ 500 # height of display area"""
    className: Optional[str] = None
    """ Outer CSS class name"""
    autoScroll: Optional[bool] = None
    """ True # whether to auto-scroll"""
    placeholder: Optional[str] = None
    """ Text in load"""
    encoding: Optional[str] = None
    """ "utf-8" # Returns the character encoding of the content"""


class Mapping(MSAUINode):
    """mapping"""

    type: str = "mapping"
    """ "mapping" if in Table, Card and List; "static-mapping" if used as a static display in Form"""
    className: Optional[str] = None
    """ Outer CSS class name"""
    placeholder: Optional[str] = None
    """ Placeholder text"""
    map: Optional[Dict] = None
    """ Mapping configuration"""
    source: Optional[MSA_UI_API] = None
    """ MSA_UI_API or data mapping"""


class Property(MSAUINode):
    """Property table"""

    class Item(MSAUINode):
        label: Optional[MSAUITemplate] = None
        """ property name"""
        content: Optional[MSAUITemplate] = None
        """ attribute value"""
        span: Optional[int] = None
        """ attribute value across several columns"""
        visibleOn: Optional[MSAUIExpression] = None
        """ Show expressions"""
        hiddenOn: Optional[MSAUIExpression] = None
        """ Hide the expression"""

    type: str = "property"
    className: Optional[str] = None
    """ the class name of the outer dom"""
    style: Optional[Dict] = None
    """ The style of the outer dom"""
    labelStyle: Optional[Dict] = None
    """ Style of the property name"""
    contentStyle: Optional[Dict] = None
    """ The style of the property value"""
    column: Optional[int] = None
    """ 3 # how many columns per row"""
    mode: Optional[str] = None
    """ 'table' # display mode, currently only 'table' and 'simple'"""
    separator: Optional[str] = None
    """ ',' # separator between attribute name and value in 'simple' mode"""
    source: Optional[MSAUITemplate] = None
    """ Data source"""
    title: Optional[str] = None
    """ title"""
    items: Optional[List[Item]] = None
    """ data items"""


class QRCode(MSAUINode):
    """QR Code"""

    type: str = "qr-code"
    """ Specified as a QRCode renderer"""
    value: MSAUITemplate
    """ The text to be displayed after scanning the QR code, to display a page enter the full url ("http://..." or "https://..." ), supports the use of templates"""
    className: Optional[str] = None
    """ Class name of the outer Dom"""
    qrcodeClassName: Optional[str] = None
    """ class name of the QR code SVG"""
    codeSize: Optional[int] = None
    """ 128 # The width and height of the QR code"""
    backgroundColor: Optional[str] = None
    """ "#fff" # QR code background color"""
    foregroundColor: Optional[str] = None
    """ "#000" # The foreground color of the QR code"""
    level: Optional[str] = None
    """ "L" # QR code complexity level, there are four ('L' 'M' 'Q' 'H')"""


class Video(MSAUINode):
    """video"""

    type: str = "video"
    """ Specify as video renderer"""
    className: Optional[str] = None
    """ class name of the outer Dom"""
    src: Optional[str] = None
    """ video address"""
    isLive: Optional[bool] = None
    """ False # whether it is live, need to add on when the video is live, supports flv and hls formats"""
    videoType: Optional[str] = None
    """ Specify the format of the live video"""
    poster: Optional[str] = None
    """ video cover address"""
    muted: Optional[bool] = None
    """ whether to mute"""
    autoPlay: Optional[bool] = None
    """ Whether to auto play"""
    rates: Optional[List[float]] = None
    """ multiplier in the format [1.0, 1.5, 2.0]"""


class Alert(MSAUINode):
    """alert"""

    type: str = "alert"
    """ Specify as alert renderer"""
    className: Optional[str] = None
    """ class name of the outer Dom"""
    level: Optional[str] = None
    """ "info" # level, can be: info, success, warning or danger"""
    body: Optional[MSAUISchemaNode] = None
    """ Display content"""
    showCloseButton: Optional[bool] = None
    """ False # whether to show the close button"""
    closeButtonClassName: Optional[str] = None
    """ CSS class name of the close button"""
    showIcon: Optional[bool] = None
    """ False # Whether to show icon"""
    icon: Optional[str] = None
    """ Custom icon"""
    iconClassName: Optional[str] = None
    """ CSS class name of the icon"""


class Dialog(MSAUINode):
    """Dialog"""

    type: str = "dialog"
    """ Specify as Dialog renderer"""
    title: Optional[MSAUISchemaNode] = None
    """ popup layer title"""
    body: Optional[MSAUISchemaNode] = None
    """ Add content to the Dialog content area"""
    size: Optional[Union[str, SizeEnum]] = None
    """ Specify dialog size, supports: xs, sm, md, lg, xl, full"""
    bodyClassName: Optional[str] = None
    """ "modal-body" # The style class name of the Dialog body area"""
    closeOnEsc: Optional[bool] = None
    """ False # Whether to close the Dialog by pressing Esc"""
    showCloseButton: Optional[bool] = None
    """ True # Whether to show the close button in the upper right corner"""
    showErrorMsg: Optional[bool] = None
    """ True # Whether to show the error message in the lower left corner of the popup box"""
    disabled: Optional[bool] = None
    """ False # If this property is set, the Dialog is read only and no action is submitted."""
    actions: Optional[List[Action]] = None
    """ If you want to not show the bottom button, you can configure: [] "[Confirm] and [Cancel]" """
    data: Optional[Dict] = None
    """ Support data mapping, if not set will default to inherit data from the context of the trigger button."""


class Drawer(MSAUINode):
    """drawer"""

    type: str = "drawer"
    """ "drawer" is specified as the Drawer renderer"""
    title: Optional[MSAUISchemaNode] = None
    """ popup layer title"""
    body: Optional[MSAUISchemaNode] = None
    """ Add content to the Drawer content area"""
    size: Optional[Union[str, SizeEnum]] = None
    """ Specify Drawer size, supports: xs, sm, md, lg"""
    position: Optional[str] = None
    """ 'left' # Position"""
    bodyClassName: Optional[str] = None
    """ "modal-body" # The style class name of the Drawer body area"""
    closeOnEsc: Optional[bool] = None
    """ False # Whether or not to support closing the Drawer by pressing Esc"""
    closeOnOutside: Optional[bool] = None
    """ False # Whether to close the Drawer by clicking outside the content area"""
    overlay: Optional[bool] = None
    """ True # Whether or not to show the mask"""
    resizable: Optional[bool] = None
    """ False # Whether the Drawer size can be changed by dragging and dropping"""
    actions: Optional[List[Action]] = None
    """ Can be set without, only two buttons by default. "[Confirm] and [Cancel]" """
    data: Optional[Dict] = None
    """ Support data mapping, if not set will default to inherit data from the context of the trigger button."""


class Iframe(MSAUINode):
    """Iframe"""

    type: str = "iframe"
    """ Specify as iFrame renderer"""
    className: Optional[str] = None
    """ The class name of the iFrame"""
    frameBorder: Optional[List] = None
    """ frameBorder"""
    style: Optional[Dict] = None
    """ Style object"""
    src: Optional[str] = None
    """ iframe address"""
    height: Optional[Union[int, str]] = None
    """ "100%" # iframe height"""
    width: Optional[Union[int, str]] = None
    """ "100%" # iframe width"""


class Spinner(MSAUINode):
    """loading"""

    type: str = "spinner"


class TableCRUD(CRUD, Table):
    """TableCRUD"""


class Avatar(MSAUINode):
    """Avatar"""

    type: str = "avatar"
    className: Optional[str] = None
    """ class name of the outer dom"""
    fit: Optional[str] = None
    """ "cover" # image scaling type"""
    src: Optional[str] = None
    """ Image address"""
    text: Optional[str] = None
    """ Text"""
    icon: Optional[str] = None
    """ Icon"""
    shape: Optional[str] = None
    """ "circle" # The shape, which can also be square"""
    size: Optional[int] = None
    """ 40 # size"""
    style: Optional[Dict] = None
    """ The style of the outer dom"""


class Audio(MSAUINode):
    """audio"""

    type: str = "audio"
    """ Specify as audio renderer"""
    className: Optional[str] = None
    """ the class name of the outer Dom"""
    inline: Optional[bool] = None
    """ True # whether inline mode is used"""
    src: Optional[str] = None
    """ Audio address"""
    loop: Optional[bool] = None
    """ False # Whether to loop"""
    autoPlay: Optional[bool] = None
    """ False # Whether to play automatically"""
    rates: Optional[List[float]] = None
    """ "[]" # Configurable audio playback multiplier e.g. [1.0, 1.5, 2.0]"""
    controls: Optional[List[str]] = None
    """ "['rates','play','time','process','volume']" # Internal module customization"""


class Status(MSAUINode):
    """status"""

    type: str = "status"
    """ Specify as Status renderer"""
    className: Optional[str] = None
    """ class name of the outer Dom"""
    placeholder: Optional[str] = None
    """ Placeholder text"""
    map: Optional[Dict] = None
    """ Mapping icon"""
    labelMap: Optional[Dict] = None
    """ Mapping text"""


class Tasks(MSAUINode):
    """A collection of task actions"""

    class Item(MSAUINode):
        label: Optional[str] = None
        """ Task name"""
        key: Optional[str] = None
        """ Task key value, please distinguish it uniquely"""
        remark: Optional[str] = None
        """ Current task status, supports html"""
        status: Optional[str] = None
        """ Task status: 0: initial, inoperable. 1: ready, operable. 2: in progress, not yet finished. 3: with errors, not retryable. 4: has ended normally. 5: with errors, and retryable."""

    type: str = "tasks"
    """ Specify as Tasks renderer"""
    className: Optional[str] = None
    """ Class name of the outer Dom"""
    tableClassName: Optional[str] = None
    """ Class name of the table Dom"""
    items: Optional[List[Item]] = None
    """ List of tasks"""
    checkApi: Optional[MSA_UI_API] = None
    """ Return a list of tasks, see items for the returned data."""
    submitApi: Optional[MSA_UI_API] = None
    """ The MSA_UI_API used to submit the task"""
    reSubmitApi: Optional[MSA_UI_API] = None
    """ This MSA_UI_API is used when submitting if the task fails and can be retried"""
    interval: Optional[int] = None
    """ 3000 # When there is a task in progress, it will be detected again at regular intervals, and the time interval is configured by this, default 3s."""
    taskNameLabel: Optional[str] = None
    """ "Task name" # Description of the task name column"""
    operationLabel: Optional[str] = None
    """ "operation" # Description of the operation column"""
    statusLabel: Optional[str] = None
    """ "Status" # Status column description"""
    remarkLabel: Optional[str] = None
    """ "Remarks" # Remarks column description"""
    btnText: Optional[str] = None
    """ "Go Live" # Action button text"""
    retryBtnText: Optional[str] = None
    """ "Retry" # Retry action button text"""
    btnClassName: Optional[str] = None
    """ "btn-sm btn-default" # Configure the container button className"""
    retryBtnClassName: Optional[str] = None
    """ "btn-sm btn-danger" # Configure the container retry button className"""
    statusLabelMap: Optional[List[str]] = None
    """ Configuration of the class name corresponding to the status display ["label-warning", "label-info", "label-success", "label-danger", "label-default", "label-danger"] """
    statusTextMap: Optional[List[str]] = None
    """ "["Not Started", "Ready", "In Progress", "Error", "Completed", "Error"]" # Status display corresponding to the text display configuration"""


class Wizard(MSAUINode):
    """Wizard"""

    class Step(MSAUINode):
        title: Optional[str] = None
        """ Step title"""
        mode: Optional[str] = None
        """ Show default, same as mode in Form, choose: normal, horizontal or inline."""
        horizontal: Optional[Horizontal] = None
        """ When in horizontal mode, used to control the left/right aspect ratio"""
        api: Optional[MSA_UI_API] = None
        """ The current step saves the interface, can be unconfigured."""
        initApi: Optional[MSA_UI_API] = None
        """ The current step data initialization interface."""
        initFetch: Optional[bool] = None
        """ Whether the current step data initialization interface is initially pulling."""
        initFetchOn: Optional[MSAUIExpression] = None
        """ Whether the current step data initialization interface is pulling initially, using an expression to determine."""
        body: Optional[List[FormItem]] = None
        """ A collection of form items for the current step, see FormItem."""

    type: str = "wizard"
    """ Specify as a Wizard component"""
    mode: Optional[str] = None
    """ Display mode, choose: horizontal or vertical"""
    api: Optional[MSA_UI_API] = None
    """ The interface saved in the last step."""
    initApi: Optional[MSA_UI_API] = None
    """ Initialize the data interface"""
    initFetch: Optional[MSA_UI_API] = None
    """ Initialize whether to pull data."""
    initFetchOn: Optional[MSAUIExpression] = None
    """ Initially pull data or not, configured by expression"""
    actionPrevLabel: Optional[str] = None
    """ "Previous" # Previous button text"""
    actionNextLabel: Optional[str] = None
    """ "Next" # Next button text"""
    actionNextSaveLabel: Optional[str] = None
    """ "Save and Next" # Save and Next button text"""
    actionFinishLabel: Optional[str] = None
    """ "Finish" # Finish button text"""
    className: Optional[str] = None
    """ Outer CSS class name"""
    actionClassName: Optional[str] = None
    """ "btn-sm btn-default" # Button CSS class name"""
    reload: Optional[str] = None
    """ Refresh the target object after the operation. Please fill in the name value set by the target component, if it is window then the whole current page will be refreshed."""
    redirect: Optional[MSAUITemplate] = None
    """ "3000" # Jump after the operation."""
    target: Optional[str] = None
    """ "False" # You can submit the data to another component instead of saving it yourself. Please fill in the name value set by the target component.
    If you fill in window, the data will be synced to the address bar, and the component that depends on the data will be refreshed automatically."""
    steps: List[Step] = None
    """ Array to configure step information"""
    startStep: Optional[int] = None
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
