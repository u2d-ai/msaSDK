#



## `TokenStoreModel`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/backends/db.py/#L13"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
TokenStoreModel()
```



----



## `DbTokenStore`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/backends/db.py/#L19"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
DbTokenStore(
   db: Union[AsyncDatabase, Database], expire_seconds: Optional[int] = 60*60*24*3,
   TokenDataSchema: _TokenDataSchemaT = None
)
```




**Methods:**



### `.read_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/backends/db.py/#L30"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.read_token(
   token: str
)
```



### `.write_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/backends/db.py/#L41"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.write_token(
   token_data: Union[_TokenDataSchemaT, dict]
)
```



### `.destroy_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/backends/db.py/#L48"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.destroy_token(
   token: str
)
```

