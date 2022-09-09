#


## AuthBackend
```python 
AuthBackend(
   auth: 'Auth', token_store: BaseTokenStore
)
```




**Methods:**


### .get_user_token
```python
.get_user_token(
   request: Request
)
```


### .authenticate
```python
.authenticate(
   request: Request
)
```


### .attach_middleware
```python
.attach_middleware(
   app: FastAPI
)
```


----


## Auth
```python 
Auth(
   db: Union[AsyncDatabase, Database], token_store: BaseTokenStore = None,
   user_model: Type[_UserModelT] = User,
   pwd_context: CryptContext = CryptContext(schemes = ['bcrypt'], deprecated = 'auto')
)
```




**Methods:**


### .authenticate_user
```python
.authenticate_user(
   username: str, password: Union[str, SecretStr]
)
```


### .get_current_user
```python
.get_current_user()
```


### .requires
```python
.requires(
   roles: Union[str, Sequence[str]] = None, groups: Union[str, Sequence[str]] = None,
   permissions: Union[str, Sequence[str]] = None, status_code: int = 403,
   redirect: str = None, response: Union[bool, Response] = None
)
```


### .create_role_user
```python
.create_role_user(
   role_key: str = 'admin'
)
```


----


## AuthRouter
```python 
AuthRouter(
   auth: Auth = None
)
```




**Methods:**


### .router_path
```python
.router_path()
```


### .route_userinfo
```python
.route_userinfo()
```


### .route_logout
```python
.route_logout()
```


### .route_gettoken
```python
.route_gettoken()
```

