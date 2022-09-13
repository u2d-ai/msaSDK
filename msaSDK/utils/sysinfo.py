# -*- coding: utf-8 -*-
"""Provides System Information about devices, OS etc."""

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
from sqlmodel import SQLModel
from msaSDK.utils.errorhandling import getMSABaseExceptionHandler


class MSAGPUInfo(SQLModel):
    """Pydantic GPU Info Model."""
    id: Optional[int]
    name: Optional[str]
    load: Optional[str]
    free_memory: Optional[str]
    used_memory: Optional[str]
    total_memory: Optional[str]
    temperature: Optional[str]
    uuid: Optional[str]


class MSADiskIO(SQLModel):
    """Pydantic Disk IO Info Model.

        Attributes:
            read_count: number of reads
            write_count: number of writes
            read_bytes: number of bytes read
            write_bytes: number of bytes written
            read_time: (all except NetBSD and OpenBSD) time spent reading from disk (in milliseconds)
            write_time: (all except NetBSD and OpenBSD) time spent writing to disk (in milliseconds)
            busy_time: (Linux, FreeBSD) time spent doing actual I/Os (in milliseconds)
            read_merged_count (Linux): number of merged reads (see iostats doc)
            write_merged_count (Linux): number of merged writes (see iostats doc)

    """
    read_count: Optional[int]
    write_count: Optional[int]
    read_bytes: Optional[int]
    write_bytes: Optional[int]
    read_time: Optional[int]
    write_time: Optional[int]
    read_merged_count: Optional[int]
    write_merged_count: Optional[int]
    busy_time: Optional[int]


class MSANetworkIO(SQLModel):
    """Pydantic Network IO Info Model.

        Attributes:
            bytes_sent: number of bytes sent
            bytes_recv: number of bytes received
            packets_sent: number of packets sent
            packets_recv: number of packets received
            errin: total number of errors while receiving
            errout: total number of errors while sending
            dropin: total number of incoming packets which were dropped
            dropout: total number of outgoing packets which were dropped (always 0 on macOS and BSD)
    """
    bytes_sent: Optional[int]
    bytes_recv: Optional[int]
    packets_sent: Optional[int]
    packets_recv: Optional[int]
    errin: Optional[int]
    errout: Optional[int]
    dropin: Optional[int]
    dropout: Optional[int]


class MSANetworkConnection(SQLModel):
    """Pydantic Network Connection Info Model."""
    index: Optional[int]
    file_descriptor: Optional[int]
    """the socket file descriptor. If the connection refers to the current process this may be passed to socket.fromfd to obtain a usable socket object. On Windows and SunOS this is always set to -1."""
    family: Optional[int]
    """the address family, either AF_INET, AF_INET6 or AF_UNIX."""
    type: Optional[int]
    """the address type, either ``SOCK_STREAM``, ``SOCK_DGRAM`` or ``SOCK_SEQPACKET``."""
    local_addr: Optional[str]
    """the local address as a ``(ip, port)`` named tuple or a ``path`` in case of AF_UNIX sockets. For UNIX sockets see notes below."""
    remote_addr: Optional[str]
    """the remote address as a ``(ip, port)`` named tuple or an absolute ``path`` in case of UNIX sockets. When the remote endpoint is not connected you’ll get an empty tuple (AF_INET*) or ``""`` (AF_UNIX). For UNIX sockets see notes below."""
    status: str = ""
    """represents the status of a TCP connection. The return value is one of the ``psutil.CONN_*`` constants (a string). For UDP and UNIX sockets this is always going to be psutil.CONN_NONE."""
    pid: Optional[int]
    """the PID of the process which opened the socket, if retrievable, else ``None``. On some platforms (e.g. Linux) the availability of this field changes depending on process privileges (root is needed)."""


