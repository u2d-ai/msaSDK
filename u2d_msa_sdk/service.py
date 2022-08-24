import os
from typing import Optional, Union, List

import httpx
from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers, InvalidPasswordException, models
from fastapi_users.models import UP, ID
from fastapi_users.password import PasswordHelper
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import Json
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import healthcheck as health
from u2d_msa_sdk.msaapi import MSAFastAPI
from u2d_msa_sdk.models.service import MSAServiceDefinition, MSAHealthDefinition
from passlib.context import CryptContext
import uvloop
from starlette_wtf import CSRFProtectMiddleware
from starception import StarceptionMiddleware

from u2d_msa_sdk.router.system import sys_router
from u2d_msa_sdk.security import getMSASecurity

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

#fastapi_users: FastAPIUsers = FastAPIUsers(BaseUserManager[UP, ID], security.auth_backends)


class NoMasterService(Exception):
    def __init__(self, msg="MSAServiceBase is running as Slave"):
        self.msg = msg


async def healthcheck():
    return JSONResponse({"status": os.getenv("API_HEALTH_RESPONSE", "MSA Service is running")})


def register_service(service_definition: MSAServiceDefinition):
    httpx.put(os.getenv("API_REGISTER_PATH"), json=service_definition.json())


class MSAApp(MSAFastAPI):
    def __init__(
            self,
            is_master=False,
            healthdefinition: MSAHealthDefinition = MSAHealthDefinition(),
            *args,
            **kwargs
    ) -> None:

        # call super class __init__
        uvloop.install()
        super().__init__(*args, **kwargs)

        self.is_master = is_master
        self.services = []
        self.healthchecks = {}

        self.add_api_route(healthdefinition.path, healthcheck)
        self.include_router(sys_router)
        #self.include_router(
        #    fastapi_users.get_auth_router(security.auth_backend_jwt), prefix="/auth/jwt", tags=["auth"]
        #)
        #self.include_router(
        #    fastapi_users.get_auth_router(security.auth_backend_cookie), prefix="/auth/jwt", tags=["auth"]
        #)
        self.add_middleware(StarceptionMiddleware)
        self.add_middleware(CORSMiddleware, allow_origins=getAllowedOrigins(),
                           allow_credentials=getAllowedCredentials(),
                           allow_methods=getAllowedMethods(),
                           allow_headers=getAllowedHeaders(), )
        # app.add_middleware(HTTPSRedirectMiddleware)
        # app.add_middleware(GZipMiddleware)
        self.add_middleware(SessionMiddleware, secret_key=getSecretKeySessions())
        self.add_middleware(CSRFProtectMiddleware, csrf_secret=getSecretKeyCSRF())

        if self.is_master:
            Instrumentator().instrument(self).expose(self)
            # add service registration
            self.add_api_route("/services/register", self.add_service)
            self.add_api_route("/services/status", self.get_services_status)
            self.add_api_route("/services/definition", self.get_services_openapi)

    async def get_services_status(self) -> JSONResponse:
        return JSONResponse(
            [
                {
                    "name": service.name,
                    "status": self.healthchecks[service.name].get_health()
                    if self.healthchecks.get(service.name, False)
                    else "No healthcheck!",
                }
                for service in self.services
            ]
        )

    async def add_service(self, service_definition: Json) -> JSONResponse:
        service_def: MSAServiceDefinition = MSAServiceDefinition.parse_obj(service_definition)
        self.services.append(service_def)
        if service_def.healthcheck:
            self.healthchecks[service_def.name] = health.MSAHealthCheck(
                service_def.healthcheck
            )
            self.healthchecks[service_def.name].start()
        return JSONResponse(
            [
                {
                    "name": service_def.name,
                    "status": "added"
                }
            ]
        )

    async def get_services_openapi(self) -> JSONResponse:
        def try_get_json(url):
            try:
                return httpx.get(url).json()
            except Exception as e:
                return {"status": "service is off"}

        return JSONResponse(
            [
                {
                    service.name: try_get_json(
                        "http://{}:{}/openapi.json".format(service.host, service.port)
                    ),
                }
                for service in self.services
            ]
        )
