#


## MSAGPUInfo
```python 
MSAGPUInfo()
```



----


## MSADiskIO
```python 
MSADiskIO()
```



----


## MSANetworkIO
```python 
MSANetworkIO()
```



----


## MSANetworkConnection
```python 
MSANetworkConnection()
```



----


## MSANetworkAdapter
```python 
MSANetworkAdapter()
```



----


## MSANetworkAdapters
```python 
MSANetworkAdapters()
```



----


## MSANetworkStat
```python 
MSANetworkStat()
```



----


## NetworkStats
```python 
NetworkStats()
```



----


## MSATemperature
```python 
MSATemperature()
```



----


## MSATemperatures
```python 
MSATemperatures()
```



----


## MSACPUFrequency
```python 
MSACPUFrequency()
```



----


## MSACPUTimes
```python 
MSACPUTimes()
```



----


## MSACPUStats
```python 
MSACPUStats()
```



----


## MSAMemoryUsage
```python 
MSAMemoryUsage()
```



----


## MSASwap
```python 
MSASwap()
```



----


## MSASystemInfo
```python 
MSASystemInfo()
```



----


## MSASystemGPUInfo
```python 
MSASystemGPUInfo()
```



----


### get_hostname
```python
.get_hostname()
```


----


### get_list_partitions
```python
.get_list_partitions()
```


----


### get_gpus
```python
.get_gpus()
```


----


### get_partition_usage
```python
.get_partition_usage(
   partitions
)
```


----


### get_map_disk_usage
```python
.get_map_disk_usage()
```


----


### get_memory_usage
```python
.get_memory_usage()
```


----


### get_cpu_freq
```python
.get_cpu_freq()
```


----


### get_cpu_times
```python
.get_cpu_times()
```


----


### get_cpu_stats
```python
.get_cpu_stats()
```


----


### get_disk_io
```python
.get_disk_io()
```


----


### get_network_io
```python
.get_network_io()
```


----


### get_network_adapters
```python
.get_network_adapters()
```


----


### get_temperatures
```python
.get_temperatures()
```


----


### get_network_stats
```python
.get_network_stats()
```


----


### get_network_connections
```python
.get_network_connections()
```


----


### get_swap
```python
.get_swap()
```


----


### get_load_average
```python
.get_load_average()
```


----


### get_cpu_usage
```python
.get_cpu_usage(
   user = None, ignore_ = False
)
```

---
Returns the total CPU usage for all available cores.
:param user: If given, returns only the total CPU usage of all processes
  for the given user.
:param ignore_self: If ``True`` the process that runs this script will
  be ignored.

----


### get_sysinfo
```python
.get_sysinfo()
```

---
Get MSASystemInfo

----


### get_sysgpuinfo
```python
.get_sysgpuinfo()
```

---
Get MSASystemGPUInfo
