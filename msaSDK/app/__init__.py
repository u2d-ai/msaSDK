# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - U2D.ai / S.Welcker
"""

from typing import Optional, List

from sqlmodel import SQLModel

from msaSDK.admin.utils.fields import Field
from msaSDK.models.service import get_msa_app_settings
from msaSDK.service import MSAApp


async def test_timer_min():
    app.logger.info("msaSDK Test Timer Async Every Minute")


def test_timer_five_sec():
    app.logger.info("msaSDK Test Timer Sync 5 Second")


class TestArticle(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


class TestCategory(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


get_msa_app_settings.cache_clear()
settings = get_msa_app_settings()
settings.title = "u2d.ai - MSA/SDK MVP"
settings.version = "0.0.1"
settings.debug = True

app = MSAApp(settings=settings, auto_mount_site=True,
             sql_models=[TestArticle, TestCategory],
             contact={"name": "msaSDK", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })

app.scheduler.task("every 1 min", func=test_timer_min )
app.scheduler.task("every 5 sec", func=test_timer_five_sec )

app.logger.info("Initialized " + settings.title + " " + settings.version)


@app.on_event("startup")
async def startup():
    app.logger.info("msaSDK Own Startup MSAUIEvent")
    #app.mount_site()


@app.on_event("shutdown")
async def shutdown():
    app.logger.info("msaSDK Own Shutdown MSAUIEvent")


if __name__ == '__main__':
    pass
