#


## MSAServiceDefinition
```python 
MSAServiceDefinition()
```


---
MSAApp Settings (Service Definitions)

This class enables the configuration of your MSAApp instance through the use of environment variables.

Any of the instance attributes can be overridden upon instantiation by either passing the desired value to the
initializer, or by setting the corresponding environment variable.

Attribute `xxx_yyy` corresponds to environment variable `API_XXX_YYY`. So, for example, to override
`openapi_prefix`, you would set the environment variable `API_OPENAPI_PREFIX`.

Note that assignments to variables are also validated, ensuring that even if you make runtime-modifications
to the config, they should have the correct types.

----


### get_msa_app_settings
```python
.get_msa_app_settings()
```

---
This function returns a cached instance of the MSAServiceDefinition object.

Caching is used to prevent re-reading the environment every time the API settings are used in an endpoint.