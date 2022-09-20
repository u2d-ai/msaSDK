import os

from starlette.endpoints import WebSocketEndpoint

from .htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
from .quasarcomponents import *
from ..jpcore.justpy_app import JustpyAjaxEndpoint, handle_event, cookie_signer

from ..jpcore.justpy_config import config, AGGRID, AGGRID_ENTERPRISE, BOKEH, COOKIE_MAX_AGE, CRASH
from ..jpcore.justpy_config import DEBUG, DECKGL, FAVICON, HIGHCHARTS, HOST, KATEX, LATENCY
from ..jpcore.justpy_config import MEMORY_DEBUG, NO_INTERNET, PLOTLY, PORT, SECRET_KEY, SESSION_COOKIE_NAME, SESSIONS
from ..jpcore.justpy_config import SSL_CERTFILE, SSL_KEYFILE, SSL_VERSION, STATIC_DIRECTORY, STATIC_NAME, STATIC_ROUTE
from ..jpcore.justpy_config import QUASAR, QUASAR_VERSION, TAILWIND, VEGA

from .pandas import *

import os


class AjaxEndpoint(JustpyAjaxEndpoint):
    """
    Justpy ajax handler
    """


class JustpyEvents(WebSocketEndpoint):
    socket_id = 0

    async def on_connect(self, websocket):
        await websocket.accept()
        websocket.id = JustpyEvents.socket_id
        websocket.open = True

        JustpyEvents.socket_id += 1
        # Send back socket_id to page
        # await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})
        WebPage.loop.create_task(
            websocket.send_json({"type": "websocket_update", "data": websocket.id})
        )

    async def on_receive(self, websocket, data):
        """
        Method to accept and act on data received from websocket
        """

        data_dict = hjson.loads(data)
        msg_type = data_dict["type"]
        # data_dict['event_data']['type'] = msg_type
        if msg_type == "connect":
            # Initial message sent from browser after connection is established
            # WebPage.sockets is a dictionary of dictionaries
            # First dictionary key is page id
            # Second dictionary key is socket id
            page_key = data_dict["page_id"]
            websocket.page_id = page_key
            if page_key in WebPage.sockets:
                WebPage.sockets[page_key][websocket.id] = websocket
            else:
                WebPage.sockets[page_key] = {websocket.id: websocket}
            return
        if msg_type == "event" or msg_type == "page_event":
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict["event_data"]["session_id"] = session_id
            # await self._event(data_dict)
            data_dict["event_data"]["msg_type"] = msg_type
            page_event = True if msg_type == "page_event" else False
            WebPage.loop.create_task(
                handle_event(data_dict, com_type=0, page_event=page_event)
            )
            return
        if msg_type == "zzz_page_event":
            # Message sent when an event occurs in the browser
            session_cookie = websocket.cookies.get(SESSION_COOKIE_NAME)
            if SESSIONS and session_cookie:
                session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                data_dict["event_data"]["session_id"] = session_id
            data_dict["event_data"]["msg_type"] = msg_type
            WebPage.loop.create_task(
                handle_event(data_dict, com_type=0, page_event=True)
            )
            return

    async def on_disconnect(self, websocket, close_code):
        try:
            pid = websocket.page_id
        except:
            return
        websocket.open = False
        WebPage.sockets[pid].pop(websocket.id)
        if not WebPage.sockets[pid]:
            WebPage.sockets.pop(pid)
        await WebPage.instances[pid].on_disconnect(
            websocket
        )  # Run the specific page disconnect function
        if MEMORY_DEBUG:
            print("************************")
            print(
                "Elements: ",
                len(JustpyBaseComponent.instances),
                JustpyBaseComponent.instances,
            )
            print("WebPages: ", len(WebPage.instances), WebPage.instances)
            print("Sockets: ", len(WebPage.sockets), WebPage.sockets)
            import psutil
            process = psutil.Process(os.getpid())
            print(f"Memory used: {process.memory_info().rss:,}")
            print("************************")


def convert_dict_to_object(d):
    """
    convert the given dict to an object
    """
    obj = globals()[d["class_name"]]()
    for obj_prop in d["object_props"]:
        obj.add(convert_dict_to_object(obj_prop))
    # combine the dictionaries
    for k, v in {**d, **d["attrs"]}.items():
        if k != "id":
            obj.__dict__[k] = v
    return obj


def redirect(url: str) -> WebPage:
    """
    redirect to the given url
    
    Args:
        url(str): the url to redirect to
        
    Returns:
        a WebPage with a single Div that hat the redirect
    """
    wp = WebPage()
    wp.add(Div())
    wp.redirect = url
    return wp
