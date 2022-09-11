Example Usage of MSAApp
Copyright (c) 2022 - U2D.ai / S.Welcker

```python
Example Usage of MSAApp
Copyright (c) 2022 - U2D.ai / S.Welcker
__version__ = "0.0.1"

from typing import Optional

from sqlmodel import SQLModel

from u2d_msa_sdk.admin.utils.fields import Field
from u2d_msa_sdk.models.service import get_msa_app_settings
from u2d_msa_sdk.service import MSAApp
from u2d_msa_sdk.utils.scheduler import MSATimers, MSATimerEnum


async def test_timer_min():
    app.logger.info("MSA SDK Test Timer Async Every Minute")


def test_timer_five_sec():
    app.logger.info("MSA SDK Test Timer Sync 5 Second")


class TestArticle(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


class TestCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    title: str = Field(title='ArticleTitle', max_length=200)
    description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
    status: bool = Field(None, title='status')
    content: str = Field(title='ArticleContent')


get_msa_app_settings.cache_clear()
settings = get_msa_app_settings()
settings.title = "SPK.ai - MSA/SDK MVP"
settings.version = "SPK.0.0.1"
settings.debug = True

my_timers: MSATimers = MSATimers()
my_timers.create_timer(MSATimerEnum.every_minute, test_timer_min)
my_timers.create_timer(MSATimerEnum.on_the_5_second, test_timer_five_sec)

app = MSAApp(settings=settings, timers=my_timers, auto_mount_site=True,
             sql_models=[TestArticle, TestCategory],
             contact={"name": "MSA SDK", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })


app.logger.info("Initialized " + settings.title + " " + settings.version)


@app.on_event("startup")
async def startup():
    app.logger.info("MSA SDK Own Startup Event")
    #app.mount_site()


@app.on_event("shutdown")
async def shutdown():
    app.logger.info("MSA SDK Own Shutdown Event")


if __name__ == '__main__':
    pass
```