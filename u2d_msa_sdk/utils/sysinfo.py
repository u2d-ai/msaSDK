# -*- coding: utf-8 -*-
__version__ = '0.0.3'

import datetime
import decimal
import os
import re
import socket
import uuid
from subprocess import getoutput
from typing import Dict, List, Optional
import GPUtil
import psutil
from pydantic import BaseModel

from u2d_msa_sdk.utils.errorhandling import getMSABaseExceptionHandler


class MSAGPUInfo(BaseModel):
    id: Optional[int]
    name: Optional[str]
    load: Optional[str]
    free_memory: Optional[str]
    used_memory: Optional[str]
    total_memory: Optional[str]
    temperature: Optional[str]
    uuid: Optional[str]


class MSADiskIO(BaseModel):
    read_count: Optional[int]
    write_count: Optional[int]
    read_bytes: Optional[int]
    write_bytes: Optional[int]
    read_time: Optional[int]
    write_time: Optional[int]
    read_merged_count: Optional[int]
    write_merged_count: Optional[int]
    busy_time: Optional[int]


class MSANetworkIO(BaseModel):
    bytes_sent: Optional[int]
    bytes_recv: Optional[int]
    packets_sent: Optional[int]
    packets_recv: Optional[int]
    errin: Optional[int]
    errout: Optional[int]
    dropin: Optional[int]
    dropout: Optional[int]


class MSANetworkConnection(BaseModel):
    index: Optional[int]
    file_descriptor: Optional[int]
    family: Optional[int]
    type: Optional[int]
    local_addr: Optional[str]
    remote_addr: Optional[str]
    status: str = ""
    pid: Optional[int]


class MSANetworkAdapter(BaseModel):
    family: Optional[int]
    address: Optional[str]
    netmask: Optional[str]
    broadcast: Optional[str]
    ptp: Optional[int]


class MSANetworkAdapters(BaseModel):
    name: str = ""
    adapters: List[MSANetworkAdapter] = []


class MSANetworkStat(BaseModel):
    isup: Optional[bool]
    duplex: Optional[int]
    speed: Optional[int]
    mtu: Optional[int]


class NetworkStats(BaseModel):
    name: str = ""
    adapters: List[MSANetworkStat] = []


class MSATemperature(BaseModel):
    label: Optional[str]
    current: Optional[float]
    high: Optional[float]
    critical: Optional[float]


class MSATemperatures(BaseModel):
    device: str = ""
    temps: List[MSATemperature] = []


class MSACPUFrequency(BaseModel):
    current: Optional[float]
    min: Optional[int]
    max: Optional[int]


class MSACPUTimes(BaseModel):
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


class MSACPUStats(BaseModel):
    ctx_switches: Optional[int]
    interrupts: Optional[int]
    soft_interrupts: Optional[int]
    syscalls: Optional[int]


class MSAMemoryUsage(BaseModel):
    total: Optional[float]
    available: Optional[float]
    used: Optional[float]
    free: Optional[float]
    percent: Optional[float]
    buffers: Optional[float]
    cached: Optional[float]
    active: Optional[float]
    inactive: Optional[float]


class MSASwap(BaseModel):
    total: Optional[float]
    used: Optional[float]
    free: Optional[float]
    percent: Optional[float]


class MSASystemInfo(BaseModel):
    OS_Name: str = ""
    Node_Name: str = ""
    Host_Name: str = ""
    OS_Release: str = ""
    OS_Version: str = ""
    HW_Identifier: str = ""
    IP_Address: str = ""
    MAC_Address: str = ""
    CPU_Physical: Optional[int]
    CPU_Logical: Optional[int]
    Memory_Physical: str = ""
    Memory_Available: str = ""
    System_Boot: str = ""
    Service_Start: str = ""
    Runtime_Exe: str = ""
    Runtime_Cmd: List[str] = []
    Disk_IO: Optional[MSADiskIO]
    Network_IO: Optional[MSANetworkIO]
    Network_Connections: Optional[List[MSANetworkConnection]]
    Network_Adapters: Optional[List[MSANetworkAdapters]]
    Network_Stats: Optional[List[NetworkStats]]
    Temperatures: Optional[List[MSATemperatures]]
    CPU_Affinity: Optional[int]
    CPU_Frequency: Optional[MSACPUFrequency]
    CPU_Times: Optional[MSACPUTimes]
    CPU_Stats: Optional[MSACPUStats]
    PID: Optional[int]
    CPU_Current: Optional[int]
    CPU_Usage_Total: Optional[float]
    CPU_Usage_Process: Optional[float]
    CPU_Usage_Name: str = ""
    CPU_LoadAvg: Optional[List[float]]
    Memory_Usage: Optional[MSAMemoryUsage]
    Swap: Optional[MSASwap]
    Runtime_Status: str = ""


