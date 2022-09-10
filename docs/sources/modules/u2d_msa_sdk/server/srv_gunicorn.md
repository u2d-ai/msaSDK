#



## `InterceptHandler`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L29"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
InterceptHandler()
```




**Methods:**



### `.emit`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L30"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.emit(
   record
)
```


----



## `StubbedGunicornLogger`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L46"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
StubbedGunicornLogger(
   cfg, log_level: str = 'info'
)
```



----



## `StandaloneApplication`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L60"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
StandaloneApplication(
   app: MSAApp, options = None
)
```




**Methods:**



### `.load_config`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L66"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.load_config()
```



### `.load`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L72"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.load()
```


----



## `MSAServerGunicorn`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L76"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAServerGunicorn(
   app: MSAApp, app_dir: str, host: str, port: int, reload: bool = False,
   log_level: str = 'info', workers: int = -1
)
```




**Methods:**



### `.run`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L96"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.run()
```


----



## number_of_workers
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/server/srv_gunicorn.py/#L22"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.number_of_workers()
```

