#


## MSAProfilerMiddleware
```python 
MSAProfilerMiddleware(
   app: ASGIApp, *, msa_app: Optional[Router] = None,
   profiler_interval: float = 0.0001, profiler_output_type: str = 'html',
   track_each_request: bool = True, **profiler_kwargs
)
```




**Methods:**


### .get_profiler_result
```python
.get_profiler_result()
```

