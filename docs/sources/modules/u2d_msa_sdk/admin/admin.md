#


## LinkModelForm
```python 
LinkModelForm(
   pk_admin: 'BaseModelAdmin', display_admin: 'ModelAdmin',
   link_model: Union[SQLModel, Table], link_col: Column, item_col: Column
)
```




**Methods:**


### .bind_model_admin
```python
.bind_model_admin(
   cls, pk_admin: 'BaseModelAdmin', insfield: InstrumentedAttribute
)
```


### .route_delete
```python
.route_delete()
```


### .route_create
```python
.route_create()
```


### .get_form_item
```python
.get_form_item(
   request: Request
)
```


### .register_router
```python
.register_router()
```


----


## BaseModelAdmin
```python 
BaseModelAdmin(
   app: 'AdminApp', model = None
)
```




**Methods:**


### .router_path
```python
.router_path()
```


### .get_link_model_forms
```python
.get_link_model_forms()
```


### .get_list_display
```python
.get_list_display(
   request: Request
)
```


### .get_list_filter
```python
.get_list_filter(
   request: Request
)
```


### .get_list_column
```python
.get_list_column(
   request: Request, modelfield: ModelField
)
```


### .get_list_columns
```python
.get_list_columns(
   request: Request
)
```


### .get_list_table_api
```python
.get_list_table_api(
   request: Request
)
```


### .get_list_table
```python
.get_list_table(
   request: Request
)
```


### .get_form_item_on_foreign_key
```python
.get_form_item_on_foreign_key(
   request: Request, modelfield: ModelField, is_filter: bool = False
)
```


### .get_form_item
```python
.get_form_item(
   request: Request, modelfield: ModelField, action: MSACRUDEnum
)
```


### .get_list_filter_form
```python
.get_list_filter_form(
   request: Request
)
```


### .get_create_form
```python
.get_create_form(
   request: Request, bulk: bool = False
)
```


### .get_update_form
```python
.get_update_form(
   request: Request, bulk: bool = False
)
```


### .get_create_action
```python
.get_create_action(
   request: Request, bulk: bool = False
)
```


### .get_update_action
```python
.get_update_action(
   request: Request, bulk: bool = False
)
```


### .get_delete_action
```python
.get_delete_action(
   request: Request, bulk: bool = False
)
```


### .get_actions_on_header_toolbar
```python
.get_actions_on_header_toolbar(
   request: Request
)
```


### .get_actions_on_item
```python
.get_actions_on_item(
   request: Request
)
```


### .get_actions_on_bulk
```python
.get_actions_on_bulk(
   request: Request
)
```


----


## BaseAdmin
```python 
BaseAdmin(
   app: 'AdminApp'
)
```




**Methods:**


### .site
```python
.site()
```


### .unique_id
```python
.unique_id()
```


----


## PageSchemaAdmin
```python 
PageSchemaAdmin(
   app: 'AdminApp'
)
```




**Methods:**


### .has_page_permission
```python
.has_page_permission(
   request: Request
)
```


### .get_page_schema
```python
.get_page_schema()
```


### .get_group_schema
```python
.get_group_schema()
```


----


## LinkAdmin
```python 
LinkAdmin()
```




**Methods:**


### .get_page_schema
```python
.get_page_schema()
```


----


## IframeAdmin
```python 
IframeAdmin()
```




**Methods:**


### .get_page_schema
```python
.get_page_schema()
```


----


## RouterAdmin
```python 
RouterAdmin(
   app: 'AdminApp'
)
```




**Methods:**


### .register_router
```python
.register_router()
```


### .router_path
```python
.router_path()
```


----


## PageAdmin
```python 
PageAdmin(
   app: 'AdminApp'
)
```


---
msa_ui页面管理


**Methods:**


### .page_permission_depend
```python
.page_permission_depend(
   request: Request
)
```


### .error_no_page_permission
```python
.error_no_page_permission(
   request: Request
)
```


### .get_page
```python
.get_page(
   request: Request
)
```


### .get_page_schema
```python
.get_page_schema()
```


### .page_parser
```python
.page_parser(
   request: Request, page: Page
)
```


### .register_router
```python
.register_router()
```


### .route_page
```python
.route_page()
```


----


