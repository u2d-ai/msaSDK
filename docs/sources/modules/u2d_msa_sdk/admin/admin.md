#



## `LinkModelForm`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L47"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
LinkModelForm(
   pk_admin: 'BaseModelAdmin', display_admin: 'ModelAdmin',
   link_model: Union[SQLModel, Table], link_col: Column, item_col: Column
)
```




**Methods:**



### `.bind_model_admin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L69"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.bind_model_admin(
   cls, pk_admin: 'BaseModelAdmin', insfield: InstrumentedAttribute
)
```



### `.route_delete`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L105"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_delete()
```



### `.route_create`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L129"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_create()
```



### `.get_form_item`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L156"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_form_item(
   request: Request
)
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L227"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```


----



## `BaseModelAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L247"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseModelAdmin(
   app: 'AdminApp', model = None
)
```




**Methods:**



### `.router_path`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L270"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_path()
```



### `.get_link_model_forms`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L273"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_link_model_forms()
```



### `.get_list_display`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L279"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_display(
   request: Request
)
```



### `.get_list_filter`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L282"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_filter(
   request: Request
)
```



### `.get_list_column`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L285"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_column(
   request: Request, modelfield: ModelField
)
```



### `.get_list_columns`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L298"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_columns(
   request: Request
)
```



### `.get_list_table_api`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L320"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_table_api(
   request: Request
)
```



### `.get_list_table`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L337"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_table(
   request: Request
)
```



### `.get_form_item_on_foreign_key`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L368"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_form_item_on_foreign_key(
   request: Request, modelfield: ModelField, is_filter: bool = False
)
```



### `.get_form_item`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L396"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_form_item(
   request: Request, modelfield: ModelField, action: MSACRUDEnum
)
```



### `.get_list_filter_form`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L409"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_list_filter_form(
   request: Request
)
```



### `.get_create_form`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L438"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_create_form(
   request: Request, bulk: bool = False
)
```



### `.get_update_form`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L465"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_update_form(
   request: Request, bulk: bool = False
)
```



### `.get_create_action`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L482"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_create_action(
   request: Request, bulk: bool = False
)
```



### `.get_update_action`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L507"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_update_action(
   request: Request, bulk: bool = False
)
```



### `.get_delete_action`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L535"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_delete_action(
   request: Request, bulk: bool = False
)
```



### `.get_actions_on_header_toolbar`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L549"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_actions_on_header_toolbar(
   request: Request
)
```



### `.get_actions_on_item`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L554"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_actions_on_item(
   request: Request
)
```



### `.get_actions_on_bulk`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L560"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_actions_on_bulk(
   request: Request
)
```


----



## `BaseAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L585"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseAdmin(
   app: 'AdminApp'
)
```




**Methods:**



### `.site`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L592"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.site()
```



### `.unique_id`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L596"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.unique_id()
```


----



## `PageSchemaAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L603"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
PageSchemaAdmin(
   app: 'AdminApp'
)
```




**Methods:**



### `.has_page_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L614"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_page_permission(
   request: Request
)
```



### `.get_page_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L617"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema()
```



### `.get_group_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L628"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_group_schema()
```


----



## `LinkAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L640"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
LinkAdmin()
```




**Methods:**



### `.get_page_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L643"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema()
```


----



## `IframeAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L650"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
IframeAdmin()
```




**Methods:**



### `.get_page_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L654"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema()
```


----



## `RouterAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L666"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
RouterAdmin(
   app: 'AdminApp'
)
```




**Methods:**



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L672"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```



### `.router_path`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L676"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_path()
```


----



## `PageAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L682"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
PageAdmin(
   app: 'AdminApp'
)
```


---
msa_ui页面管理


**Methods:**



### `.page_permission_depend`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L697"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.page_permission_depend(
   request: Request
)
```



### `.error_no_page_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L700"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.error_no_page_permission(
   request: Request
)
```



### `.get_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L709"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page(
   request: Request
)
```



### `.get_page_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L712"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema()
```



### `.page_parser`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L722"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.page_parser(
   request: Request, page: Page
)
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L739"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```



