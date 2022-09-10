#



## `MSARouterMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L17"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python

```




**Methods:**



### `.get_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L25"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_router()
```



### `.error_no_router_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L34"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.error_no_router_permission(
   request: Request
)
```


----



## `MSABaseCrud`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L38"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSABaseCrud(
   schema_model: Type[BaseModel], router: APIRouter = None
)
```




**Methods:**



### `.router_prefix`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L60"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_prefix()
```



### `.schema_name_prefix`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L64"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.schema_name_prefix()
```



### `.register_crud`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L67"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_crud(
   schema_list: Type[BaseModel] = None, schema_filter: Type[BaseModel] = None,
   schema_create: Type[BaseModel] = None, schema_read: Type[BaseModel] = None,
   schema_update: Type[BaseModel] = None, list_max_per_page: int = None,
   depends_list: List[Depends] = None, depends_read: List[Depends] = None,
   depends_create: List[Depends] = None, depends_update: List[Depends] = None,
   depends_delete: List[Depends] = None
)
```



### `.route_list`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L158"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_list()
```



### `.route_read`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L162"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_read()
```



### `.route_create`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L166"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_create()
```



### `.route_update`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L170"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_update()
```



### `.route_delete`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L174"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_delete()
```



### `.has_list_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L177"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_list_permission(
   request: Request, paginator: Optional[MSACRUDPaginator],
   filters: Optional[BaseModel], **kwargs
)
```



### `.has_create_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L186"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_create_permission(
   request: Request, obj: Optional[BaseModel], **kwargs
)
```



### `.has_read_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L194"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_read_permission(
   request: Request, item_id: Optional[List[str]], **kwargs
)
```



### `.has_update_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L202"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_update_permission(
   request: Request, item_id: Optional[List[str]], obj: Optional[BaseModel],
   **kwargs
)
```



### `.has_delete_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L211"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_delete_permission(
   request: Request, item_id: Optional[List[str]], **kwargs
)
```



### `.error_data_handle`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L219"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.error_data_handle(
   request: Request
)
```



### `.error_execute_sql`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/base.py/#L222"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.error_execute_sql(
   request: Request, error: Exception
)
```

