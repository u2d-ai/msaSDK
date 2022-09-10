#



## `PkMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L17"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
PkMixin()
```



----



## `CreateTimeMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L21"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
CreateTimeMixin()
```



----



## `UsernameMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L25"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
UsernameMixin()
```



----



## `PasswordStr`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L32"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
PasswordStr()
```



----



## `PasswordMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L36"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
PasswordMixin()
```



----



## `EmailMixin`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L44"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
EmailMixin()
```



----



## `UserRoleLink`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L53"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
UserRoleLink()
```



----



## `UserGroupLink`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L63"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
UserGroupLink()
```



----



## `GroupRoleLink`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L73"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
GroupRoleLink()
```



----



## `RolePermissionLink`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L83"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
RolePermissionLink()
```



----



## `BaseUser`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L93"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseUser()
```




**Methods:**



### `.is_authenticated`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L111"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.is_authenticated()
```



### `.display_name`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L115"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.display_name()
```



### `.identity`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L119"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.identity()
```



### `.has_requires`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L175"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

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



## `User`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L207"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
User()
```



----



## `BaseRBAC`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L214"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseRBAC()
```



----



## `Role`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L224"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
Role()
```


---
角色

----



## `BaseGroup`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L231"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
BaseGroup()
```



----



## `Group`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L236"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
Group()
```


---
用户组

----



## `Permission`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/auth/auth/models.py/#L241"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
Permission()
```


---
权限
