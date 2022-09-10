#



## `InterceptHandler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/logger.py/#L14"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
InterceptHandler()
```


---
Default handler from examples in loguru documentaion.
See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging


**Methods:**



### `.emit`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/logger.py/#L20"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.emit(
   record: logging.LogRecord
)
```


----



## format_record
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/logger.py/#L38"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.format_record(
   record: dict
)
```

---
Custom format for loguru loggers.
Uses pformat for log any data like request/response body during debug.
Works with logging if loguru handler it.

**Example**

* "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
* 2,
* [   {'age': 87, 'is_active': True, 'name': 'Nick'},
* 27, 'is_active': True, 'name': 'Alex'}]}]
>>> logger.bind(payload=).debug("users payload")

----



## init_logging
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/logger.py/#L62"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.init_logging()
```

---
Replaces logging handlers with a handler for using the custom handler.

WARNING!
if you call the init_logging in startup event function,
then the first logs before the application start will be in the old format
>>> app.add_event_handler("startup", init_logging)
stdout:
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [11528] using statreload
INFO:     Started server process [6036]
INFO:     Waiting for application startup.
2020-07-25 02:19:21.357 | INFO     | uvicorn.lifespan.on:startup:34 - Application startup complete.
