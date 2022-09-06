# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - U2D.ai / S.Welcker
"""
__version__ = "0.0.1"

from fastapi_utils.api_settings import get_api_settings
from fastapi_utils.tasks import repeat_every
from u2d_msa_sdk.service import MSAApp

get_api_settings.cache_clear()
settings = get_api_settings()
settings.title = "SPK.ai - MSA/SDK MVP"
settings.version = "SPK.0.0.1"
settings.debug = True

app = MSAApp(settings,
             contact={"name": "MSA SDK", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })
app.logger.info("Initialized " + settings.title + " " + settings.version)


@app.on_event("startup")
async def startup():
    app.logger.info("MSA SDK Startup Event")


@app.on_event("shutdown")
async def shutdown():
    app.logger.info("MSA SDK Shutdown Event")


@app.on_event("startup")
@repeat_every(seconds=60)
async def repeat_expired_sec() -> None:
    app.logger.info("MSA SDK Repeat Event 60 sec")

