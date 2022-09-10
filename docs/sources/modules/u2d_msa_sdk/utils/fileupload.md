#



## `ServerHTTPException`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L78"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
ServerHTTPException(
   error: str = None
)
```



----



## `InvalidResource`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L85"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
InvalidResource()
```


---
raise when has invalid resource

----



## `NoSuchFieldFound`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L91"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
NoSuchFieldFound()
```


---
raise when no such field for the given

----



## `FileMaxSizeLimit`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L97"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
FileMaxSizeLimit()
```


---
raise when the upload file exceeds the max size

----



## `FileExtNotAllowed`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L103"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
FileExtNotAllowed()
```


---
raise when the upload file ext not allowed

----



## `FileUpload`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L113"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
FileUpload(
   filesize: int, root_path: str = os.path.join(os.path.dirname(__file__)),
   uploads_dir: str = 'data/uploads',
   not_allow_extensions: Optional[List[str]] = None, max_size: int = 150000000,
   createUIDSubFolders: bool = False
)
```




**Methods:**



### `.save_file`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L137"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.save_file(
   filename: str, ufile: UploadFile
)
```



### `.upload`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L160"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.upload(
   file: UploadFile
)
```


----



## `FileDelete`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L177"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
FileDelete(
   uid: str, root_path: str = os.path.join(os.path.dirname(__file__)),
   uploads_dir: str = 'data/uploads'
)
```




**Methods:**



### `.delete_files`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L189"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.delete_files()
```


----



## secure_filename
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L36"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.secure_filename(
   filename: str
)
```

---
Pass it a filename and it will return a secure version of it.  This
filename can then safely be stored on a regular file system and passed
to :func:`os.path.join`.  The filename returned is an ASCII only string
for maximum portability.
On windows systems the function also makes sure that the file is not
named after one of the special device files.

```python

>>> secure_filename("../../../etc/passwd")
'etc_passwd'
>>> secure_filename('i contain cool \xfcml\xe4uts.txt')
'i_contain_cool_umlauts.txt'
The function might return an empty filename.  It's your responsibility
to ensure that the filename is unique and that you abort or
generate a random filename if the function returned an empty one.
.. versionadded:: 0.5
:param filename: the filename to secure
```

----



## nameGen
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L109"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.nameGen(
   uid, file
)
```


----



## checkIfFileIsArchive
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L210"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.checkIfFileIsArchive(
   file: UploadFile
)
```


----



## createMSAFile
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L224"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createMSAFile(
   file: UploadFile, up: FileUpload
)
```


----



## createMSAFileFromUnpacked
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/fileupload.py/#L236"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.createMSAFileFromUnpacked(
   filepath: str, processuid: str
)
```

