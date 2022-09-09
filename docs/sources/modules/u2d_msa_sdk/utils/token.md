#


## MSATokenData
```python 
MSATokenData()
```



----


## MSAToken
```python 
MSAToken(
   secret_key: str, algorithm: str = 'HS256'
)
```




**Methods:**


### .create_token
```python
.create_token(
   data: dict, expire_minutes: int = 100
)
```


### .verify_token
```python
.verify_token(
   token: str
)
```


### .get_current_user
```python
.get_current_user(
   token: str = Depends(oauth2_scheme)
)
```

