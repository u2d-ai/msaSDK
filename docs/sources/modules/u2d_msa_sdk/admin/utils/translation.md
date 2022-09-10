#



## `I18N`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/utils/translation.py/#L8"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python

```




**Methods:**



### `.load_translations`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/utils/translation.py/#L14"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.load_translations(
   translations: Dict[str, GNUTranslations]
)
```



### `.set_language`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/utils/translation.py/#L21"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.set_language(
   language: str = None
)
```

---
设置i18n本地化语言.如果为空,则依次尝试读取环境变量`LANGUAGE`/`LANG`,系统默认语言.
:param language: 尝试设置的语言
:return: 设置成功后的语言


### `.get_language`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/admin/utils/translation.py/#L31"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.get_language()
```

