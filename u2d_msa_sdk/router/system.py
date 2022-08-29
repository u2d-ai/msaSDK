
import typing
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from u2d_msa_sdk.utils.sysinfo import get_sysinfo

sys_router = APIRouter(prefix="", tags=["system"], include_in_schema=True)



@sys_router.get('/sysinfo', response_class=ORJSONResponse)
async def sysinfo(request: Request):
    """
    Get SystemInfo
    """
    sysinfo = await get_sysinfo()
    json_compatible_item_data = jsonable_encoder(sysinfo)
    return ORJSONResponse(content=json_compatible_item_data)


@sys_router.get('/syserror')
async def sys_error(request: Request):
    raise TypeError('MSA SDK System Test error...')