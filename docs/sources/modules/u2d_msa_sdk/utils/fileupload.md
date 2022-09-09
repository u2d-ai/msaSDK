#


## ServerHTTPException
```python 
ServerHTTPException(
   error: str = None
)
```



----


## InvalidResource
```python 
InvalidResource()
```


---
raise when has invalid resource

----


## NoSuchFieldFound
```python 
NoSuchFieldFound()
```


---
raise when no such field for the given

----


## FileMaxSizeLimit
```python 
FileMaxSizeLimit()
```


---
raise when the upload file exceeds the max size

----


## FileExtNotAllowed
```python 
FileExtNotAllowed()
```


---
raise when the upload file ext not allowed

----


## FileUpload
```python 
FileUpload(
   filesize: int, root_path: str = os.path.join(os.path.dirname(__file__)),
   uploads_dir: str = 'data/uploads',
   not_allow_extensions: Optional[List[str]] = None, max_size: int = 150000000,
   createUIDSubFolders: bool = False
)
```




**Methods:**


### .save_file
```python
.save_file(
   filename: str, ufile: UploadFile
)
```


### .upload
```python
.upload(
   file: UploadFile
)
```


----


## FileDelete
```python 
FileDelete(
   uid: str, root_path: str = os.path.join(os.path.dirname(__file__)),
   uploads_dir: str = 'data/uploads'
)
```




**Methods:**


### .delete_files
```python
.delete_files()
```


----


### secure_filename
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


### nameGen
```python
.nameGen(
   uid, file
)
```


----


### checkIfFileIsArchive
```python
.checkIfFileIsArchive(
   file: UploadFile
)
```


----


### createMSAFile
```python
.createMSAFile(
   file: UploadFile, up: FileUpload
)
```


----


### createMSAFileFromUnpacked
```python
.createMSAFileFromUnpacked(
   filepath: str, processuid: str
)
```

