#



## `MSATimerStatus`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L68"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSATimerStatus()
```


---
**MSATimerStatus** Pydantic Response Class

----



## `MSASchedulerStatus`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L77"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSASchedulerStatus()
```


---
**MSASchedulerStatus** Pydantic Response Class

----



## `MSAServiceStatus`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L86"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAServiceStatus()
```


---
**MSAServiceStatus** Pydantic Response Class

----



## `MSAOpenAPIInfo`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L95"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAOpenAPIInfo()
```


---
**MSAOpenAPIInfo** Pydantic Response Class

----



## `MSAApp`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L135"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAApp(
   settings: MSAServiceDefinition, timers: MSATimers = None,
   sql_models: List[SQLModel] = None, auto_mount_site: bool = True, *args, **kwargs
)
```


---
Creates an application MSA SDK instance.


**Note**

Do not include the `self` parameter in the ``Args`` section.


**Args**

* **settings**  : MSAServiceDefinition (Must be provided), instance of a service definition with all settings
* **timers**  : MSATimers instance Default None, provide a MSATimers instance and it will start the scheduler internaly
* **sql_models**  : List of SQLModel Default None, provide list of your SQLModel Classes and the instance can create CRUD API and if site is enabled also UI for CRUD
* **auto_mount_site**  : Default True, if site is enabled in settings and this is true, mounts the site in internal startup event.
* **debug**  : Boolean indicating if debug tracebacks should be returned on errors.
* **routes**  : A list of routes to serve incoming HTTP and WebSocket requests.
* **middleware**  : A list of middleware to run for every request. A starlette application will always automatically include two middleware classes. `ServerErrorMiddleware` is added as the very outermost middleware, to handle any uncaught errors occurring anywhere in the entire stack. `ExceptionMiddleware` is added as the very innermost middleware, to deal with handled exception cases occurring in the routing or endpoints.
* **exception_handlers**  : A mapping of either integer status codes, or exception class types onto callables which handle the exceptions. Exception handler callables should be of the form `handler(request, exc) -> response` and may be be either standard functions, or async functions.
* **on_startup**  : A list of callables to run on application startup. Startup handler callables do not take any arguments, and may be be either standard functions, or async functions.
* **on_shutdown**  : A list of callables to run on application shutdown. Shutdown handler callables do not take any arguments, and may be be either standard functions, or async functions.


**Returns**

* **MSAApp**  : MSAApp Instance.


**Attributes**

* **msg** (str) : Human readable string describing the exception.
* **code** (int) : Exception error code.


**Raises**

* **AttributeError**  : The ``Raises`` section is a list of all exceptions
    that are relevant to the interface.
* **ValueError**  : If `param2` is equal to `param1`.


**Yields**

* **int**  : The next number in the range of 0 to `n` - 1.


**Examples**

Examples should be written in doctest format, and should illustrate how
to use the function.

>>> print([i for i in example_generator(4)])
[0, 1, 2, 3]


**Methods:**



### `.startup_event`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L418"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.startup_event()
```

---
:return:
:rtype:


### `.mount_site`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L461"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.mount_site()
```



### `.shutdown_event`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L468"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.shutdown_event()
```



### `.get_healthcheck`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L509"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_healthcheck(
   request: Request
)
```

---
Get Healthcheck Status


### `.get_scheduler_status`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L525"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_scheduler_status(
   request: Request
)
```

---
Get Service Status Info


### `.get_services_status`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L550"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_services_status(
   request: Request
)
```

---
Get Service Status Info


### `.get_services_definition`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L568"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_services_definition(
   request: Request
)
```

---
Get Service Definition Info


### `.get_services_settings`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L575"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_services_settings(
   request: Request
)
```

---
Get Service OpenAPI Schema


### `.get_services_openapi_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L596"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_services_openapi_schema(
   request: Request
)
```

---
Get Service OpenAPI Schema


### `.get_services_openapi_info`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L617"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_services_openapi_info(
   request: Request
)
```

---
Get Service OpenAPI Info


### `.validation_exception_handler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L634"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.validation_exception_handler(
   request: Request, exc: RequestValidationError
)
```



### `.msa_exception_handler_disabled`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L641"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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


### `.msa_exception_handler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L664"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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


### `.index_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L690"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.index_page(
   request: Request
)
```

---
Get Service Index.html Page


### `.testpage`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L700"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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


### `.monitor`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L712"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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


### `.profiler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L725"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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


### `.monitor_inline`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L736"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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



## getSecretKey
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L105"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getSecretKey()
```

---
Get Secret Key for Token creation from OS Environment Variable **SECRET_KEY_TOKEN**
:return: key as str

----



## getSecretKeySessions
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L115"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getSecretKeySessions()
```

---
Get Secret Key for Session Middleware from OS Environment Variable **SECRET_KEY_SESSIONS**
:return: key as str

----



## getSecretKeyCSRF
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/service.py/#L125"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.getSecretKeyCSRF()
```

---
Get Secret Key for CSRF Middleware from OS Environment Variable **SECRET_KEY_CSRF**
:return: key as str
