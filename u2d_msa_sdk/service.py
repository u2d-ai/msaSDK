import os
from typing import List

import uvloop
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi_users.password import PasswordHelper
from fastapi_utils.api_settings import get_api_settings
from passlib.context import CryptContext
from prometheus_fastapi_instrumentator import Instrumentator
from starception import StarceptionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette_wtf import CSRFProtectMiddleware

import healthcheck as health
from u2d_msa_sdk.models.health import MSAHealthMessage
from u2d_msa_sdk.models.service import MSAServiceDefinition, MSAHealthDefinition
from u2d_msa_sdk.msaapi import MSAFastAPI
from u2d_msa_sdk.router.system import sys_router
from u2d_msa_sdk.security import getMSASecurity
from strawberry import fastapi as fgraph , schema


context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password_helper = PasswordHelper(context)
security = getMSASecurity()


def getSecretKey():
    ret_key: str = os.getenv("SECRET_KEY_TOKEN",
                             "u2dmsaservicex_#M8A{1o3Bd?<ipwt^K},Z)OE<Fkj-X9IILWq|Cf`Y:HFI~&2L%Ion3}+p{T%")
    return ret_key


def getSecretKeySessions():
    ret_key: str = os.getenv("SECRET_KEY_SESSIONS",
                             "u2dmsaserviceeP)zg5<g@4WJ0W8'?ad!T9UBvW1z2k|y~|Pgtewv=H?GY_Q]t~-~UUe'pJ0V[>!<)")
    return ret_key


def getSecretKeyCSRF():
    ret_key: str = os.getenv("SECRET_KEY_CSRF",
                             "u2dmsaservicee_rJM'onkEV1trD=I7dci$flB)aSNW+raL4j]Ww=n~_BRg35*3~(E.>rx`1aTw:s")
    return ret_key


def getAllowedOrigins() -> List[str]:
    origins: List[str] = [os.getenv("ALLOWED_ORIGINS", "*")]
    return origins


def getAllowedMethods() -> List[str]:
    methods: List[str] = [os.getenv("ALLOWED_METHODS", "*")]
    return methods


def getAllowedHeaders() -> List[str]:
    headers: List[str] = [os.getenv("ALLOWED_HEADERS", "*")]
    return headers


def getAllowedCredentials() -> bool:
    cred: bool = os.getenv("ALLOWED_CREDENTIALS", True)
    return cred


