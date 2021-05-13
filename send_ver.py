import os
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

