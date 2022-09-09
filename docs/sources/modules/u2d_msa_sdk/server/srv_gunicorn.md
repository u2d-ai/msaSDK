#


## InterceptHandler
```python 
InterceptHandler()
```




**Methods:**


### .emit
```python
.emit(
   record
)
```


----


## StubbedGunicornLogger
```python 
StubbedGunicornLogger(
   cfg, log_level: str = 'info'
)
```



----


## StandaloneApplication
```python 
StandaloneApplication(
   app: MSAApp, options = None
)
```




**Methods:**


### .load_config
```python
.load_config()
```


### .load
```python
.load()
```


----


## MSAServerGunicorn
```python 
MSAServerGunicorn(
   app: MSAApp, app_dir: str, host: str, port: int, reload: bool = False,
   log_level: str = 'info', workers: int = -1
)
```




**Methods:**


### .run
```python
.run()
```


----


### number_of_workers
```python
.number_of_workers()
```

