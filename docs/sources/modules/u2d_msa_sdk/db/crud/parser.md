#



## `MSASQLModelFieldParser`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L22"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSASQLModelFieldParser(
   default_model: Type[SQLModel]
)
```




**Methods:**



### `.get_modelfield`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L29"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_modelfield(
   field: Union[ModelField, SQLModelField], deepcopy: bool = False
)
```

---
pydantic ModelField


### `.get_column`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L51"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_column(
   field: SQLModelField
)
```

---
sqlalchemy Column


### `.get_alias`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L59"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_alias(
   field: Union[Column, SQLModelField, Label]
)
```



### `.get_name`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L74"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_name(
   field: InstrumentedAttribute
)
```



### `.get_row_keys`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L79"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_row_keys(
   row: Row
)
```

---
sqlalchemy row keys


### `.get_select_keys`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L83"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_select_keys(
   stmt: Select
)
```

---
sqlalchemy select keys


### `.conv_row_to_dict`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L87"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.conv_row_to_dict(
   rows: Union[Row, List[Row]]
)
```

---
sqlalchemy row to dict


### `.get_sqlmodel_insfield`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L99"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_sqlmodel_insfield(
   model: Type[SQLModel]
)
```



### `.get_insfield`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L103"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_insfield(
   field: SQLModelField
)
```



### `.filter_insfield`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L111"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.filter_insfield(
   fields: Iterable[Union[SQLModelListField, Any]], save_class: Tuple[type] = None
)
```


----



## get_python_type_parse
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/db/crud/parser.py/#L126"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_python_type_parse(
   field: Union[InstrumentedAttribute, Column]
)
```

