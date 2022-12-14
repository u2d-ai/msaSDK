# Admin Site

<h2 align="center">
  msaSDK - Admin Site
</h2>
<p align="center">
    <em>Admin Site is an efficient and easily extensible MSAApp (FastAPI) admin framework.</em><br/>
    <em>Inspired by Django-admin, and for a fast track through PoC's, MVP's to Production.</em>
</p>

---

`msaSDK - Admin Site` is an efficient `Python 3.7+` based framework on top of `msaSDK` & `fastapi` & `amis` , and
build with standard Python type hints. The original intention of the development is to improve the application ecology and
to quickly generate a visual dashboard for API's and web application. It was build to support very quick PoC's, MVP's 
in AI Applications. It can be extended with Auth and Login for an MVP Phase with the Auth Module by just define a setting to True. 

---

## Features
- **Front-end separation**: The front-end is rendered by `Amis`, the back-end interface is automatically generated
  by `msaSDK.db.crud`. The interface is reusable.
- **Strong scalability**: The page creation supports `Amis` pages and ordinary `html` pages. 


## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
  combined with  [SQLAlchemy](https://www.sqlalchemy.org/) and [Pydantic](https://pydantic-docs.helpmanual.io/), with all
  their features .
- [Amis](https://baidu.gitee.io/amis): Vue.js / React - JSON based Frontend

## Composition

`msaSDK - Admin` consists of three core modules, of which, `amis`, `crud`, which can be used as separate
modules, and `MSAApp` as the core SDK part.

- `amis`: Based on the `pydantic` data model building library of `baidu amis`. To generate/parse data rapidly.
- `crud`: Based on `FastAPI` & `SQLModel`. To quickly build Create, Read, Update, Delete common API interfaces.
- `admin`: Inspired by `Django-Admin`. Combine `amis` with `crud`. To quickly build Web Admin dashboard .

## Simple Example

```python
# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - U2D.ai / S.Welcker
"""
__version__ = "0.0.1"

from typing import Optional
from sqlmodel import SQLModel
from msaSDK.admin.utils.fields import Field
from msaSDK.models.service import get_msa_app_settings
from msaSDK.service import MSAApp
from msaSDK.utils.scheduler import MSATimers, MSATimerEnum


# example async function to be executed by a timer
async def test_timer_min():
  app.logger.info("msaSDK Test Timer Async Every Minute")


# example sync/blocking function to be executed by a timer
def test_timer_five_sec():
  app.logger.info("msaSDK Test Timer Sync 5 Second")


# SQLModel class to be used for auto API CRUD and/or Admin Site Web UI
class TestArticle(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
  title: str = Field(title='ArticleTitle', max_length=200)
  description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
  status: bool = Field(None, title='status')
  content: str = Field(title='ArticleContent')


# SQLModel class to be used for auto API CRUD and/or Admin Site Web UI
class TestCategory(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
  title: str = Field(title='ArticleTitle', max_length=200)
  description: Optional[str] = Field(default='', title='ArticleDescription', max_length=400)
  status: bool = Field(None, title='status')
  content: str = Field(title='ArticleContent')


# get the MSA app setting, clear the cache, set some settings
get_msa_app_settings.cache_clear()
settings = get_msa_app_settings()
settings.title = "u2d.ai - MSA/SDK MVP"
settings.version = "MSA.0.0.1"
settings.debug = True

# Create some timers with a MSATimer instance, define the interval and set the handler
my_timers: MSATimers = MSATimers()
my_timers.create_timer(MSATimerEnum.every_minute, test_timer_min)
my_timers.create_timer(MSATimerEnum.on_the_5_second, test_timer_five_sec)

# Create the main app instance, like FastAPI but provide a Setting Definition Instance
# Optional the Classes of your SQLModels
# Define if the optional Admin Site gets mounted automatically, if False you need to Mount in your own Startup MSAUIEvent Handler
# Optional the MSATimers instance
app = MSAApp(settings=settings, timers=my_timers, auto_mount_site=True,
             sql_models=[TestArticle, TestCategory],
             contact={"name": "msaSDK", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })

# use the internal logger of app
app.logger.info("Initialized " + settings.title + " " + settings.version)


# Optional use startup event
@app.on_event("startup")
async def startup():
  app.logger.info("msaSDK Own Startup MSAUIEvent")


# Optional use shutdown event
@app.on_event("shutdown")
async def shutdown():
  app.logger.info("msaSDK Own Shutdown MSAUIEvent")
```


## Interface Preview


#### Home Screen with System Info
- Open `http://127.0.0.1:8090/admin/` in your browser:
![Home](../images/msa_admin_home.png)

#### CRUD of SQLModels Screen
![CRUD](../images/msa_admin_crud.png)

#### OpenAPI Interactive Documentation (Swagger) Screen
- Open `http://127.0.0.1:8090/#/admin/docs` in your browser:
![OpenAPI](../images/msa_admin_openapi.png)

#### Profiler Screen
- Open `http://127.0.0.1:8090/#/admin/profiler` in your browser:
![Profiler](../images/msa_admin_profiler.png)

## License Agreement

- `msaSDK`Based on `MIT` open source and free to use, it is free for commercial use, but please clearly show the copyright information about msaSDK - Auth Admin in the display interface.


