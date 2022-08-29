import socket
from typing import Dict, List
import datetime
import os
import psutil

from u2d_msa_sdk.errorhandling import getMSABaseExceptionHandler

import decimal
import os
from subprocess import getoutput


async def get_hostname():
    hostname = (socket.gethostname())
    return hostname


async def get_list_partitions() -> List:
    partitions_list = []
    path_list = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partitions_list.append(partition[1])
    return partitions_list


async def get_partition_usage(partitions) -> Dict:
    lspartition = []
    lstotal = []
    lsused = []
    lsfree = []
    lspercent = []
    for partition in partitions:
        usage = psutil.disk_usage(partition)
        total, used, free, percent = usage
        lspartition.append(partition)
        lstotal.append(total // (2 ** 30))
        lsused.append(used // (2 ** 30))
        lsfree.append(free // (2 ** 30))
        lspercent.append(percent)
    ret: Dict = {"partition": lspartition, "total": lstotal, "used": lsused, "free": lsfree, "percent": lspercent}
    return ret


async def get_map_disk_usage():
    MapUsage: Dict = await get_partition_usage(await get_list_partitions())
    rdict = {}
    y = 0
    disk, total, used, free, percent = MapUsage["partition"], MapUsage["total"], MapUsage["used"], MapUsage["free"], \
                                       MapUsage["percent"]
    rdict = dict(zip(disk, zip(total, used, free, percent)))
    return rdict


async def get_memory_usage() -> Dict:
    memory = psutil.virtual_memory()
    meminfo = {}
    meminfo['total'] = memory.total / 1024 / 1024
    meminfo['available'] = memory.available / 1024 / 1024
    meminfo['used'] = memory.used / 1024 / 1024
    meminfo['free'] = memory.free / 1024 / 1024
    meminfo['percent'] = memory.percent
    meminfo['buffers'] = memory.buffers / 1024 / 1024
    meminfo['cached'] = memory.cached / 1024 / 1024
    meminfo['active'] = memory.active / 1024 / 1024
    meminfo['inactive'] = memory.inactive / 1024 / 1024
    return meminfo


async def get_disk_io() -> Dict:
    print(psutil.disk_io_counters())
    read_count, write_count, read_bytes, write_bytes, read_time, write_time, read_merged_count, write_merged_count, busy_time = psutil.disk_io_counters()
    rdict: Dict = {"read_count": read_count, "write_count": write_count, "read_bytes": read_bytes,
                   "write_bytes": write_bytes, "read_time": read_time, "write_time": write_time,
                   "read_merged_count": read_merged_count, "write_merged_count": write_merged_count,
                   "busy_time": busy_time}
    return rdict


async def get_network_io() -> Dict:
    bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout = psutil.net_io_counters()
    rdict: Dict = {"bytes_sent": bytes_sent, "bytes_recv": bytes_recv, "packets_sent": packets_sent,
                   "packets_recv": packets_recv, "errin": errin, "errout": errout,
                   "dropin": dropin, "dropout": dropout}
    return rdict


async def get_network_connections() -> List:
    rlist: List = []
    inlist = psutil.net_connections()
    for xi, entry in enumerate(inlist):

        fd = entry[0]
        family = entry[1]
        type = entry[2]
        laddr = entry[3]
        raddr = entry[4]
        status = entry[5]
        pid = entry[6]

        rdict: Dict = {"number": xi, "file_descriptor": fd, "family": family, "type": type, "local_addr": laddr, "remote_addr": raddr,
                       "status": status, "pid": pid}
        rlist.append(rdict)
    return rlist


async def get_swap() -> Dict:
    swap = psutil.swap_memory()
    swapinfo = {}
    swapinfo['total'] = swap.total / 1024 / 1024
    swapinfo['used'] = swap.used / 1024 / 1024
    swapinfo['free'] = swap.free / 1024 / 1024
    swapinfo['percent'] = swap.percent
    return swapinfo


async def get_load_avarage():
    return [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]


async def get_cpu_usage(user=None, ignore_self=False):
    """
    Returns the total CPU usage for all available cores.
    :param user: If given, returns only the total CPU usage of all processes
      for the given user.
    :param ignore_self: If ``True`` the process that runs this script will
      be ignored.
    """
    pid = os.getpid()
    cmd = "ps aux"
    output = getoutput(cmd)
    total = 0
    largest_process = 0
    largest_process_name = None
    for row in output.split('\n')[1:]:
        row = row.split()
        if row[1] == str(pid) and ignore_self:
            continue
        if user is None or user == row[0]:
            cpu = decimal.Decimal(row[2])
            if cpu > total:
                largest_process = cpu
                largest_process_name = ' '.join(row[10:len(row)])
            total += decimal.Decimal(row[2])
    return total, largest_process, largest_process_name


async def get_sysinfo() -> Dict:
    """
    Get SystemInfo
    """
    sysinfo = {}
    try:
        sysinfo["OS_Name"] = os.uname().sysname
        sysinfo["Node_Name"] = os.uname().nodename
        sysinfo["Host_Name"] = await get_hostname()
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
        sysinfo["Disk_IO"] = await get_disk_io()
        sysinfo["Network_IO"] = await get_network_io()
        sysinfo["Network_Connections"] = await get_network_connections()
        sysinfo["Network_Adapters_Definition"] = {"name": [["family", "address", "netmask", "broadcast", "ptp"]]}
        sysinfo["Network_Adapters"] = psutil.net_if_addrs()
        sysinfo["Network_Stats_Definition"] = {"device_name": ["label", "current", "high", "critical"]}
        sysinfo["Network_Stats"] = psutil.net_if_stats()
        sysinfo["Temperatures_Definition"] = psutil.sensors_temperatures()
        sysinfo["Temperatures"] = psutil.sensors_temperatures()
        sysinfo["CPU_Affinity"] = len(psutil.Process().cpu_affinity())
        sysinfo["CPU_Frequency"] = psutil.cpu_freq()
        sysinfo["CPU_Times"] = psutil.cpu_times()
        sysinfo["CPU_Stats"] = psutil.cpu_stats()
        sysinfo["PID"] = psutil.Process().pid
        sysinfo["CPU_Current"] = psutil.Process().cpu_num()
        sysinfo["CPU_Usage_Total"], sysinfo["CPU_Usage_Process"], sysinfo["CPU_Usage_Name"] = await get_cpu_usage()
        sysinfo["CPU_LoadAvg"] = await get_load_avarage()
        sysinfo["Memory_Usage"] = await get_memory_usage()
        sysinfo["Swap"] = await get_swap()
        sysinfo["Runtime_Status"] = psutil.Process().status() + " / " + str(int(sysinfo["CPU_LoadAvg"][0])) + "%"

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System Information:")

    return sysinfo
