#



## `MSAProfilerMiddleware`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/profiler.py/#L15"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAProfilerMiddleware(
   app: ASGIApp, *, msa_app: Optional[Router] = None,
   profiler_interval: float = 0.0001, profiler_output_type: str = 'html',
   track_each_request: bool = True, **profiler_kwargs
)
```




**Methods:**



### `.get_profiler_result`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/profiler.py/#L69"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_profiler_result()
```

