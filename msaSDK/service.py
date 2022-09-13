# -*- coding: utf-8 -*-
"""Main Service Module for MSAApp.

Initialize with a MSAServiceDefintion Instance to control the features and functions of the MSAApp.

"""


import asyncio
import os
import time
from asyncio import Task
from typing import List, Optional

import uvloop
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from fastapi_users.password import PasswordHelper
from fastapi_utils.timing import add_timing_middleware
from loguru import logger
from msgpack_asgi import MessagePackMiddleware
from passlib.context import CryptContext
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeMeta
from sqlmodel import SQLModel
from starception import StarceptionMiddleware
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from starlette_wtf import CSRFProtectMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from strawberry import schema

from msaSDK.db.crud import MSASQLModelCrud
from msaSDK.models.health import MSAHealthMessage
from msaSDK.models.service import MSAServiceDefinition, MSAHealthDefinition
from msaSDK.msaapi import MSAFastAPI
from msaSDK.router.system import sys_router
from msaSDK.security import getMSASecurity
from msaSDK.utils import healthcheck as health
from msaSDK.utils.logger import init_logging
from msaSDK.utils.profiler import MSAProfilerMiddleware
from msaSDK.utils.scheduler import MSATimers, MSAScheduler
from msaSDK.utils.sysinfo import get_sysinfo, MSASystemInfo


security_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
"""Security Context for Password Helper"""
password_helper = PasswordHelper(security_context)
"""Password Helper Instance"""
security = getMSASecurity()
"""MSASecurity instance"""


class MSATimerStatus(SQLModel):
    """**MSATimerStatus** Pydantic Response Class
    """
    mode: Optional[str] = None
    """Timer Mode."""
    func: Optional[str] = None
    """Timer Handler Function."""
    mark_HH_MM: Optional[str] = None
    """ Mark for Schedule"""


class MSASchedulerStatus(SQLModel):
    """
    **MSASchedulerStatus** Pydantic Response Class
    """
    name: Optional[str] = "msaSDK Service"
    """Service Name."""
    timers: Optional[List[MSATimerStatus]] = []
    """Optional MSATimerStatus List"""
    message: Optional[str] = "None"
    """Optional Message Text"""


class MSAServiceStatus(SQLModel):
    """
    **MSAServiceStatus** Pydantic Response Class
    """
    name: Optional[str] = "msaSDK Service"
    """Service Name."""
    healthy: Optional[str] = "None"
    """Health status"""
    message: Optional[str] = "None"
    """Optional Message Text"""


class MSAOpenAPIInfo(SQLModel):
    """
    **MSAOpenAPIInfo** Pydantic Response Class
    """
    name: str = "msaSDK Service"
    """Service Name."""
    version: str = "0.0.0"
    """API Version."""
    url: str = "/openapi.json"
    """OpenAPI URL."""
    tags: Optional[List[str]] = None
    """OpenAPI Tags."""


def getSecretKey():
    """
    Get Secret Key for Token creation from OS Environment Variable **SECRET_KEY_TOKEN**

    Returns:
        key: The SECRET_KEY_TOKEN.

    """
    key: str = os.getenv("SECRET_KEY_TOKEN",
                             "u2dmsaservicex_#M8A{1o3Bd?<ipwt^K},Z)OE<Fkj-X9IILWq|Cf`Y:HFI~&2L%Ion3}+p{T%")
    return key


def getSecretKeySessions():
    """
    Get Secret Key for Session Middleware from OS Environment Variable **SECRET_KEY_SESSIONS**

    Returns:
        key: The SECRET_KEY_SESSIONS.

    """
    key: str = os.getenv("SECRET_KEY_SESSIONS",
                             "u2dmsaserviceeP)zg5<g@4WJ0W8'?ad!T9UBvW1z2k|y~|Pgtewv=H?GY_Q]t~-~UUe'pJ0V[>!<)")
    return key


def getSecretKeyCSRF() -> str:
    """
    Get Secret Key for CSRF Middleware from OS Environment Variable **SECRET_KEY_CSRF**

    Returns:
        key: The SECRET_KEY_CSRF.

    """
    key: str = os.getenv("SECRET_KEY_CSRF",
                             "u2dmsaservicee_rJM'onkEV1trD=I7dci$flB)aSNW+raL4j]Ww=n~_BRg35*3~(E.>rx`1aTw:s")
    return key


