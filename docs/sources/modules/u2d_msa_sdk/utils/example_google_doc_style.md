#



## `ExampleError`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L154"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ExampleError(
   msg, code
)
```


---
Exceptions are documented in the same way as classes.

The __init__ method may be documented in either the class level
docstring, or as a docstring on the __init__ method itself.

Either form is acceptable, but the two should not be mixed. Choose one
convention to document the __init__ method and be consistent with it.


**Note**

Do not include the `self` parameter in the ``Args`` section.


**Args**

* **msg** (str) : Human readable string describing the exception.
* **code** (:obj:`int`, optional) : Error code.


**Attributes**

* **msg** (str) : Human readable string describing the exception.
* **code** (int) : Exception error code.


----



## `ExampleClass`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L181"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ExampleClass(
   param1, param2, param3
)
```


---
The summary line for a class docstring should fit on one line.

If the class has public attributes, they may be documented here
in an ``Attributes`` section and follow the same formatting as a
function's ``Args`` section. Alternatively, attributes may be documented
inline with the attribute's declaration (see __init__ method below).

Properties created with the ``@property`` decorator should be documented
in the property's getter method.


**Attributes**

* **attr1** (str) : Description of `attr1`.
* **attr2** (:obj:`int`, optional) : Description of `attr2`.



**Methods:**



### `.readonly_property`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L228"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.readonly_property()
```

---
str: Properties should be documented in their getter method.


### `.readwrite_property`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L233"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.readwrite_property()
```

---
:obj:`list` of :obj:`str`: Properties with both a getter and setter
should only be documented in their getter method.

If the setter method contains notable behavior, it should be
mentioned here.


### `.example_method`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L246"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.example_method(
   param1, param2
)
```

---
Class methods are similar to regular functions.


**Note**

Do not include the `self` parameter in the ``Args`` section.


**Args**

* **param1**  : The first parameter.
* **param2**  : The second parameter.


**Returns**

True if successful, False otherwise.

----



## function_with_types_in_docstring
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L46"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.function_with_types_in_docstring(
   param1, param2
)
```

---
Example function with types documented in the docstring.

`PEP 484`_ type annotations are supported. If attribute, parameter, and
return types are annotated according to `PEP 484`_, they do not need to be
included in the docstring:


**Args**

* **param1** (int) : The first parameter.
* **param2** (str) : The second parameter.


**Returns**

* **bool**  : The return value. True for success, False otherwise.

---
.. _PEP 484:
    https://www.python.org/dev/peps/pep-0484/

----



## function_with_pep484_type_annotations
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L66"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.function_with_pep484_type_annotations(
   param1: int, param2: str
)
```

---
Example function with PEP 484 type annotations.


**Args**

* **param1**  : The first parameter.
* **param2**  : The second parameter.


**Returns**

The return value. True for success, False otherwise.

----



## module_level_function
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L79"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.module_level_function(
   param1, param2 = None, *args, **kwargs
)
```

---
This is an example of a module level function.

Function parameters should be documented in the ``Args`` section. The name
of each parameter is required. The type and description of each parameter
is optional, but should be included if not obvious.

If \*args or \*\*kwargs are accepted,
they should be listed as ``*args`` and ``**kwargs``.

The format for a parameter is::

    descriptions.


**Args**

* **param1** (int) : The first parameter.
* **param2** (:obj:`str`, optional) : The second parameter. Defaults to None.
    Second line of description should be indented.
* **args**  : Variable length argument list.
* **kwargs**  : Arbitrary keyword arguments.


**Returns**

* **bool**  : True if successful, False otherwise.
* param1,
        'param2': param2
    }

The return type is optional and may be specified at the beginning of
the ``Returns`` section followed by a colon.

The ``Returns`` section may span multiple lines and paragraphs.
Following lines should be indented to match the first line.

The ``Returns`` section supports any reStructuredText formatting,
including literal blocks::

    {


**Raises**

* **AttributeError**  : The ``Raises`` section is a list of all exceptions
    that are relevant to the interface.
* **ValueError**  : If `param2` is equal to `param1`.


----



## example_generator
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/example_google_doc_style.py/#L133"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.example_generator(
   n
)
```

---
Generators have a ``Yields`` section instead of a ``Returns`` section.


**Args**

* **n** (int) : The upper limit of the range to generate, from 0 to `n` - 1.


**Yields**

* **int**  : The next number in the range of 0 to `n` - 1.


**Examples**

Examples should be written in doctest format, and should illustrate how
to use the function.

>>> print([i for i in example_generator(4)])
[0, 1, 2, 3]
