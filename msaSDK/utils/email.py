# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiofiles import os
from jinja2 import Template


class MSASendEmail:
    def __init__(self, smtp_host: str, smtp_port: int, smtp_username: str, smtp_password: str, timeout: int = 60, testmode: bool = False):
        super().__init__()
        self.host: str = smtp_host
        self.port: int = smtp_port
        self.username: str = smtp_username
        self.password: str = smtp_password
        self.timeout: int = timeout
        self.testmode: bool = testmode
        """Testmode True doesnt send the email out through SMTP Server"""

    async def send_email(self, from_email: str, to_email: str, subject: str, body: str, jinja_template_path_html: str = ""):
        """Send an email.

            Raises:
                TypeError: Error: MSASendEmail: HTML Templatefile ... not exists
                TypeError: Error: MSASendEmail: SMTP Server Login failed for User
        """
        msg = MIMEMultipart("alternative")
        # me == the sender's email address
        # you == the recipient's email address
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Get the contents of the template.
        if len(jinja_template_path_html)>0:
            if os.path.exists(jinja_template_path_html):
                with open(jinja_template_path_html, "r") as template:
                    # Parse
                    template = Template(template.read())
                    html = template.render(body=body)
                    msg.attach(MIMEText(html, "html"))
            else:
                raise TypeError("Error: MSASendEmail: HTML Templatefile " + jinja_template_path_html + " not exists")

        # inject the body.
        text = body
        msg.attach(MIMEText(text, "plain"))

        if self.testmode:
            # Do not send an actual email if testmode is True.
            return

        smtpObj = smtplib.SMTP(host=self.host, port=self.port, timeout=self.timeout)
        if len(self.username)>0:
            try:
                smtpObj.login(user=self.username, password=self.password)
            except Exception as e:
                raise TypeError("Error: MSASendEmail: SMTP Server Login failed for User " + self.username + " ErrorMessage: " + e.__str__())
        smtpObj.send_message(msg)
