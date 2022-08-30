import socket
from typing import Dict, List, Union, Optional
import datetime
import os
import psutil

from u2d_msa_sdk.errorhandling import getMSABaseExceptionHandler

import decimal
import os
from subprocess import getoutput
from pydantic import BaseModel


class DiskIO(BaseModel):
    read_count: Optional[int]
    write_count: Optional[int]
    read_bytes: Optional[int]
    write_bytes: Optional[int]
    read_time: Optional[int]
    write_time: Optional[int]
    read_merged_count: Optional[int]
    write_merged_count: Optional[int]
    busy_time: Optional[int]


class NetworkIO(BaseModel):
    bytes_sent: Optional[int]
    bytes_recv: Optional[int]
    packets_sent: Optional[int]
    packets_recv: Optional[int]
    errin: Optional[int]
    errout: Optional[int]
    dropin: Optional[int]
    dropout: Optional[int]


class NetworkConnection(BaseModel):
    number: Optional[int]
    file_descriptor: Optional[int]
    family: Optional[int]
    type: Optional[int]
    local_addr: Optional[List[Union[int, str]]]
    remote_addr: Optional[List[Union[int, str]]]
    status: str = ""
    pid: Optional[int]


class NetworkAdapter(BaseModel):
    family: Optional[int]
    address: Optional[str]
    netmask: Optional[str]
    broadcast: Optional[str]
    ptp: Optional[int]


class NetworkAdapters(BaseModel):
    name: Optional[str]
    adapters: Optional[List[NetworkAdapter]]


class NetworkStat(BaseModel):
    isup: Optional[bool]
    duplex: Optional[int]
    speed: Optional[int]
    mtu: Optional[int]


class NetworkStats(BaseModel):
    name: Optional[str]
    adapters: Optional[List[NetworkStat]]


class Temperature(BaseModel):
    label: Optional[str]
    current: Optional[float]
    high: Optional[float]
    critical: Optional[float]


class Temperatures(BaseModel):
    device: Optional[str]
    temps: Optional[List[Temperature]]


class CPUFrequency(BaseModel):
    current: Optional[float]
    min: Optional[int]
    max: Optional[int]


class CPUTimes(BaseModel):
    user: Optional[float]
    nice: Optional[int]
    system: Optional[float]
    idle: Optional[float]
    iowait: Optional[float]
    irq: Optional[int]
    softirq: Optional[float]
    steal: Optional[int]
    guest: Optional[float]
    guest_nice: Optional[int]


class CPUStats(BaseModel):
    ctx_switches: Optional[int]
    interrupts: Optional[int]
    soft_interrupts: Optional[int]
    syscalls: Optional[int]


class MemoryUsage(BaseModel):
    total: Optional[float]
    available: Optional[float]
    used: Optional[float]
    free: Optional[float]
    percent: Optional[float]
    buffers: Optional[float]
    cached: Optional[float]
    active: Optional[float]
    inactive: Optional[float]


class Swap(BaseModel):
    total: Optional[float]
    used: Optional[float]
    free: Optional[float]
    percent: Optional[float]


class SystemInfo(BaseModel):
    OS_Name: str = ""
    Node_Name: str = ""
    Host_Name: str = ""
    OS_Release: str = ""
    OS_Version: str = ""
    HW_Identifier: str = ""
    CPU_Physical: Optional[int]
    CPU_Logical: Optional[int]
    Memory_Physical: str = ""
    Memory_Available: str = ""
    System_Boot: str = ""
    Service_Start: str = ""
    Runtime_Exe: str = ""
    Runtime_Cmd: List[str] = []
    Disk_IO: Optional[DiskIO]
    Network_IO: Optional[NetworkIO]
    Network_Connections: Optional[List[NetworkConnection]]
    Network_Adapters: Optional[List[NetworkAdapters]]
    Network_Stats: Optional[List[NetworkStats]]
    Temperatures: Optional[List[Temperatures]]
    CPU_Affinity: Optional[int]
    CPU_Frequency: Optional[CPUFrequency]
    CPU_Times: Optional[CPUTimes]
    CPU_Stats: Optional[CPUStats]
    PID: Optional[int]
    CPU_Current: Optional[int]
    CPU_Usage_Total: Optional[float]
    CPU_Usage_Process: Optional[float]
    CPU_Usage_Name: str = ""
    CPU_LoadAvg: Optional[List[float]]
    Memory_Usage: Optional[MemoryUsage]
    Swap: Optional[Swap]
    Runtime_Status: str = ""


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


