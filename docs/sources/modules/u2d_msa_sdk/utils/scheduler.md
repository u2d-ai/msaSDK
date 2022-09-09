#


## MSATimerEnum
```python 
MSATimerEnum()
```



----


## MSATimers
```python 

```


---
Class to create dictionary of timers for use in MSAScheduler.


**Methods:**


### .create_timer
```python
.create_timer(
   T_mode: MSATimerEnum, func: typing.Callable, mark_HH_MM = None
)
```


----


## MSAScheduler
```python 
MSAScheduler(
   jobs, local_time_zone = 'UTC', poll_millis = 1000, debug = False,
   parent_logger = None
)
```




**Methods:**


### .stop_timers
```python
.stop_timers()
```


### .run_timers
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


### get_time_stamp
```python
.get_time_stamp(
   local_time_zone = 'UTC', time_format = 'HMS'
)
```


----


### get_time
```python
.get_time(
   local_time_zone = 'UTC'
)
```

