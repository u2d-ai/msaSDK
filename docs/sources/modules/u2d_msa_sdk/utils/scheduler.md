#



## `MSATimerEnum`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L16"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSATimerEnum()
```



----



## `MSATimers`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L30"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python

```


---
Class to create dictionary of timers for use in MSAScheduler.


**Methods:**



### `.create_timer`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L58"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.create_timer(
   T_mode: MSATimerEnum, func: typing.Callable, mark_HH_MM = None
)
```


----



## `MSAScheduler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L113"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAScheduler(
   jobs, local_time_zone = 'UTC', poll_millis = 1000, debug = False,
   parent_logger = None
)
```




**Methods:**



### `.stop_timers`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L143"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.stop_timers()
```



### `.run_timers`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L148"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.run_timers(
   poll_adjuster = 0.99, debug = False
)
```

---
runs timers as follows:
Step 1:  run every poll jobs
Step 2: load timer queues for next poll
Step 3: delay function which runs previous poll queues
poll_adjustor allows time for other timing

----



## get_time_stamp
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L264"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_time_stamp(
   local_time_zone = 'UTC', time_format = 'HMS'
)
```


----



## get_time
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/scheduler.py/#L272"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_time(
   local_time_zone = 'UTC'
)
```