class MSAApp(MSAFastAPI):
    """Creates an application msaSDK instance.

    Note:
        As with FastApi the MSAApp provides two events:
        ``startup``: A list of callables to run on application startup. Startup handler callables do not take any arguments, and may be be either standard functions, or async functions.
        ``shutdown``: A list of callables to run on application shutdown. Shutdown handler callables do not take any arguments, and may be be either standard functions, or async functions.
        Those are also used internally, which are triggered before the external events.

        Do not include the `self` parameter in the ``Args`` section.

    Args:
        settings: MSAServiceDefinition (Must be provided), instance of a service definition with all settings
        timers: MSATimers instance Default None, provide a MSATimers instance and it will start the scheduler internaly
        sql_models: List of SQLModel Default None, provide list of your SQLModel Classes and the instance can create CRUD API and if site is enabled also UI for CRUD
        auto_mount_site: Default True, if site is enabled in settings and this is true, mounts the site in internal startup event.

    Attributes:
        logger: loguru logger instance
        auto_mount_site: bool auto_mount_site
        settings: MSAServiceDefinition settings instance.
        timers: MSATimers = timers
        healthdefinition: MSAHealthDefinition settings.healthdefinition
        limiter: Limiter = None
        db_engine: AsyncEngine = Db Engine instance
        sql_models: List[SQLModel] = sql_models
        sql_cruds: List[MSASQLModelCrud] = []
        scheduler: MSAScheduler = None
        site: AdminSite Admin/Auth Site instance.
        scheduler_task: The Task instance that runs the Scheduler in the Background
        ROOTPATH: str os.path.join(os.path.dirname(__file__))

    """

    def __init__(
            self,
            settings: MSAServiceDefinition,
            timers: MSATimers = None,
            sql_models: List[SQLModel] = None,
            auto_mount_site: bool = True,
            *args,
            **kwargs
    ) -> None:
        # call super class __init__
        super().__init__(*args, **settings.fastapi_kwargs)
        self.logger = logger
        init_logging()
        self.auto_mount_site: bool = auto_mount_site
        self.settings = settings
        self.timers: MSATimers = timers
        self.healthdefinition: MSAHealthDefinition = self.settings.healthdefinition
        self.limiter: Limiter = None
        self.db_engine: AsyncEngine = None
        self.sql_models: List[SQLModel] = sql_models
        self.sql_cruds: List[MSASQLModelCrud] = []
        self.scheduler: MSAScheduler = None
        self.site = None
        self.scheduler_task: Task = None
        self.ROOTPATH = os.path.join(os.path.dirname(__file__))

        if self.settings.uvloop:
            self.logger.info("Enable UVLoop")
            uvloop.install()
        else:
            self.logger.info("Excluded UVLoop")

        self.healthcheck: health.MSAHealthCheck = None

        if self.settings.validationception:
            self.logger.info("Add Handler ValidationError")
            self.add_exception_handler(RequestValidationError, self.validation_exception_handler)
        else:
            self.logger.info("Excluded Handler ValidationError")

        if self.settings.httpception:
            self.logger.info("Add Handler HTTPException")
            self.add_exception_handler(StarletteHTTPException, self.msa_exception_handler)
        else:
            self.add_exception_handler(StarletteHTTPException, self.msa_exception_handler_disabled)
            self.logger.info("Excluded Handler HTTPException")

        if self.settings.starception:
            self.logger.info("Add Middleware Starception")
            self.add_middleware(StarceptionMiddleware)
        else:
            self.logger.info("Excluded Middleware Starception")

        if not self.settings.site:
            self.logger.info("Excluded Admin Site")
        if not self.settings.site_auth:
            self.logger.info("Excluded Admin Auth Site")

        if self.settings.db:
            self.logger.info("DB - Init: " + self.settings.db_url)
            self.Base: DeclarativeMeta = declarative_base()
            self.db_engine = create_async_engine(self.settings.db_url, echo=self.settings.db_debug, future=True)
            if (self.settings.db_crud or self.settings.site) and self.sql_models:
                self.logger.info("DB - Register/CRUD SQL Models: " + str(self.sql_models))
                # register all Models and the crud for them
                for model in self.sql_models:
                    new_crud: MSASQLModelCrud = MSASQLModelCrud(model=model, engine=self.db_engine).register_crud()
                    if self.settings.db_crud:
                        self.include_router(new_crud.router)
                    self.sql_cruds.append(new_crud)
        else:
            self.logger.info("Excluded DB")

        if self.settings.graphql:
            self.logger.info("Init Graphql")
            from strawberry.fastapi import GraphQLRouter
            self.graphql_app: GraphQLRouter = None
            self.graphql_schema: schema = None
        else:
            self.logger.info("Excluded Graphql")

        if self.healthdefinition.enabled:
            self.logger.info("Init Healthcheck")
            self.healthcheck = health.MSAHealthCheck(
                healthdefinition=self.healthdefinition,
                host=self.settings.host,
                port=self.settings.port
            )
            self.logger.info("Start Healthcheck Thread")
            self.healthcheck.start()
            self.add_api_route(self.healthdefinition.path, self.get_healthcheck,
                               response_model=MSAHealthMessage,
                               tags=["service"])
        else:
            self.logger.info("Excluded Healthcheck")

        if self.settings.sysrouter:
            self.logger.info("Include Sysrouter")
            self.include_router(sys_router)
        else:
            self.logger.info("Excluded Sysrouter")

        if self.settings.cors:
            self.logger.info("Add Middleware CORS")
            self.add_middleware(CORSMiddleware, allow_origins=self.settings.allow_origins,
                                allow_credentials=self.settings.allow_credentials,
                                allow_methods=self.settings.allow_methods,
                                allow_headers=self.settings.allow_headers, )
        else:
            self.logger.info("Excluded Middleware CORS")

        if self.settings.httpsredirect:
            self.logger.info("Add Middleware HTTPSRedirect")
            self.add_middleware(HTTPSRedirectMiddleware)
        else:
            self.logger.info("Excluded Middleware HTTPSRedirect")

        if self.settings.gzip:
            self.logger.info("Add Middleware GZip")
            self.add_middleware(GZipMiddleware)
        else:
            self.logger.info("Excluded Middleware GZip")

        if self.settings.session:
            self.logger.info("Add Middleware Session")
            self.add_middleware(SessionMiddleware, secret_key=getSecretKeySessions())
        else:
            self.logger.info("Excluded Middleware Session")

        if self.settings.csrf:
            self.logger.info("Add Middleware CSRF")
            self.add_middleware(CSRFProtectMiddleware, csrf_secret=getSecretKeyCSRF())
        else:
            self.logger.info("Excluded Middleware CSRF")

        if self.settings.msgpack:
            self.logger.info("Add Middleware MSGPack")
            self.add_middleware(MessagePackMiddleware)
        else:
            self.logger.info("Excluded Middleware MSGPack")

        if self.settings.context:
            self.logger.info("Add Middleware Context")
            self.add_middleware(RawContextMiddleware, plugins=(
                plugins.RequestIdPlugin(),
                plugins.CorrelationIdPlugin()
            ))
        else:
            self.logger.info("Excluded Middleware Context")

        if self.settings.profiler:
            self.logger.info("Add Middleware Profiler")
            self.add_middleware(MSAProfilerMiddleware,
                                profiler_output_type=self.settings.profiler_output_type,
                                track_each_request=self.settings.profiler_single_calls,
                                msa_app=self)
        else:
            self.logger.info("Excluded Middleware Profiler")

        if self.settings.timing:
            self.logger.info("Add Middleware Timing")
            add_timing_middleware(self, record=self.logger.info, prefix="app", exclude="untimed")
        else:
            self.logger.info("Excluded Middleware Timing")

        if self.settings.limiter:
            self.logger.info("Add Limiter Engine")
            self.limiter = Limiter(key_func=get_remote_address)
            self.state.limiter = self.limiter
            self.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        else:
            self.logger.info("Excluded Limiter Engine")

        if self.settings.servicerouter:
            self.logger.info("Include Servicerouter")
            self.add_api_route("/scheduler", self.get_scheduler_status, tags=["service"],
                               response_model=MSASchedulerStatus)
            self.add_api_route("/status", self.get_services_status, tags=["service"],
                               response_model=MSAServiceStatus)
            self.add_api_route("/definition", self.get_services_definition, tags=["service"],
                               response_model=MSAServiceDefinition)
            self.add_api_route("/settings", self.get_services_settings, tags=["service"])
            self.add_api_route("/schema", self.get_services_openapi_schema, tags=["openapi"])
            self.add_api_route("/info", self.get_services_openapi_info, tags=["openapi"],
                               response_model=MSAOpenAPIInfo)
        else:
            self.logger.info("Excluded Servicerouter")

        if self.settings.static or self.settings.pages:
            self.logger.info("Mount MSAStatic")
            self.mount("/msastatic", StaticFiles(directory="msastatic"), name="msastatic")
        else:
            self.logger.info("Excluded MSAStatic")

        if self.settings.pagination:
            self.logger.info("Add Pagination Engine")
            add_pagination(self)
        else:
            self.logger.info("Excluded Pagination Engine")

        if self.settings.templates or self.settings.pages:
            self.logger.info("Init Jinja MSAUITemplate Engine")
            self.templates = Jinja2Templates(directory=self.settings.templates_dir)
        else:
            self.logger.info("Excluded Jinja MSAUITemplate Engine")

        if self.settings.pages:
            self.logger.info("Add Pages Router")
            self.add_api_route(self.settings.profiler_url, self.profiler, tags=["pages"], response_class=HTMLResponse)
            self.add_api_route("/testpage", self.testpage, tags=["pages"], response_class=HTMLResponse)
            if not self.settings.site:
                self.add_api_route("/", self.index_page, tags=["pages"], response_class=HTMLResponse)
                self.add_api_route("/monitor", self.monitor, tags=["pages"], response_class=HTMLResponse)
                self.add_api_route("/monitor_inline", self.monitor_inline, tags=["pages"], response_class=HTMLResponse)
        else:
            self.logger.info("Excluded Pages Router")

        if self.settings.instrument:
            self.logger.info("Prometheus Instrument and Expose App")
            Instrumentator().instrument(app=self).expose(app=self, include_in_schema=True, tags=["service"],
                                                         response_class=HTMLResponse)
        else:
            self.logger.info("Excluded Prometheus Instrument and Expose")

        self.logger.info("Events - Add Internal Handlers")
        self.add_event_handler("shutdown", self.shutdown_event)
        self.add_event_handler("startup", self.startup_event)

        if self.settings.scheduler and self.timers:
            self.logger.info("Add Scheduler Timers: " + str(len(self.timers.timer_jobs)))
            if time.daylight:
                offsetHour = time.altzone / 3600
            else:
                offsetHour = time.timezone / 3600
            tz: str = 'Etc/GMT%+d' % offsetHour
            self.scheduler = MSAScheduler(jobs=self.timers.timer_jobs, local_time_zone=tz,
                                          poll_millis=self.settings.scheduler_poll_millis,
                                          parent_logger=self.logger)
        elif not self.settings.scheduler:
            self.logger.info("Excluded Scheduler, Disabled")
        else:
            self.logger.info("Excluded Scheduler, Timers is Empty")

    async def startup_event(self) -> None:
        """

        :return:
        :rtype:
        """
        self.logger.info("msaSDK Internal Startup MSAUIEvent")

        if self.settings.db:
            async with self.db_engine.begin() as conn:
                if self.settings.db_meta_drop:
                    self.logger.info("DB - Drop Meta All: " + self.settings.db_url)
                    await conn.run_sync(SQLModel.metadata.drop_all)
                if self.settings.db_meta_create:
                    self.logger.info("DB - Create Meta All: " + self.settings.db_url)
                    await conn.run_sync(SQLModel.metadata.create_all)
            await self.db_engine.dispose()

        if self.settings.site or self.settings.site_auth:

            site = None
            if self.settings.site_auth:
                self.logger.info("Add Admin Site with Auth")
                from msaSDK.auth.site import AuthAdminSite
                site = AuthAdminSite(msa_app=self)
                try:
                    await site.db.async_run_sync(SQLModel.metadata.create_all, is_session=False)
                    await site.auth.create_role_user('admin')
                except Exception as e:
                    pass
            else:
                self.logger.info("Add Admin Site without Auth")
                from msaSDK.admin import AdminSite
                site = AdminSite(msa_app=self)

            self.site = site
            if site and self.auto_mount_site:
                self.mount_site()

        if self.settings.scheduler and self.timers:
            self.logger.info("Scheduler - Start All Timers")
            self.scheduler_task = asyncio.create_task(self.scheduler.run_timers(), name="MSA_Scheduler")

    def mount_site(self) -> None:
        if self.site:
            self.logger.info("Mount Admin Site")
            self.site.mount_app(self)
        else:
            self.logger.error("Can't Mount Admin Site - Not initialized or enabled")

    async def shutdown_event(self) -> None:
        self.logger.info("msaSDK Internal Shutdown MSAUIEvent")
        if self.settings.scheduler and self.timers:
            self.logger.info("Stop Scheduler Timers: " + str(len(self.timers.timer_jobs)))
            await self.scheduler.stop_timers()
            self.logger.info("Cancel Scheduler Timers: " + str(len(self.timers.timer_jobs)))
            if not self.scheduler_task.cancelled():
                try:
                    self.scheduler_task.cancel()
                except Exception as ex:
                    self.logger.error(f"scheduler_task cancel failed")
                    pass

            self.logger.info("End Scheduler")
            self.scheduler_task = None
            del self.scheduler_task

        if self.site:
            self.logger.info("Stopping Site")
            self.site = None

        if self.healthcheck:
            self.logger.info("Stopping Healthcheck Thread")
            await self.healthcheck.stop()
            self.healthcheck = None

        if self.settings.db:
            self.logger.info("DB - Dispose Connections: " + self.settings.db_url)
            await self.db_engine.dispose()

    async def _init_graphql(self, strawberry_schema: schema) -> None:
        """
        Internal helper function to initialize the graphql router
        """
        if self.settings.graphql:
            from strawberry.fastapi import GraphQLRouter
            self.graphql_schema = strawberry_schema
            self.graphql_app = GraphQLRouter(self.graphql_schema, graphiql=True)
            self.include_router(self.graphql_app, prefix="/graphql", tags=["graphql"])

    async def get_healthcheck(self, request: Request) -> ORJSONResponse:
        """
        Get Healthcheck Status
        """
        self.logger.info("Called - get_healthcheck :" + str(request.url))
        msg: MSAHealthMessage = MSAHealthMessage()
        if not self.healthcheck:
            msg.message = "Healthcheck is disabled!"
        else:
            msg.healthy = self.healthcheck.is_healthy
            msg.message = await self.healthcheck.get_health()
            if len(self.healthcheck.error) > 0:
                msg.error = self.healthcheck.error

        return ORJSONResponse(content=jsonable_encoder(msg))

    async def get_scheduler_status(self, request: Request) -> MSASchedulerStatus:
        """
        Get Service Status Info
        """
        self.logger.info("Called - get_scheduler_status :" + str(request.url))
        sst: MSASchedulerStatus = MSASchedulerStatus()
        if not self.settings.scheduler:
            sst.name = self.settings.name
            sst.message = "Scheduler is disabled!"

        else:
            sst.name = self.settings.name
            for key, val in self.timers.timer_jobs.items():
                nt: MSATimerStatus = MSATimerStatus()
                nt.mode = key
                if isinstance(val, tuple):
                    nt.func = str(val[0])
                    nt.mark_HH_MM = str(val[1])
                else:
                    nt.func = str(val)
                sst.timers.append(nt)
            sst.message = "Scheduler is enabled!"

        return sst

    async def get_services_status(self, request: Request) -> MSAServiceStatus:
        """
        Get Service Status Info
        """
        self.logger.info("Called - get_services_status :" + str(request.url))
        sst: MSAServiceStatus = MSAServiceStatus()
        if not self.healthcheck:
            sst.name = self.settings.name
            sst.healthy = "disabled:400"
            sst.message = "Healthcheck is disabled!"

        else:
            sst.name = self.settings.name
            sst.healthy = await self.healthcheck.get_health()
            sst.message = "Healthcheck is enabled!"

        return sst

    def get_services_definition(self, request: Request) -> MSAServiceDefinition:
        """
        Get Service Definition Info
        """
        self.logger.info("Called - get_services_definition :" + str(request.url))
        return self.settings

    def get_services_settings(self, request: Request) -> ORJSONResponse:
        """
        Get Service OpenAPI Schema
        """
        self.logger.info("Called - get_services_settings :" + str(request.url))

        def try_get_json():
            try:

                return jsonable_encoder(self.settings)

            except Exception as e:
                return {"status": "error:400", "error": e.__str__()}

        return ORJSONResponse(
            {
                self.settings.name: try_get_json(),
            }

        )

    def get_services_openapi_schema(self, request: Request) -> ORJSONResponse:
        """
        Get Service OpenAPI Schema
        """
        self.logger.info("Called - get_services_openapi_schema :" + str(request.url))

        def try_get_json():
            try:

                return jsonable_encoder(self.openapi())

            except Exception as e:
                return {"status": "error:400", "error": e.__str__()}

        return ORJSONResponse(
            {
                self.settings.name: try_get_json(),
            }

        )

    def get_services_openapi_info(self, request: Request) -> MSAOpenAPIInfo:
        """
        Get Service OpenAPI Info
        """
        self.logger.info("Called - get_services_openapi_info :" + str(request.url))
        oai: MSAOpenAPIInfo = MSAOpenAPIInfo()

        try:
            oai.name = self.title
            oai.version = self.openapi_version
            oai.url = self.openapi_url
            oai.tags = self.openapi_tags
        except Exception as e:
            oai.tags = ["error:400 error" + e.__str__()]

        return oai

    async def validation_exception_handler(self, request: Request, exc: RequestValidationError) -> JSONResponse:
        self.logger.error("validation_exception_handler - " + str(exc.errors()))
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
        )

    async def msa_exception_handler_disabled(self, request: Request, exc: HTTPException) -> JSONResponse:
        """
        Handles all HTTPExceptions if Disabled with JSON Response.
        :param request:
        :type request:
        :param exc:
        :type exc:
        :return:
        :rtype:
        """

        error_content = jsonable_encoder({"status_code": exc.status_code,
                                          "detail": exc.detail,
                                          "args": exc.args,
                                          "headers": exc.headers,
                                          "request": request.url,
                                          })
        self.logger.error("msa_exception_handler_disabled - " + str(error_content))
        return JSONResponse(
            status_code=exc.status_code,
            content=error_content,
        )

    async def msa_exception_handler(self, request: Request, exc: HTTPException):
        """
        Handles all HTTPExceptions if enabled with HTML Response or forward error if the code is in the exclude settings list.
        :param request:
        :type request:
        :param exc:
        :type exc:
        :return:
        :rtype:
        """
        error_content = {'request': request, 'detail': exc.detail,
                         'status': exc.status_code,
                         "definitions": jsonable_encoder(self.settings)}
        self.logger.error("msa_exception_handler - " + str(error_content))
        if exc.status_code == 403:
            return self.templates.TemplateResponse('403.html', error_content)
        elif exc.status_code == 404:
            return self.templates.TemplateResponse('404.html', error_content)
        elif exc.status_code == 500:
            return self.templates.TemplateResponse('500.html', error_content)
        elif exc.status_code in self.settings.httpception_exclude:
            return await http_exception_handler(request, exc)
        else:
            # Generic error page
            return self.templates.TemplateResponse('error.html', error_content)

    def index_page(self, request: Request) -> _TemplateResponse:
        """
        Get Service Index.html Page
        """
        self.logger.info("Called - index_page :" + str(request.url))
        return self.templates.TemplateResponse("index.html",
                                               {"request": request,
                                                "settings": jsonable_encoder(self.settings),
                                                "definitions": jsonable_encoder(self.settings)})

    def testpage(self, request: Request) -> _TemplateResponse:
        """
        Simple Testpage to see if the Micro Service is up and running.
        Only works if pages is enabled in MSAServiceDefinition
        :param request:
        :return:
        """
        self.logger.info("Called - testpage :" + str(request.url))
        return self.templates.TemplateResponse("test.html",
                                               {"request": request,
                                                "settings": jsonable_encoder(self.settings)})

    async def monitor(self, request: Request) -> _TemplateResponse:
        """
        Simple Service Monitor Page.
        Only works if pages is enabled in MSAServiceDefinition
        :param request:
        :return:
        """
        self.logger.info("Called - monitor :" + str(request.url))
        sysinfo: MSASystemInfo = get_sysinfo()
        return self.templates.TemplateResponse("monitor.html",
                                               {"request": request,
                                                "outputSystemInfo": sysinfo})

    def profiler(self, request: Request) -> _TemplateResponse:
        """
        Simple Profiler Page.
        Only works if pages is enabled in MSAServiceDefinition
        :param request:
        :return:
        """
        self.logger.info("Called - profiler :" + str(request.url))
        return self.templates.TemplateResponse("profiler.html",
                                               {"request": request})

    async def monitor_inline(self, request: Request) -> _TemplateResponse:
        """
        Simple Monitor Page as Inline without head and body tags.
        Only works if pages is enabled in MSAServiceDefinition
        :param request:
        :return:
        """
        self.logger.info("Called - monitor_inline :" + str(request.url))
        sysinfo: MSASystemInfo = get_sysinfo()
        return self.templates.TemplateResponse("monitor_inline.html",
                                               {"request": request,
                                                "outputSystemInfo": sysinfo})
