#


## MSATimerStatus
```python 
MSATimerStatus()
```


---
**MSATimerStatus** Pydantic Response Class

----


## MSASchedulerStatus
```python 
MSASchedulerStatus()
```


---
**MSASchedulerStatus** Pydantic Response Class

----


## MSAServiceStatus
```python 
MSAServiceStatus()
```


---
**MSAServiceStatus** Pydantic Response Class

----


## MSAOpenAPIInfo
```python 
MSAOpenAPIInfo()
```


---
**MSAOpenAPIInfo** Pydantic Response Class

----


## MSAApp
```python 
MSAApp(
   settings: MSAServiceDefinition, timers: MSATimers = None,
   sql_models: List[SQLModel] = None, auto_mount_site: bool = True, *args, **kwargs
)
```


---
Creates an application MSA SDK instance.

**Parameters:**

* **settings** - MSAServiceDefinition (Must be provided), instance of a service definition with all settings
* **timers** - MSATimers instance Default None, provide a MSATimers instance and it will start the scheduler internaly
* **sql_models** - List of SQLModel Default None, provide list of your SQLModel Classes and the instance can create CRUD API and if site is enabled also UI for CRUD
* **auto_mount_site** - Default True, if site is enabled in settings and this is true, mounts the site in internal startup event.

**Inherited Parameters: used as *args, **kwargs**

* **debug** - Boolean indicating if debug tracebacks should be returned on errors.
* **routes** - A list of routes to serve incoming HTTP and WebSocket requests.
* **middleware** - A list of middleware to run for every request. A starlette
application will always automatically include two middleware classes.
`ServerErrorMiddleware` is added as the very outermost middleware, to handle
any uncaught errors occurring anywhere in the entire stack.
`ExceptionMiddleware` is added as the very innermost middleware, to deal
with handled exception cases occurring in the routing or endpoints.
* **exception_handlers** - A mapping of either integer status codes,
or exception class types onto callables which handle the exceptions.
Exception handler callables should be of the form
`handler(request, exc) -> response` and may be be either standard functions, or
async functions.
* **on_startup** - A list of callables to run on application startup.
Startup handler callables do not take any arguments, and may be be either
standard functions, or async functions.
* **on_shutdown** - A list of callables to run on application shutdown.
Shutdown handler callables do not take any arguments, and may be be either
standard functions, or async functions.


**Methods:**


### .startup_event
```python
.startup_event()
```

---
:return:
:rtype:

### .mount_site
```python
.mount_site()
```


### .shutdown_event
```python
.shutdown_event()
```


### .get_healthcheck
```python
.get_healthcheck(
   request: Request
)
```

---
Get Healthcheck Status

### .get_scheduler_status
```python
.get_scheduler_status(
   request: Request
)
```

---
Get Service Status Info

### .get_services_status
```python
.get_services_status(
   request: Request
)
```

---
Get Service Status Info

### .get_services_definition
```python
.get_services_definition(
   request: Request
)
```

---
Get Service Definition Info

### .get_services_settings
```python
.get_services_settings(
   request: Request
)
```

---
Get Service OpenAPI Schema

### .get_services_openapi_schema
```python
.get_services_openapi_schema(
   request: Request
)
```

---
Get Service OpenAPI Schema

### .get_services_openapi_info
```python
.get_services_openapi_info(
   request: Request
)
```

---
Get Service OpenAPI Info

### .validation_exception_handler
```python
.validation_exception_handler(
   request: Request, exc: RequestValidationError
)
```


### .msa_exception_handler_disabled
```python
.msa_exception_handler_disabled(
   request: Request, exc: HTTPException
)
```

---
Handles all HTTPExceptions if Disabled with JSON Response.
:param request:
:type request:
:param exc:
:type exc:
:return:
:rtype:

### .msa_exception_handler
```python
.msa_exception_handler(
   request: Request, exc: HTTPException
)
```

---
Handles all HTTPExceptions if enabled with HTML Response or forward error if the code is in the exclude settings list.
:param request:
:type request:
:param exc:
:type exc:
:return:
:rtype:

### .index_page
```python
.index_page(
   request: Request
)
```

---
Get Service Index.html Page

### .testpage
```python
.testpage(
   request: Request
)
```

---
Simple Testpage to see if the Micro Service is up and running.
Only works if pages is enabled in MSAServiceDefinition
:param request:
:return:

### .monitor
```python
.monitor(
   request: Request
)
```

---
Simple Service Monitor Page.
Only works if pages is enabled in MSAServiceDefinition
:param request:
:return:

### .profiler
```python
.profiler(
   request: Request
)
```

---
Simple Profiler Page.
Only works if pages is enabled in MSAServiceDefinition
:param request:
:return:

### .monitor_inline
```python
.monitor_inline(
   request: Request
)
```

---
Simple Monitor Page as Inline without head and body tags.
Only works if pages is enabled in MSAServiceDefinition
:param request:
:return:

----


### getSecretKey
```python
.getSecretKey()
```

---
Get Secret Key for Token creation from OS Environment Variable **SECRET_KEY_TOKEN**
:return: key as str

----


### getSecretKeySessions
```python
.getSecretKeySessions()
```

---
Get Secret Key for Session Middleware from OS Environment Variable **SECRET_KEY_SESSIONS**
:return: key as str

----


### getSecretKeyCSRF
```python
.getSecretKeyCSRF()
```

---
Get Secret Key for CSRF Middleware from OS Environment Variable **SECRET_KEY_CSRF**
:return: key as str