### `.route_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L761"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_page()
```


----



## `TemplateAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L768"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
TemplateAdmin(
   app: 'AdminApp'
)
```


---
Jinja2渲染模板管理


**Methods:**



### `.page_parser`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L780"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.page_parser(
   request: Request, page: Dict[str, Any]
)
```



### `.get_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L784"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page(
   request: Request
)
```


----



## `BaseFormAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L788"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseFormAdmin(
   app: 'AdminApp'
)
```




**Methods:**



### `.get_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L804"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page(
   request: Request
)
```



### `.get_form_item`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L809"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_form_item(
   request: Request, modelfield: ModelField
)
```



### `.get_form`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L816"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_form(
   request: Request
)
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L829"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```


----



## `FormAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L850"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
FormAdmin()
```


---
表单管理


**Methods:**



### `.route_submit`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L854"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_submit()
```



### `.handle`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L862"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.handle(
   request: Request, data: BaseModel, **kwargs
)
```



### `.get_init_data`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L865"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_init_data(
   request: Request, **kwargs
)
```



### `.route_init`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L869"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_init()
```


----



## `ModelFormAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L876"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ModelFormAdmin(
   app: 'AdminApp'
)
```


---
todo Read and update a model resource 

----



## `ModelAdmin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L884"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ModelAdmin(
   app: 'AdminApp', model = None
)
```


---
模型管理


**Methods:**



### `.router_prefix`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L894"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_prefix()
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L899"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```



### `.get_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L906"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page(
   request: Request
)
```



### `.has_list_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L911"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_list_permission(
   request: Request, paginator: MSACRUDPaginator, filters: BaseModel = None,
   **kwargs
)
```



### `.has_create_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L920"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_create_permission(
   request: Request, data: BaseModel, **kwargs
)
```



### `.has_read_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L928"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_read_permission(
   request: Request, item_id: List[str], **kwargs
)
```



### `.has_update_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L936"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_update_permission(
   request: Request, item_id: List[str], data: BaseModel, **kwargs
)
```



### `.has_delete_permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L945"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.has_delete_permission(
   request: Request, item_id: List[str], **kwargs
)
```


----



## `BaseModelAction`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L954"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseModelAction(
   admin: 'ModelAdmin'
)
```




**Methods:**



### `.fetch_item_scalars`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L962"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.fetch_item_scalars(
   item_id: List[str]
)
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L966"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```


----



## `ModelAction`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L970"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ModelAction(
   admin: 'ModelAdmin'
)
```




**Methods:**



### `.get_action`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L979"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_action(
   request: Request, **kwargs
)
```



### `.handle`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L995"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.handle(
   request: Request, item_id: List[str], data: Optional[BaseModel], **kwargs
)
```



### `.route_submit`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1005"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_submit()
```


----



## `AdminGroup`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1021"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
AdminGroup(
   app: 'AdminApp'
)
```




**Methods:**



### `.unique_id`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1028"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.unique_id()
```



### `.append_child`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1034"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.append_child(
   child: _PageSchemaAdminT, group_schema: PageSchema = None
)
```



### `.get_page_schema_children`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1050"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema_children(
   request: Request
)
```



### `.get_page_schema_child`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1068"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema_child(
   unique_id: str
)
```


----



## `AdminApp`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1082"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
AdminApp(
   app: 'AdminApp', msa_app: MSAApp
)
```


---
管理应用


**Methods:**



### `.router_prefix`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1118"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_prefix()
```



### `.get_admin_or_create`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1121"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_admin_or_create(
   admin_cls: Type[_BaseAdminT], register: bool = True
)
```



### `.register_router`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1146"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_router()
```



### `.register_admin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1167"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.register_admin(
   *admin_cls: Type[_BaseAdminT]
)
```



### `.unregister_admin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1171"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.unregister_admin(
   *admin_cls: Type[BaseAdmin]
)
```



### `.get_page_schema`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1174"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page_schema()
```



### `.get_page`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1179"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_page(
   request: Request
)
```


----



## `BaseAdminSite`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1213"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseAdminSite(
   msa_app: MSAApp
)
```




**Methods:**



### `.router_path`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1231"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_path()
```



### `.mount_app`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/admin.py/#L1234"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.mount_app(
   msa_app: MSAApp, name: str = 'admin'
)
```

