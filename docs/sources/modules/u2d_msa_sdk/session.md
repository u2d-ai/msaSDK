#


## SessionData
```python 
SessionData()
```



----


## BasicVerifier
```python 
BasicVerifier(
   *, identifier: str, auto_error: bool, backend: InMemoryBackend[UUID,
   SessionData], auth_http_exception: HTTPException
)
```




**Methods:**


### .identifier
```python
.identifier()
```


### .backend
```python
.backend()
```


### .auto_error
```python
.auto_error()
```


### .auth_http_exception
```python
.auth_http_exception()
```


### .verify_session
```python
.verify_session(
   model: SessionData
)
```

---
If the session exists, it is valid

----


### xuuid4
```python
.xuuid4()
```


----


### getSecretKey
```python
.getSecretKey()
```