class MSASystemGPUInfo(BaseModel):
    OS_Name: str = ""
    Node_Name: str = ""
    Host_Name: str = ""
    OS_Release: str = ""
    OS_Version: str = ""
    HW_Identifier: str = ""
    IP_Address: str = ""
    MAC_Address: str = ""
    CPU_Physical: Optional[int]
    CPU_Logical: Optional[int]
    Memory_Physical: str = ""
    Memory_Available: str = ""
    System_Boot: str = ""
    Service_Start: str = ""
    Runtime_Exe: str = ""
    Runtime_Cmd: List[str] = []
    PID: Optional[int]
    GPUs: Optional[List[MSAGPUInfo]]
    Runtime_Status: str = ""


def get_hostname():
    hostname = (socket.gethostname())
    return hostname


def get_list_partitions() -> List:
    partitions_list = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partitions_list.append(partition[1])
    return partitions_list


def get_gpus() -> List[MSAGPUInfo]:
    gpus = GPUtil.getGPUs()
    list_gpus: List[MSAGPUInfo] = []
    for gpu in gpus:
        ng: MSAGPUInfo = MSAGPUInfo()
        # get the GPU id
        ng.id = gpu.id
        # name of GPU
        ng.name = gpu.name
        # get % percentage of GPU usage of that GPU
        ng.load = f"{gpu.load * 100}%"
        # get free memory in MB format
        ng.free_memory = f"{gpu.memoryFree}MB"
        # get used memory
        ng.used_memory = f"{gpu.memoryUsed}MB"
        # get total memory
        ng.total_memory = f"{gpu.memoryTotal}MB"
        # get GPU temperature in Celsius
        ng.temperature = f"{gpu.temperature} °C"
        ng.uuid = gpu.uuid
        list_gpus.append(ng)
    return list_gpus


def get_partition_usage(partitions) -> Dict:
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


def get_map_disk_usage():
    MapUsage: Dict = get_partition_usage(get_list_partitions())
    disk = MapUsage["partition"]
    total = MapUsage["total"]
    used = MapUsage["used"]
    free = MapUsage["free"]
    percent = MapUsage["percent"]
    rdict = dict(zip(disk, zip(total, used, free, percent)))
    return rdict


def get_memory_usage() -> MSAMemoryUsage:
    mu: MSAMemoryUsage = MSAMemoryUsage()
    memory = psutil.virtual_memory()

    mu.total = memory.total / 1024 / 1024
    mu.available = memory.available / 1024 / 1024
    mu.used = memory.used / 1024 / 1024
    mu.free = memory.free / 1024 / 1024
    mu.percent = memory.percent
    mu.buffers = memory.buffers / 1024 / 1024
    mu.cached = memory.cached / 1024 / 1024
    mu.active = memory.active / 1024 / 1024
    mu.inactive = memory.inactive / 1024 / 1024
    return mu


def get_cpu_freq() -> MSACPUFrequency:
    cpf: MSACPUFrequency = MSACPUFrequency()
    cpf.current, cpf.min, cpf.max = psutil.cpu_freq()
    return cpf


def get_cpu_times() -> MSACPUTimes:
    cti: MSACPUTimes = MSACPUTimes()
    cti.user, cti.nice, cti.system, cti.idle, cti.iowait, cti.irq, cti.softirq, \
        cti.steal, cti.guest, cti.guest_nice = psutil.cpu_times()
    return cti


def get_cpu_stats() -> MSACPUStats:
    cst: MSACPUStats = MSACPUStats()
    cst.ctx_switches, cst.interrupts, cst.soft_interrupts, cst.syscalls = psutil.cpu_stats()
    return cst


def get_disk_io() -> MSADiskIO:
    dio: MSADiskIO = MSADiskIO()
    dio.read_count, dio.write_count, dio.read_bytes, dio.write_bytes, dio.read_time, dio.write_time, \
        dio.read_merged_count, dio.write_merged_count, dio.busy_time = psutil.disk_io_counters()
    return dio


def get_network_io() -> MSANetworkIO:
    nio: MSANetworkIO = MSANetworkIO()
    nio.bytes_sent, nio.bytes_recv, nio.packets_sent, nio.packets_recv, nio.errin, \
        nio.errout, nio.dropin, nio.dropout = psutil.net_io_counters()
    return nio


