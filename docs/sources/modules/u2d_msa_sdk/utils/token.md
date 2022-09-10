#



## `MSATokenData`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/token.py/#L15"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSATokenData()
```



----



## `MSAToken`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/token.py/#L19"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSAToken(
   secret_key: str, algorithm: str = 'HS256'
)
```




**Methods:**



### `.create_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/token.py/#L28"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.create_token(
   data: dict, expire_minutes: int = 100
)
```



### `.verify_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/token.py/#L37"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.verify_token(
   token: str
)
```



### `.get_current_user`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/token.py/#L50"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_current_user(
   token: str = Depends(oauth2_scheme)
)
```

