# -*- coding: utf-8 -*-

from fastapi import APIRouter
from starlette.requests import Request

from msaSDK.utils.sysinfo import get_sysinfo, MSASystemInfo, MSASystemGPUInfo, get_sysgpuinfo

sys_router = APIRouter(prefix="", tags=["system"], include_in_schema=True)


@sys_router.get('/sysinfo', response_model=MSASystemInfo)
def system_info(request: Request) -> MSASystemInfo:
    """Get System Info

    Args:
        request: HTTP Request.

    Returns:
        sysinfo: MSASystemInfo Pydantic Model

    """
    sysinfo = get_sysinfo()
    return sysinfo


@sys_router.get('/sysgpuinfo', response_model=MSASystemGPUInfo)
def system_gpu_info(request: Request) -> MSASystemGPUInfo:
    """Get System Nvidia GPU's Info

    Args:
        request: HTTP Request.

    Returns:
        sysgpuinfo: MSASystemGPUInfo Pydantic Model

    """
    sysgpuinfo = get_sysgpuinfo()
    return sysgpuinfo


@sys_router.get('/syserror')
def system_test_error(request: Request) -> TypeError:
    """Create an Error to test the interception middleware.

    With an HTTP request it replies with an HTML Interception Page

    Args:
        request: HTTP Request.

    Raises:
        TypeError: TypeError('msaSDK System Test error...')



    """
    raise TypeError('msaSDK System Test error...')