class MSANetworkAdapter(SQLModel):
    """Pydantic Network Adapter Info Model.
    """
    family: Optional[int]
    """the address family, either AF_INET or AF_INET6 or psutil.AF_LINK, which refers to a MAC address."""
    address: Optional[str]
    """the primary NIC address (always set)."""
    netmask: Optional[str]
    """the netmask address (may be None)."""
    broadcast: Optional[str]
    """the broadcast address (may be None)."""
    ptp: Optional[int]
    """stands for “point to point”; it’s the destination address on a point to point interface (typically a VPN). broadcast and ptp are mutually exclusive. May be None."""


class MSANetworkAdapters(SQLModel):
    """Pydantic Network Adapters List Model."""
    name: str = ""
    adapters: List[MSANetworkAdapter] = []


class MSANetworkStat(SQLModel):
    """Pydantic Network Stats Info Model."""
    isup: Optional[bool]
    """a bool indicating whether the NIC is up and running (meaning ethernet cable or Wi-Fi is connected)."""
    duplex: Optional[int]
    """the duplex communication type; it can be either NIC_DUPLEX_FULL, NIC_DUPLEX_HALF or NIC_DUPLEX_UNKNOWN."""
    speed: Optional[int]
    """the NIC speed expressed in mega bits (MB), if it can’t be determined (e.g. ‘localhost’) it will be set to 0."""
    mtu: Optional[int]
    """NIC’s maximum transmission unit expressed in bytes."""


class MSANetworkStats(SQLModel):
    """Pydantic Network Stats List Info Model."""
    name: str = ""
    adapters: List[MSANetworkStat] = []


class MSATemperature(SQLModel):
    """Pydantic Temperature Info Model."""
    label: Optional[str]
    current: Optional[float]
    high: Optional[float]
    critical: Optional[float]


class MSATemperatures(SQLModel):
    """Pydantic Temperatures List Model."""
    device: str = ""
    temps: List[MSATemperature] = []


class MSACPUFrequency(SQLModel):
    """Pydantic CPU Frequency Info Model."""
    current: Optional[float]
    min: Optional[int]
    max: Optional[int]


class MSACPUTimes(SQLModel):
    """Pydantic CPU Timings Info Model."""
    user: Optional[float]
    """time spent by normal processes executing in user mode; on Linux this also includes guest time"""
    nice: Optional[int]
    """(UNIX): time spent by niced (prioritized) processes executing in user mode; on Linux this also includes guest_nice time"""
    system: Optional[float]
    """time spent by processes executing in kernel mode"""
    idle: Optional[float]
    """time spent doing nothing"""
    iowait: Optional[float]
    """(Linux): time spent waiting for I/O to complete. This is not accounted in idle time counter."""
    irq: Optional[int]
    """(Linux, BSD): time spent for servicing hardware interrupts"""
    softirq: Optional[float]
    """(Linux): time spent for servicing software interrupts"""
    steal: Optional[int]
    """(Linux 2.6.11+): time spent by other operating systems running in a virtualized environment"""
    guest: Optional[float]
    """(Linux 2.6.24+): time spent running a virtual CPU for guest operating systems under the control of the Linux kernel"""
    guest_nice: Optional[int]
    """(Linux 3.2.0+): time spent running a niced guest (virtual CPU for guest operating systems under the control of the Linux kernel)"""


class MSACPUStats(SQLModel):
    """Pydantic CPU Stats Info Model."""
    ctx_switches: Optional[int]
    """number of context switches (voluntary + involuntary) since boot."""
    interrupts: Optional[int]
    """number of interrupts since boot."""
    soft_interrupts: Optional[int]
    """number of software interrupts since boot. Always set to 0 on Windows and SunOS."""
    syscalls: Optional[int]
    """number of system calls since boot. Always set to 0 on Linux."""


