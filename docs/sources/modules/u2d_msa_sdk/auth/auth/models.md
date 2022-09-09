#


## PkMixin
```python 
PkMixin()
```



----


## CreateTimeMixin
```python 
CreateTimeMixin()
```



----


## UsernameMixin
```python 
UsernameMixin()
```



----


## PasswordStr
```python 
PasswordStr()
```



----


## PasswordMixin
```python 
PasswordMixin()
```



----


## EmailMixin
```python 
EmailMixin()
```



----


## UserRoleLink
```python 
UserRoleLink()
```



----


## UserGroupLink
```python 
UserGroupLink()
```



----


## GroupRoleLink
```python 
GroupRoleLink()
```



----


## RolePermissionLink
```python 
RolePermissionLink()
```



----


## BaseUser
```python 
BaseUser()
```




**Methods:**


### .is_authenticated
```python
.is_authenticated()
```


### .display_name
```python
.display_name()
```


### .identity
```python
.identity()
```


### .has_requires
```python
.has_requires(
   session: Session, *, roles: Union[str, Sequence[str]] = None, groups: Union[str,
   Sequence[str]] = None, permissions: Union[str, Sequence[str]] = None
)
```

---
检查用户是否属于拥有指定的RBAC权限

**Args**

* **session**  : sqlalchemy `Session`;异步`AsyncSession`,请使用`run_sync`方法.
* **roles**  : 角色列表
* **groups**  : 用户组列表
* **permissions**  : 权限列表


**Returns**

检测成功返回`True`

----


## User
```python 
User()
```



----


## BaseRBAC
```python 
BaseRBAC()
```



----


## Role
```python 
Role()
```


---
角色

----


## BaseGroup
```python 
BaseGroup()
```



----


## Group
```python 
Group()
```


---
用户组

----


## Permission
```python 
Permission()
```


---
权限
