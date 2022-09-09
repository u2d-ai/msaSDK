#


## UserLoginFormAdmin
```python 
UserLoginFormAdmin()
```




**Methods:**


### .handle
```python
.handle(
   request: Request, data: BaseModel, **kwargs
)
```


### .route_submit
```python
.route_submit()
```


### .get_form
```python
.get_form(
   request: Request
)
```


### .get_page
```python
.get_page(
   request: Request
)
```


### .route_page
```python
.route_page()
```


### .has_page_permission
```python
.has_page_permission(
   request: Request
)
```


----


## UserRegFormAdmin
```python 
UserRegFormAdmin()
```




**Methods:**


### .handle
```python
.handle(
   request: Request, data: BaseModel, **kwargs
)
```


### .route_submit
```python
.route_submit()
```


### .get_form
```python
.get_form(
   request: Request
)
```


### .get_page
```python
.get_page(
   request: Request
)
```


### .has_page_permission
```python
.has_page_permission(
   request: Request
)
```


----


## UserInfoFormAdmin
```python 
UserInfoFormAdmin()
```




**Methods:**


### .get_init_data
```python
.get_init_data(
   request: Request, **kwargs
)
```


### .get_form
```python
.get_form(
   request: Request
)
```


### .handle
```python
.handle(
   request: Request, data: BaseModel, **kwargs
)
```


### .has_page_permission
```python
.has_page_permission(
   request: Request
)
```


----


## UserAdmin
```python 
UserAdmin()
```




**Methods:**


### .on_create_pre
```python
.on_create_pre(
   request: Request, obj, **kwargs
)
```


### .on_update_pre
```python
.on_update_pre(
   request: Request, obj, item_id: List[int], **kwargs
)
```


----


## RoleAdmin
```python 
RoleAdmin()
```



----


## GroupAdmin
```python 
GroupAdmin()
```



----


## PermissionAdmin
```python 
PermissionAdmin()
```



----


### attach_page_head
```python
.attach_page_head(
   page: Page
)
```

