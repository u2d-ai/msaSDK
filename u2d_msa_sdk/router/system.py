from fastapi import APIRouter
from starlette.requests import Request

from u2d_msa_sdk.utils.sysinfo import get_sysinfo, SystemInfo, SystemGPUInfo, get_sysgpuinfo

sys_router = APIRouter(prefix="", tags=["system"], include_in_schema=True)


@sys_router.get('/sysinfo', response_model=SystemInfo)
def system_info(request: Request):
    """
    Get System Info
    """
    sysinfo = get_sysinfo()
    return sysinfo


@sys_router.get('/sysgpuinfo', response_model=SystemGPUInfo)
def system_gpu_info(request: Request):
    """
    Get System Nvidia GPU's Info
    """
    sysgpuinfo = get_sysgpuinfo()
    return sysgpuinfo


@sys_router.get('/syserror')
def system_test_error(request: Request):
    """
    Create a Error to test the interception middleware.
    With a HTTP request it replies with a HTML Interception Page
    """
    raise TypeError('MSA SDK System Test error...')