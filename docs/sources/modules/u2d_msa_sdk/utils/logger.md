#


## InterceptHandler
```python 
InterceptHandler()
```


---
Default handler from examples in loguru documentaion.
See https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging


**Methods:**


### .emit
```python
.emit(
   record: logging.LogRecord
)
```


----


### format_record
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


### init_logging
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
