#



## `AuthBackend`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L36"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
AuthBackend(
   auth: 'Auth', token_store: BaseTokenStore
)
```




**Methods:**



### `.get_user_token`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L43"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_user_token(
   request: Request
)
```



### `.authenticate`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L50"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.authenticate(
   request: Request
)
```



### `.attach_middleware`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L53"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.attach_middleware(
   app: FastAPI
)
```


----



## `Auth`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L57"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
Auth(
   db: Union[AsyncDatabase, Database], token_store: BaseTokenStore = None,
   user_model: Type[_UserModelT] = User,
   pwd_context: CryptContext = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
)
```




**Methods:**



### `.authenticate_user`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L75"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.authenticate_user(
   username: str, password: Union[str, SecretStr]
)
```



### `.get_current_user`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L85"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_current_user()
```



### `.requires`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L104"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.requires(
   roles: Union[str, Sequence[str]] = None, groups: Union[str, Sequence[str]] = None,
   permissions: Union[str, Sequence[str]] = None, status_code: int = 403,
   redirect: str = None, response: Union[bool, Response] = None
)
```



### `.create_role_user`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L228"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.create_role_user(
   role_key: str = 'admin'
)
```


----



## `AuthRouter`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L236"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
AuthRouter(
   auth: Auth = None
)
```




**Methods:**



### `.router_path`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L269"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.router_path()
```



### `.route_userinfo`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L273"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_userinfo()
```



### `.route_logout`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L281"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_logout()
```



### `.route_gettoken`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/auth.py/#L294"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.route_gettoken()
```

