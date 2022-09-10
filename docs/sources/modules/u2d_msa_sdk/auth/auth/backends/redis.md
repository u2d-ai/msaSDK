#


## RedisTokenStore
```python 
RedisTokenStore(
   redis: Redis, expire_seconds: Optional[int] = 60*60*24*3,
   TokenDataSchema: _TokenDataSchemaT = None
)
```




**Methods:**


### .read_token
```python
.read_token(
   token: str
)
```


### .write_token
```python
.write_token(
   token_data: Union[_TokenDataSchemaT, dict]
)
```


### .destroy_token
```python
.destroy_token(
   token: str
)
```


### .get_key
```python
.get_key(
   token: str
)
```