def get_network_adapters() -> List[MSANetworkAdapters]:
    ret: List[MSANetworkAdapters] = []
    la: Dict = psutil.net_if_addrs()

    for key, val in la.items():
        na: MSANetworkAdapters = MSANetworkAdapters()
        na.name = key
        for entry in val:
            la_entry: MSANetworkAdapter = MSANetworkAdapter()
            la_entry.family = entry[0]
            la_entry.address = entry[1]
            la_entry.netmask = entry[2]
            la_entry.broadcast = entry[3]
            la_entry.ptp = entry[4]
            na.adapters.append(la_entry)
        ret.append(na)
    return ret


def get_temperatures() -> List[MSATemperatures]:
    ret: List[MSATemperatures] = []
    ta: Dict = psutil.sensors_temperatures()
    for key, val in ta.items():
        tp: MSATemperatures = MSATemperatures()
        tp.device = key
        for entry in val:
            tp_entry: MSATemperature = MSATemperature()
            tp_entry.label = entry[0]
            tp_entry.current = entry[1]
            tp_entry.high = entry[2]
            tp_entry.critical = entry[3]
            tp.temps.append(tp_entry)
        ret.append(tp)
    return ret


def get_network_stats() -> List[NetworkStats]:
    ret: List[NetworkStats] = []
    net_stats: Dict = psutil.net_if_stats()
    for key, entry in net_stats.items():
        ns: NetworkStats = NetworkStats()
        ns.name = key
        ns_entry: MSANetworkStat = MSANetworkStat()
        ns_entry.isup = entry[0]
        ns_entry.duplex = entry[1]
        ns_entry.speed = entry[2]
        ns_entry.mtu = entry[3]
        ns.adapters.append(ns_entry)
        ret.append(ns)
    return ret


def get_network_connections() -> List[MSANetworkConnection]:
    rlist: List = []
    inlist = psutil.net_connections()
    for xi, entry in enumerate(inlist):
        nc: MSANetworkConnection = MSANetworkConnection()
        nc.index = xi
        nc.file_descriptor = entry[0]
        nc.family = entry[1]
        nc.type = entry[2]

        nc.local_addr = str(entry[3])
        nc.remote_addr = str(entry[4])

        nc.status = entry[5]
        nc.pid = entry[6]
        rlist.append(nc)
    return rlist


def get_swap() -> MSASwap:
    swap = psutil.swap_memory()
    sw: MSASwap = MSASwap()
    sw.total = swap.total / 1024 / 1024
    sw.used = swap.used / 1024 / 1024
    sw.free = swap.free / 1024 / 1024
    sw.percent = swap.percent
    return sw


def get_load_average():
    return [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]


def get_cpu_usage(user=None, ignore_self=False):
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


def get_sysinfo() -> MSASystemInfo:
    """
    Get MSASystemInfo
    """
    si: MSASystemInfo = MSASystemInfo()
    try:
        si.OS_Name = os.uname().sysname
        si.Node_Name = os.uname().nodename
        si.Host_Name = get_hostname()
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
        si.Disk_IO = get_disk_io()
        si.Network_IO = get_network_io()
        si.CPU_Times = get_cpu_times()
        si.CPU_Stats = get_cpu_stats()
        si.CPU_Frequency = get_cpu_freq()
        si.CPU_Affinity = len(psutil.Process().cpu_affinity())
        si.Memory_Usage = get_memory_usage()
        si.CPU_LoadAvg = get_load_average()
        si.CPU_Usage_Total, si.CPU_Usage_Process, si.CPU_Usage_Name = get_cpu_usage()
        si.Runtime_Status = psutil.Process().status()
        si.Network_Adapters = get_network_adapters()
        si.Temperatures = get_temperatures()
        si.Network_Connections = get_network_connections()
        si.Swap = get_swap()
        si.Network_Stats = get_network_stats()
        si.IP_Address = socket.gethostbyname(socket.gethostname())
        si.MAC_Address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System Information:")

    return si


def get_sysgpuinfo() -> MSASystemGPUInfo:
    """
    Get MSASystemGPUInfo
    """
    si: MSASystemGPUInfo = MSASystemGPUInfo()
    try:
        si.OS_Name = os.uname().sysname
        si.Node_Name = os.uname().nodename
        si.Host_Name = get_hostname()
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
        si.Runtime_Status = psutil.Process().status()
        si.PID = psutil.Process().pid
        si.GPUs = get_gpus()
        si.IP_Address = socket.gethostbyname(socket.gethostname())
        si.MAC_Address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System GPU Information:")

    return si