import datetime
import os

import psutil
import typing
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.requests import Request
from starlette.responses import JSONResponse

from u2d_msa_sdk.errorhandling import getMSABaseExceptionHandler

sys_router = APIRouter(prefix="", tags=["system"], include_in_schema=True)


@sys_router.get('/sysinfo')
async def sysinfo(request: Request):
    """
    Get SystemInfo
    """
    sysinfo = {}
    try:
        sysinfo["OS_Name"] = os.uname().sysname
        sysinfo["Node_Name"] = os.uname().nodename
        sysinfo["OS_Release"] = os.uname().release
        sysinfo["OS_Version"] = os.uname().version
        sysinfo["HW_Identifier"] = os.uname().machine
        sysinfo["CPU_Physical"] = psutil.cpu_count(logical=False)
        sysinfo["CPU_Logical"] = os.cpu_count()
        sysinfo["Memory_Physical"] = str(round(psutil.virtual_memory().total / 1024000000., 2)) + " GB"
        sysinfo["Memory_Available"] = str(round(psutil.virtual_memory().available / 1024000000., 2)) + " GB"
        sysinfo["System_Boot"] = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        sysinfo["Service_Start"] = datetime.datetime.fromtimestamp(psutil.Process().create_time()).strftime(
            "%Y-%m-%d %H:%M:%S")
        sysinfo["Runtime_Exe"] = psutil.Process().exe()
        sysinfo["Runtime_Cmd"] = psutil.Process().cmdline()
        sysinfo["Runtime_Status"] = psutil.Process().status()
        sysinfo["CPU_Affinity"] = len(psutil.Process().cpu_affinity())
        sysinfo["PID"] = psutil.Process().pid
        sysinfo["CPU_Current"] = psutil.Process().cpu_num()

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System Information:")

    json_compatible_item_data = jsonable_encoder(sysinfo)
    return JSONResponse(content=json_compatible_item_data)


@sys_router.get('/syserror')
async def sys_error(request: Request):
    raise TypeError('MSA SDK System Test error...')