class MSAMemoryUsage(SQLModel):
    """Pydantic Memory Usage Info Model."""
    total: Optional[float]
    """total physical memory (exclusive swap)."""
    available: Optional[float]
    """the memory that can be given instantly to processes without the system going into swap. This is calculated by summing different memory values depending on the platform and it is supposed to be used to monitor actual memory usage in a cross platform fashion."""
    used: Optional[float]
    """memory used, calculated differently depending on the platform and designed for informational purposes only. total - free does not necessarily match used."""
    free: Optional[float]
    """memory not being used at all (zeroed) that is readily available; note that this doesn’t reflect the actual memory available (use available instead). total - used does not necessarily match free."""
    percent: Optional[float]
    """the percentage usage calculated as (total - available) / total * 100"""
    buffers: Optional[float]
    """(Linux, BSD): cache for things like file system metadata."""
    cached: Optional[float]
    """(Linux, BSD): cache for various things."""
    active: Optional[float]
    """(UNIX): memory currently in use or very recently used, and so it is in RAM."""
    inactive: Optional[float]
    """(UNIX): memory that is marked as not used."""


class MSASwap(SQLModel):
    """Pydantic Swapfile Info Model."""
    total: Optional[float]
    used: Optional[float]
    free: Optional[float]
    percent: Optional[float]
    """the percentage usage calculated as (total - available) / total * 100"""


class MSASystemInfo(SQLModel):
    """Pydantic System Info Model."""
    OS_Name: str = ""
    Node_Name: str = ""
    Host_Name: str = ""
    OS_Release: str = ""
    OS_Version: str = ""
    HW_Identifier: str = ""
    IP_Address: str = ""
    MAC_Address: str = ""
    CPU_Physical: Optional[int]
    """Amount of physical CPU's"""
    CPU_Logical: Optional[int]
    """Amount of logical (each physical core doing 2 or more threads, hyperthreading) CPU's"""
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
    Network_Stats: Optional[List[MSANetworkStats]]
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
    """Service Status, running or stopped"""


class MSASystemGPUInfo(SQLModel):
    """Pydantic System GPU Info Model."""
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


def get_hostname() -> str:
    """Get socket.gethostname()

        Returns:
            hostname: str
    """
    hostname: str = (socket.gethostname())
    return hostname


def get_list_partitions() -> List:
    """Get psutil.disk_partitions()

        Returns:
            partitions_list: List = []
    """
    partitions_list = []
    partitions = psutil.disk_partitions()
    partitions_list = [partition[1] for partition in partitions]

    return partitions_list


