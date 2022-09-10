#



## `MSASendEmail`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/email.py/#L12"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
MSASendEmail(
   smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str,
   timeout: int = 60, testmode: bool = False
)
```




**Methods:**



### `.send_email`
<p align="right" style="margin-top:-20px;margin-bottom:-15px;"><a href="https://github.com/swelcker/U2D_MSA_SDK/tree/0.0.7/u2d_msa_sdk/utils/email.py/#L22"><img src="https://img.shields.io/badge/-source-cccccc?style=flat&logo=github"></a></p>

```python
.send_email(
   from_email: str, to_email: str, subject: str, body: str,
   jinja_template_path_html: str = ''
)
```

---
Send an email.
