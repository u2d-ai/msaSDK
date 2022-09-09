#


## MSASQLModelSelector
```python 
MSASQLModelSelector(
   model: Type[SQLModel] = None, fields: List[SQLModelListField] = None
)
```




**Methods:**


### .get_select
```python
.get_select(
   request: Request
)
```


### ._select_maker
```python
._select_maker()
```


### .get_link_clause
```python
.get_link_clause(
   request: Request, link_model: str = None, link_item_id: Union[int,
   str] = Query(None, title = 'pk', example = '1, 2, 3',
   description = 'LinkModelPrimarykeyorlistofprimarykeys')
)
```


### ._parser_query_value
```python
._parser_query_value(
   value: Any, operator: str = '__eq__', python_type_parse: Callable = str
)
```


### .calc_filter_clause
```python
.calc_filter_clause(
   data: Dict[str, Any]
)
```


----


## MSASQLModelCrud
```python 
MSASQLModelCrud(
   model: Type[SQLModel], engine: Union[Engine, AsyncEngine],
   fields: List[SQLModelListField] = None, router: APIRouter = None
)
```




**Methods:**


### .schema_name_prefix
```python
.schema_name_prefix()
```


### .on_create_pre
```python
.on_create_pre(
   request: Request, obj: BaseModel, **kwargs
)
```


### .on_update_pre
```python
.on_update_pre(
   request: Request, obj: BaseModel, item_id: Union[List[str], List[int]],
   **kwargs
)
```


### .on_filter_pre
```python
.on_filter_pre(
   request: Request, obj: BaseModel, **kwargs
)
```


### .route_list
```python
.route_list()
```


### .route_create
```python
.route_create()
```


### .route_read
```python
.route_read()
```


### .route_update
```python
.route_update()
```


### .route_delete
```python
.route_delete()
```