def get_gpus() -> List[MSAGPUInfo]:
    """Get GPUtil.getGPUs()

        Returns:
            list_gpus: List[MSAGPUInfo] = []
    """
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
    """Get psutil.disk_usage(partition)

        Returns:
            ret: Dict = {"partition": list, "total": list, "used": list, "free": list, "percent": list}
    """
    lstotal = []
    lsused = []
    lsfree = []
    lspercent = []
    lspartition: List = [partition for partition in partitions]

    for partition in partitions:
        usage = psutil.disk_usage(partition)
        total, used, free, percent = usage

        lstotal.append(total // (2 ** 30))
        lsused.append(used // (2 ** 30))
        lsfree.append(free // (2 ** 30))
        lspercent.append(percent)

    ret: Dict = {"partition": lspartition, "total": lstotal, "used": lsused, "free": lsfree, "percent": lspercent}
    return ret


def get_map_disk_usage() -> Dict:
    """Get get_partition_usage(get_list_partitions())

        Returns:
            rdict: Dict
    """
    MapUsage: Dict = get_partition_usage(get_list_partitions())
    disk = MapUsage["partition"]
    total = MapUsage["total"]
    used = MapUsage["used"]
    free = MapUsage["free"]
    percent = MapUsage["percent"]
    rdict = dict(zip(disk, zip(total, used, free, percent)))
    return rdict


def get_memory_usage() -> MSAMemoryUsage:
    """Get psutil.virtual_memory()

        Returns:
            mu: MSAMemoryUsage
    """
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
    """Get psutil.cpu_freq()

        Returns:
            cpf: MSACPUFrequency
    """
    cpf: MSACPUFrequency = MSACPUFrequency()
    cpf.current, cpf.min, cpf.max = psutil.cpu_freq()
    return cpf


def get_cpu_times() -> MSACPUTimes:
    """Get psutil.cpu_times()

        Returns:
            cti: MSACPUTimes
    """
    cti: MSACPUTimes = MSACPUTimes()
    cti.user, cti.nice, cti.system, cti.idle, cti.iowait, cti.irq, cti.softirq, \
    cti.steal, cti.guest, cti.guest_nice = psutil.cpu_times()
    return cti


def get_cpu_stats() -> MSACPUStats:
    """Get psutil.cpu_times()

        Returns:
            cst: MSACPUStats
    """
    cst: MSACPUStats = MSACPUStats()
    cst.ctx_switches, cst.interrupts, cst.soft_interrupts, cst.syscalls = psutil.cpu_stats()
    return cst


def get_disk_io() -> MSADiskIO:
    """Get psutil.disk_io_counters()

        Returns:
            dio: MSADiskIO
    """
    dio: MSADiskIO = MSADiskIO()
    dio.read_count, dio.write_count, dio.read_bytes, dio.write_bytes, dio.read_time, dio.write_time, \
    dio.read_merged_count, dio.write_merged_count, dio.busy_time = psutil.disk_io_counters()
    return dio


def get_network_io() -> MSANetworkIO:
    """Get psutil.net_io_counters()

        Returns:
            nio: MSANetworkIO
    """
    nio: MSANetworkIO = MSANetworkIO()
    nio.bytes_sent, nio.bytes_recv, nio.packets_sent, nio.packets_recv, nio.errin, \
    nio.errout, nio.dropin, nio.dropout = psutil.net_io_counters()
    return nio


def get_network_adapters() -> List[MSANetworkAdapters]:
    """Get psutil.net_if_addrs()

        Returns:
            ret: List[MSANetworkAdapters] = []
    """
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
    """Get psutil.sensors_temperatures()

        Returns:
            ret: List[MSATemperatures] = []
    """
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


def get_network_stats() -> List[MSANetworkStats]:
    """Get psutil.net_if_stats()

        Returns:
            ret: List[MSANetworkStats] = []
    """
    ret: List[MSANetworkStats] = []
    net_stats: Dict = psutil.net_if_stats()
    for key, entry in net_stats.items():
        ns: MSANetworkStats = MSANetworkStats()
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
    """Get psutil.net_connections()

        Returns:
            rlist: List[MSANetworkConnection] = []
    """
    rlist: List[MSANetworkConnection] = []
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
    """Get psutil.swap_memory()

        Returns:
            sw: MSASwap
    """
    swap = psutil.swap_memory()
    sw: MSASwap = MSASwap()
    sw.total = swap.total / 1024 / 1024
    sw.used = swap.used / 1024 / 1024
    sw.free = swap.free / 1024 / 1024
    sw.percent = swap.percent
    return sw


def get_load_average() -> tuple[float, float, float]:
    """Returns the CPU load average in tuple[1min, 5min, 15min].

    Returns:
        1min: total usage
        5min: largest process usage
        15min: name of the largest process

    """
    return [x / psutil.cpu_count() * 100 for x in psutil.getloadavg()]


def get_cpu_usage(user: str = None, ignore_self: bool = False) -> tuple[int, int, str]:
    """Returns the total CPU usage for all available cores.

        Args:
            user: If given, returns only the total CPU usage of all processes for the given user.
            ignore_self: If ``True`` the process that runs this script will be ignored.

        Returns:
            total: total usage
            largest_process: largest process usage
            largest_process_name: name of the largest process

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
    """Get MSASystemInfo
    Returns:
        system_info: Pydantic System Info Model.

    """
    system_info: MSASystemInfo = MSASystemInfo()
    try:
        system_info.OS_Name = os.uname().sysname
        system_info.Node_Name = os.uname().nodename
        system_info.Host_Name = get_hostname()
        system_info.OS_Release = os.uname().release
        system_info.OS_Version = os.uname().version
        system_info.HW_Identifier = os.uname().machine
        system_info.CPU_Physical = psutil.cpu_count(logical=False)
        system_info.CPU_Logical = os.cpu_count()
        system_info.Memory_Physical = str(round(psutil.virtual_memory().total / 1024000000., 2)) + " GB"
        system_info.Memory_Available = str(round(psutil.virtual_memory().available / 1024000000., 2)) + " GB"
        system_info.System_Boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        system_info.Service_Start = datetime.datetime.fromtimestamp(psutil.Process().create_time()).strftime(
            "%Y-%m-%d %H:%M:%S")
        system_info.Runtime_Exe = psutil.Process().exe()
        system_info.Runtime_Cmd = psutil.Process().cmdline()
        system_info.PID = psutil.Process().pid
        system_info.CPU_Current = psutil.Process().cpu_num()
        system_info.Disk_IO = get_disk_io()
        system_info.Network_IO = get_network_io()
        system_info.CPU_Times = get_cpu_times()
        system_info.CPU_Stats = get_cpu_stats()
        system_info.CPU_Frequency = get_cpu_freq()
        system_info.CPU_Affinity = len(psutil.Process().cpu_affinity())
        system_info.Memory_Usage = get_memory_usage()
        system_info.CPU_LoadAvg = get_load_average()
        system_info.CPU_Usage_Total, system_info.CPU_Usage_Process, system_info.CPU_Usage_Name = get_cpu_usage()
        system_info.Runtime_Status = psutil.Process().status()
        system_info.Network_Adapters = get_network_adapters()
        system_info.Temperatures = get_temperatures()
        system_info.Network_Connections = get_network_connections()
        system_info.Swap = get_swap()
        system_info.Network_Stats = get_network_stats()
        system_info.IP_Address = socket.gethostbyname(socket.gethostname())
        system_info.MAC_Address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System Information:")

    return system_info


def get_sysgpuinfo() -> MSASystemGPUInfo:
    """Get MSASystemGPUInfo
    Returns:
        system_gpu_info: Pydantic System GPU Info Model.
    """
    system_gpu_info: MSASystemGPUInfo = MSASystemGPUInfo()
    try:
        system_gpu_info.OS_Name = os.uname().sysname
        system_gpu_info.Node_Name = os.uname().nodename
        system_gpu_info.Host_Name = get_hostname()
        system_gpu_info.OS_Release = os.uname().release
        system_gpu_info.OS_Version = os.uname().version
        system_gpu_info.HW_Identifier = os.uname().machine
        system_gpu_info.CPU_Physical = psutil.cpu_count(logical=False)
        system_gpu_info.CPU_Logical = os.cpu_count()
        system_gpu_info.Memory_Physical = str(round(psutil.virtual_memory().total / 1024000000., 2)) + " GB"
        system_gpu_info.Memory_Available = str(round(psutil.virtual_memory().available / 1024000000., 2)) + " GB"
        system_gpu_info.System_Boot = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        system_gpu_info.Service_Start = datetime.datetime.fromtimestamp(psutil.Process().create_time()).strftime(
            "%Y-%m-%d %H:%M:%S")
        system_gpu_info.Runtime_Exe = psutil.Process().exe()
        system_gpu_info.Runtime_Cmd = psutil.Process().cmdline()
        system_gpu_info.Runtime_Status = psutil.Process().status()
        system_gpu_info.PID = psutil.Process().pid
        system_gpu_info.GPUs = get_gpus()
        system_gpu_info.IP_Address = socket.gethostbyname(socket.gethostname())
        system_gpu_info.MAC_Address = ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    except Exception as e:
        getMSABaseExceptionHandler().handle(e, "Error: Get System GPU Information:")

    return system_gpu_info
