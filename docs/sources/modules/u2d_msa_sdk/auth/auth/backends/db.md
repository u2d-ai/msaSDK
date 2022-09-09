#


## TokenStoreModel
```python 
TokenStoreModel()
```



----


## DbTokenStore
```python 
DbTokenStore(
   db: Union[AsyncDatabase, Database], expire_seconds: Optional[int] = 60*60*24*3,
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