async def get_cpu_freq() -> CPUFrequency:
    cpf: CPUFrequency = CPUFrequency()
    cpf.current, cpf.min, cpf.max = psutil.cpu_freq()
    return cpf


async def get_cpu_times() -> CPUTimes:
    cti: CPUTimes = CPUTimes()
    cti.user, cti.nice, cti.system, cti.idle, cti.iowait, cti.irq, cti.softirq, cti.steal, cti.guest, cti.guest_nice = psutil.cpu_times()
    return cti


async def get_cpu_stats() -> CPUStats:
    cst: CPUStats = CPUStats()
    cst.ctx_switches, cst.interrupts, cst.soft_interrupts, cst.syscalls = psutil.cpu_stats()
    return cst


async def get_disk_io() -> DiskIO:
    dio: DiskIO = DiskIO()
    dio.read_count, dio.write_count, dio.read_bytes, dio.write_bytes, dio.read_time, dio.write_time, \
        dio.read_merged_count, dio.write_merged_count, dio.busy_time = psutil.disk_io_counters()
    return dio


async def get_network_io() -> NetworkIO:
    nio: NetworkIO = NetworkIO()
    nio.bytes_sent, nio.bytes_recv, nio.packets_sent, nio.packets_recv, nio.errin, nio.errout, nio.dropin, nio.dropout = psutil.net_io_counters()
    return nio


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

        rdict: Dict = {"number": xi, "file_descriptor": fd, "family": family, "type": type, "local_addr": laddr,
                       "remote_addr": raddr,
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
    si: SystemInfo = SystemInfo()
    try:
        si.OS_Name = os.uname().sysname
        si.Node_Name = os.uname().nodename
        si.Host_Name = await get_hostname()
        si.OS_Release = os.uname().release
        si.OS_Version = os.uname().version
        si.HW_Identifier = os.uname().machine
        si.CPU_Physical = psutil.cpu_count(logical=False)
        si.CPU_Logical = os.cpu_count()
        si.Memory_Physical = str(round(psutil.virtual_memory().total / 1024000000., 2)) + " GB"
        si.Memory_Available = str(round(psutil.virtual_memory().available / 1024000000., 2)) + " GB"
        si.System_Boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        si.Service_Start = datetime.datetime.fromtimestamp(psutil.Process().create_time()).strftime(
            "%Y-%m-%d %H:%M:%S")
        si.Runtime_Exe = psutil.Process().exe()
        si.Runtime_Cmd = psutil.Process().cmdline()
        si.PID = psutil.Process().pid
        si.CPU_Current = psutil.Process().cpu_num()
        si.Disk_IO = await get_disk_io()
        si.Network_IO = await get_network_io()
        si.CPU_Times = await get_cpu_times()
        si.CPU_Stats = await get_cpu_stats()
        si.CPU_Frequency = await get_cpu_freq()
        si.CPU_Affinity = len(psutil.Process().cpu_affinity())
        #print(si)

        # old
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
        sysinfo["PID"] = psutil.Process().pid
        sysinfo["CPU_Current"] = psutil.Process().cpu_num()
        sysinfo["Disk_IO"] = await get_disk_io()
        sysinfo["Network_IO"] = await get_network_io()
        sysinfo["CPU_Times"] = await get_cpu_times()
        sysinfo["CPU_Stats"] = await get_cpu_stats()
        sysinfo["CPU_Frequency"] = await get_cpu_freq()
        sysinfo["CPU_Affinity"] = len(psutil.Process().cpu_affinity())

        # not yet in si
        sysinfo["Network_Connections"] = await get_network_connections()
        sysinfo["Network_Adapters_Definition"] = {"name": [["family", "address", "netmask", "broadcast", "ptp"]]}
        sysinfo["Network_Adapters"] = psutil.net_if_addrs()
        sysinfo["Network_Stats_Definition"] = {"name": ["isup", "duplex", "speed", "mtu"]}
        sysinfo["Network_Stats"] = psutil.net_if_stats()
        sysinfo["Temperatures_Definition"] = {"device_name": ["label", "current", "high", "critical"]}
        sysinfo["Temperatures"] = psutil.sensors_temperatures()
        sysinfo["CPU_Usage_Total"], sysinfo["CPU_Usage_Process"], sysinfo["CPU_Usage_Name"] = await get_cpu_usage()
        sysinfo["CPU_LoadAvg"] = await get_load_avarage()
        sysinfo["Memory_Usage"] = await get_memory_usage()
        sysinfo["Swap"] = await get_swap()
        sysinfo["Runtime_Status"] = psutil.Process().status() + " / " + str(int(sysinfo["CPU_LoadAvg"][0])) + "%"

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System Information:")

    return sysinfo