class MSAApp(MSAFastAPI):
    def __init__(
            self,
            service_definition: MSAServiceDefinition = MSAServiceDefinition(),
            *args,
            **kwargs
    ) -> None:
        # call super class __init__
        super().__init__(*args, **kwargs)
        self.msa_settings = get_api_settings()
        self.service_definition: MSAServiceDefinition = service_definition
        self.healthdefinition: MSAHealthDefinition = self.service_definition.healthdefinition

        if self.service_definition.uvloop:
            uvloop.install()
        self.healthcheck: health.MSAHealthCheck = None

        self.ROOTPATH = os.path.join(os.path.dirname(__file__))
        if self.service_definition.graphql:
            from strawberry.fastapi import GraphQLRouter
            self.graphql_app: GraphQLRouter = None
            self.graphql_schema: schema = None

        if self.healthdefinition.enabled:
            self.healthcheck = health.MSAHealthCheck(
                healthdefinition=self.healthdefinition,
                host=self.service_definition.host,
                port=self.service_definition.port
            )
            self.healthcheck.start()
            self.add_api_route(self.healthdefinition.path, self.get_healthcheck,
                               response_model=MSAHealthMessage,
                               tags=["service"])

        if self.service_definition.sysrouter:
            self.include_router(sys_router)

        if self.service_definition.starception:
            self.add_middleware(StarceptionMiddleware)

        if self.service_definition.cors:
            self.add_middleware(CORSMiddleware, allow_origins=getAllowedOrigins(),
                                allow_credentials=getAllowedCredentials(),
                                allow_methods=getAllowedMethods(),
                                allow_headers=getAllowedHeaders(), )
        if self.service_definition.redirect:
            self.add_middleware(HTTPSRedirectMiddleware)
        if self.service_definition.gzip:
            self.add_middleware(GZipMiddleware)
        if self.service_definition.session:
            self.add_middleware(SessionMiddleware, secret_key=getSecretKeySessions())
        if self.service_definition.csrf:
            self.add_middleware(CSRFProtectMiddleware, csrf_secret=getSecretKeyCSRF())

        if self.service_definition.instrument:
            Instrumentator().instrument(app=self).expose(app=self, tags=["service"])

        if self.service_definition.servicerouter:
            self.add_api_route("/status", self.get_services_status, tags=["service"])
            self.add_api_route("/definition", self.get_services_definition, tags=["service"])
            self.add_api_route("/schema", self.get_services_openapi_schema, tags=["openapi"])
            self.add_api_route("/info", self.get_services_openapi_info, tags=["openapi"])

        if self.service_definition.static or self.service_definition.pages:
            self.mount("/msastatic", StaticFiles(directory="msastatic"), name="msastatic")
        if self.service_definition.templates or self.service_definition.pages:
            self.templates = Jinja2Templates(directory="msatemplates")
        if self.service_definition.pages:
            self.add_api_route("/", self.index_page, tags=["pages"])
            self.add_api_route("/testpage", self.testpage, tags=["pages"])

    async def init_graphql(self, strawberry_schema: schema):
        if self.service_definition.graphql:
            from strawberry.fastapi import GraphQLRouter
            self.graphql_schema = strawberry_schema
            self.graphql_app = GraphQLRouter(self.graphql_schema, graphiql=True)
            self.include_router(self.graphql_app, prefix="/graphql", tags=["graphql"])

    async def get_healthcheck(self) -> ORJSONResponse:
        msg: MSAHealthMessage = MSAHealthMessage()
        if not self.healthcheck:
            msg.message = "Healthcheck is disabled!"
        else:
            msg.healthy = self.healthcheck.is_healthy,
            msg.message = await self.healthcheck.get_health()
            if len(self.healthcheck.error)>0:
                msg.error = self.healthcheck.error

        return ORJSONResponse(content=jsonable_encoder(msg))

    async def get_services_status(self) -> ORJSONResponse:
        if not self.healthcheck:
            return ORJSONResponse(
                {
                    "name": self.service_definition.name,
                    "healthy": "disabled:400",
                    "message": "Healthcheck is disabled!",
                }
            )
        else:
            return ORJSONResponse(
                {
                    "name": self.service_definition.name,
                    "healthy": await self.healthcheck.get_health(),
                    "message": "Healthcheck is enabled!",
                }
            )

    async def get_services_definition(self) -> ORJSONResponse:
        if not self.healthcheck:
            return ORJSONResponse(
                {
                    "name": self.service_definition.name,
                    "definition": jsonable_encoder(self.service_definition)
                }
            )
        else:
            return ORJSONResponse(
                {
                    "name": self.service_definition.name,
                    "definition": jsonable_encoder(self.service_definition)
                }
            )

    async def get_services_openapi_schema(self) -> ORJSONResponse:
        def try_get_json():
            try:

                return jsonable_encoder(self.openapi())

            except Exception as e:
                return {"status": "error:400", "error": e.__str__()}

        return ORJSONResponse(
            {
                self.service_definition.name: try_get_json(),
            }

        )

    async def get_services_openapi_info(self) -> ORJSONResponse:
        def try_get_json():
            try:

                return {"version": self.openapi_version,"url": self.openapi_url, "tags": self.openapi_tags}

            except Exception as e:
                return {"status": "error:400", "error": e.__str__()}

        return ORJSONResponse(
            {
                self.service_definition.name: try_get_json(),
            }

        )

    async def index_page(self, request: Request):
        return self.templates.TemplateResponse("index.html",
                                               {"request": request,
                                                "settings": jsonable_encoder(self.msa_settings)})

    async def testpage(self, request: Request):
        """
        Simple Testpage to see if the Micro Service is up and running.
        Only works if pages is enabled in MSAServiceDefinition
        :param request:
        :return:
        """
        return self.templates.TemplateResponse("test.html",
                                               {"request": request,
                                                "settings": jsonable_encoder(self.msa_settings)})
