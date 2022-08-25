# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - U2D.ai / S.Welcker
"""
__version__ = "0.0.1"
import os

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from u2d_msa_sdk.service import MSAApp
from fastapi_utils.api_settings import get_api_settings
from fastapi_utils.tasks import repeat_every


get_api_settings.cache_clear()
settings = get_api_settings()
settings.title = "MSA SDK PROJECT_NAME"
settings.version = "MSA SDK VERSION"
settings.debug = True

app = MSAApp(**settings.fastapi_kwargs, is_master=True,
             contact={"name": "MSA SDK Prototype", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })

app.mount("/msastatic", StaticFiles(directory="msastatic"), name="msastatic")
templates = Jinja2Templates(directory="templates")


ROOTPATH = os.path.join(os.path.dirname(__file__))


@app.get("/", tags=["default"], response_class=HTMLResponse)
async def index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "settings": settings.json()})


@app.get("/testpage", tags=["test"], response_class=HTMLResponse)
async def testpage(request: Request):
    return templates.TemplateResponse("test.html", {"request": request, "settings": settings.json()})


@app.on_event("startup")
async def startup():
    print("MSA SDK Startup Event")


@app.on_event("shutdown")
async def shutdown():
    print("MSA SDK Shutdown Event")


@app.on_event("startup")
@repeat_every(seconds=60)
async def repeat_expired_sec() -> None:
    print("MSA SDK Repeat Event 60 sec")

