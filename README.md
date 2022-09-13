![Logo](./docs/images/msa_logo_big.png)

------
<p align="center">
    <em>MSA SDK - FastAPI based Microservice Architecture Development Kit</em>
</p>
<p align="center">
    To build PoC's, MVP's, API's with CRUD and Dashboards fast and consistent.
</p>
<p align="center">
    Build on top of FastAPI, SQLModel, SQLAlchemy, Amis and many other bullet proofed libraries.
</p>

------

**Documentation**: <a href="http://msa.u2d.ai/" target="_blank">http://msa.u2d.ai/</a>

## Features
- **Build connected distributed applications faster**: Ready for [Dapr](https://dapr.io/)..
- **Consistency**: With sometimes 10s or 100s of Micro Services, the SDK helps to easy version control and provides a stable Dapr Basis.
- **High performance**: Based on [FastAPI](https://fastapi.tiangolo.com/zh/). Enjoy all the benefits.
- **High efficiency**: Perfect code type hints. Higher code reusability.
- **Support asynchronous and synchronous hybrid writing**: `ORM`  is based on`SQLModel` & `Sqlalchemy`. Freely customize
  database type. Asynchronous mode. Strong scalability.
- **Front-end separation**: The front-end is rendered by `Amis`, the back-end interface is automatically generated
  by `MSA SDK - Admin`. The interface is reusable.
- **Strong scalability**: The background page supports `Amis` pages and ordinary `html` pages. Easily customize the
  interface freely.
- **Automatic api documentation**: Automatically generate Interface documentation by `FastAPI`. Easily debug and share
  interfaces.

## Dependencies

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
  combined with  [SQLAlchemy](https://www.sqlalchemy.org/) and [Pydantic](https://pydantic-docs.helpmanual.io/), with all
  their features .
- [Amis](https://baidu.gitee.io/amis): Vue Frontend

### Usage example is in the app module \_\_init\_\_.py

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
  app.logger.info("MSA SDK Test Timer Async Every Minute")


# example sync/blocking function to be executed by a timer
def test_timer_five_sec():
  app.logger.info("MSA SDK Test Timer Sync 5 Second")


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
settings.title = "SPK.ai - MSA/SDK MVP"
settings.version = "SPK.0.0.1"
settings.debug = True

# Create some timers with a MSATimer instance, define the interval and set the handler
my_timers: MSATimers = MSATimers()
my_timers.create_timer(MSATimerEnum.every_minute, test_timer_min)
my_timers.create_timer(MSATimerEnum.on_the_5_second, test_timer_five_sec)

# Create the main app instance, like the FastAPI but provide a Setting Definition Instance
# Optional the Classes of your SQLModels
# Define if the optional Admin Site gets mounted automatically, if False you need to Mount in your own Startup MSAUIEvent Handler
# Optional the MSATimers instance
app = MSAApp(settings=settings, timers=my_timers, auto_mount_site=True,
             sql_models=[TestArticle, TestCategory],
             contact={"name": "MSA SDK", "url": "http://u2d.ai", "email": "stefan@u2d.ai"},
             license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT", })

# use the internal logger of app
app.logger.info("Initialized " + settings.title + " " + settings.version)


# Optional use startup event
# Mount the Admin Site here if enabled and the auto mount option was False
@app.on_event("startup")
async def startup():
  app.logger.info("MSA SDK Own Startup MSAUIEvent")
  # app.mount_site()


# Optional use shutdown event
@app.on_event("shutdown")
async def shutdown():
  app.logger.info("MSA SDK Own Shutdown MSAUIEvent")
```

# Typical Run Log
![Typical Log Run](./docs/images/msa_sdk_run.png)

## Interface Preview


#### Home Screen with System Info
- Open `http://127.0.0.1:8090/admin/` in your browser:
![Home](./docs/images/msa_admin_home.png)

#### CRUD of SQLModels Screen
![CRUD](./docs/images/msa_admin_crud.png)

#### Login Screen
- Open `http://127.0.0.1:8090/admin/auth/form/login` in your browser:
![Login](./docs/images/msa_auth_login.png)
- 
#### OpenAPI Interactive Documentation (Swagger) Screen
- Open `http://127.0.0.1:8090/#/admin/docs` in your browser:
![OpenAPI](./docs/images/msa_admin_openapi.png)

#### Profiler Screen
- Open `http://127.0.0.1:8090/#/admin/profiler` in your browser:
![OpenAPI](./docs/images/msa_admin_profiler.png)

## License Agreement

- `MSA SDK`Based on `MIT` open source and free to use, it is free for commercial use, but please clearly show the copyright information about MSA SDK - Auth Admin in the display interface.


## How to create the documentation

We use mkdocs and mkdocsstring. The code reference and nav entry get's created virtually by the triggered python script /docs/gen_ref_pages.py while ``mkdocs`` ``serve`` or ``build`` is executed.

### Requirements Install for the PDF creation option:
PDF Export is using mainly weasyprint, if you get some errors here pls. check there documentation. Installation is part of the MSA SDK, so this should be fine.

We can now test and view our documentation using:

    mkdocs serve

Build static Site:

    mkdocs build