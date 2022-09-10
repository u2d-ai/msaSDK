#



## `MSASQLModelSelector`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L45"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSASQLModelSelector(
   model: Type[SQLModel] = None, fields: List[SQLModelListField] = None
)
```




**Methods:**



### `.get_select`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L75"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_select(
   request: Request
)
```



### `._select_maker`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L89"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
._select_maker()
```



### `.get_link_clause`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L102"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_link_clause(
   request: Request, link_model: str = None, link_item_id: Union[int,
   str] = Query(None, title = 'pk', example = '1, 2, 3',
   description = 'LinkModelPrimarykeyorlistofprimarykeys')
)
```



### `._parser_query_value`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L130"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
._parser_query_value(
   value: Any, operator: str = '__eq__', python_type_parse: Callable = str
)
```



### `.calc_filter_clause`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L154"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.calc_filter_clause(
   data: Dict[str, Any]
)
```


----



## `MSASQLModelCrud`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L165"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSASQLModelCrud(
   model: Type[SQLModel], engine: Union[Engine, AsyncEngine],
   fields: List[SQLModelListField] = None, router: APIRouter = None
)
```




**Methods:**



### `.schema_name_prefix`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L277"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.schema_name_prefix()
```



### `.on_create_pre`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L282"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.on_create_pre(
   request: Request, obj: BaseModel, **kwargs
)
```



### `.on_update_pre`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L288"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.on_update_pre(
   request: Request, obj: BaseModel, item_id: Union[List[str], List[int]],
   **kwargs
)
```



### `.on_filter_pre`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L300"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.on_filter_pre(
   request: Request, obj: BaseModel, **kwargs
)
```



### `.route_list`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L304"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_list()
```



### `.route_create`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L338"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_create()
```



### `.route_read`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L372"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_read()
```



### `.route_update`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L388"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_update()
```



### `.route_delete`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/_sqlmodel.py/#L408"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_delete()
```

