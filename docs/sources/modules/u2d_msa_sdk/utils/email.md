#


## MSASendEmail
```python 
MSASendEmail(
   smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str,
   timeout: int = 60, testmode: bool = False
)
```




**Methods:**


### .send_email
```python
.send_email(
   from_email: str, to_email: str, subject: str, body: str,
   jinja_template_path_html: str = ''
)
```

---
Send an email.