## TemplateAdmin
```python 
TemplateAdmin(
   app: 'AdminApp'
)
```


---
Jinja2渲染模板管理


**Methods:**


### .page_parser
```python
.page_parser(
   request: Request, page: Dict[str, Any]
)
```


### .get_page
```python
.get_page(
   request: Request
)
```


----


## BaseFormAdmin
```python 
BaseFormAdmin(
   app: 'AdminApp'
)
```




**Methods:**


### .get_page
```python
.get_page(
   request: Request
)
```


### .get_form_item
```python
.get_form_item(
   request: Request, modelfield: ModelField
)
```


### .get_form
```python
.get_form(
   request: Request
)
```


### .register_router
```python
.register_router()
```


----


## FormAdmin
```python 
FormAdmin()
```


---
表单管理


**Methods:**


### .route_submit
```python
.route_submit()
```


### .handle
```python
.handle(
   request: Request, data: BaseModel, **kwargs
)
```


### .get_init_data
```python
.get_init_data(
   request: Request, **kwargs
)
```


### .route_init
```python
.route_init()
```


----


## ModelFormAdmin
```python 
ModelFormAdmin(
   app: 'AdminApp'
)
```


---
todo Read and update a model resource 

----


## ModelAdmin
```python 
ModelAdmin(
   app: 'AdminApp', model = None
)
```


---
模型管理


**Methods:**


### .router_prefix
```python
.router_prefix()
```


### .register_router
```python
.register_router()
```


### .get_page
```python
.get_page(
   request: Request
)
```


### .has_list_permission
```python
.has_list_permission(
   request: Request, paginator: MSACRUDPaginator, filters: BaseModel = None,
   **kwargs
)
```


### .has_create_permission
```python
.has_create_permission(
   request: Request, data: BaseModel, **kwargs
)
```


### .has_read_permission
```python
.has_read_permission(
   request: Request, item_id: List[str], **kwargs
)
```


### .has_update_permission
```python
.has_update_permission(
   request: Request, item_id: List[str], data: BaseModel, **kwargs
)
```


### .has_delete_permission
```python
.has_delete_permission(
   request: Request, item_id: List[str], **kwargs
)
```


----


## BaseModelAction
```python 
BaseModelAction(
   admin: 'ModelAdmin'
)
```




**Methods:**


### .fetch_item_scalars
```python
.fetch_item_scalars(
   item_id: List[str]
)
```


### .register_router
```python
.register_router()
```


----


## ModelAction
```python 
ModelAction(
   admin: 'ModelAdmin'
)
```




**Methods:**


### .get_action
```python
.get_action(
   request: Request, **kwargs
)
```


### .handle
```python
.handle(
   request: Request, item_id: List[str], data: Optional[BaseModel], **kwargs
)
```


### .route_submit
```python
.route_submit()
```


----


## AdminGroup
```python 
AdminGroup(
   app: 'AdminApp'
)
```




**Methods:**


### .unique_id
```python
.unique_id()
```


### .append_child
```python
.append_child(
   child: _PageSchemaAdminT, group_schema: PageSchema = None
)
```


### .get_page_schema_children
```python
.get_page_schema_children(
   request: Request
)
```


### .get_page_schema_child
```python
.get_page_schema_child(
   unique_id: str
)
```


----


## AdminApp
```python 
AdminApp(
   app: 'AdminApp', msa_app: MSAApp
)
```


---
管理应用


**Methods:**


### .router_prefix
```python
.router_prefix()
```


### .get_admin_or_create
```python
.get_admin_or_create(
   admin_cls: Type[_BaseAdminT], register: bool = True
)
```


### .register_router
```python
.register_router()
```


### .register_admin
```python
.register_admin(
   *admin_cls: Type[_BaseAdminT]
)
```


### .unregister_admin
```python
.unregister_admin(
   *admin_cls: Type[BaseAdmin]
)
```


### .get_page_schema
```python
.get_page_schema()
```


### .get_page
```python
.get_page(
   request: Request
)
```


----


## BaseAdminSite
```python 
BaseAdminSite(
   msa_app: MSAApp
)
```




**Methods:**


### .router_path
```python
.router_path()
```


### .mount_app
```python
.mount_app(
   msa_app: MSAApp, name: str = 'admin'
)
```

