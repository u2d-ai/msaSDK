from typing import Dict
import datetime
import os
import psutil

from u2d_msa_sdk.errorhandling import getMSABaseExceptionHandler


async def get_sysinfo() -> Dict:
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

    return sysinfo
