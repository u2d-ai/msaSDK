#


## I18N
```python 

```




**Methods:**


### .load_translations
```python
.load_translations(
   translations: Dict[str, GNUTranslations]
)
```


### .set_language
```python
.set_language(
   language: str = None
)
```

---
设置i18n本地化语言.如果为空,则依次尝试读取环境变量`LANGUAGE`/`LANG`,系统默认语言.
:param language: 尝试设置的语言
:return: 设置成功后的语言

### .get_language
```python
.get_language()
```

