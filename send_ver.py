"""import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send(email,url):
    with open("ver_email.html","r") as f:
        html_content=f.read().replace("{{url}}",url).replace("{{url}}",url)
    message = Mail(
        from_email='account@mail.weathon.top',
        to_emails=email,
        subject='Confirm Your Email Address',
        html_content=html_content)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
"""

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def send(email: str, token: str):
    vurl = "https://farmer.weathon.top/static/confirm.html?token="+token
    with open("ver_email.html", "r") as f:
        html_content = f.read().replace(
            "{{url}}", vurl).replace("{{url}}", vurl)
    print(vurl)
    msg = MIMEText(html_content, 'html', 'utf-8')
    from_addr = "farmer.weathon@gmail.com"
    password = "jkchsedkfyg*&T&GFW*^(RFVI"
    to_addr = email
    smtp_server = "smtp.gmail.com"

    msg['From'] = _format_addr('Account <%s>' % from_addr)
    msg['To'] = _format_addr(to_addr)
    msg['Subject'] = Header('Account Verification', 'utf-8').encode()

    smtp_port = 587
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()