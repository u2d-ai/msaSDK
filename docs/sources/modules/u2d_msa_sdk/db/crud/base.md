#


## MSARouterMixin
```python 

```




**Methods:**


### .get_router
```python
.get_router()
```


### .error_no_router_permission
```python
.error_no_router_permission(
   request: Request
)
```


----


## MSABaseCrud
```python 
MSABaseCrud(
   schema_model: Type[BaseModel], router: APIRouter = None
)
```




**Methods:**


### .router_prefix
```python
.router_prefix()
```


### .schema_name_prefix
```python
.schema_name_prefix()
```


### .register_crud
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


### .route_list
```python
.route_list()
```


### .route_read
```python
.route_read()
```


### .route_create
```python
.route_create()
```


### .route_update
```python
.route_update()
```


### .route_delete
```python
.route_delete()
```


### .has_list_permission
```python
.has_list_permission(
   request: Request, paginator: Optional[MSACRUDPaginator],
   filters: Optional[BaseModel], **kwargs
)
```


### .has_create_permission
```python
.has_create_permission(
   request: Request, obj: Optional[BaseModel], **kwargs
)
```


### .has_read_permission
```python
.has_read_permission(
   request: Request, item_id: Optional[List[str]], **kwargs
)
```


### .has_update_permission
```python
.has_update_permission(
   request: Request, item_id: Optional[List[str]], obj: Optional[BaseModel],
   **kwargs
)
```


### .has_delete_permission
```python
.has_delete_permission(
   request: Request, item_id: Optional[List[str]], **kwargs
)
```


### .error_data_handle
```python
.error_data_handle(
   request: Request
)
```


### .error_execute_sql
```python
.error_execute_sql(
   request: Request, error: Exception
)
```

