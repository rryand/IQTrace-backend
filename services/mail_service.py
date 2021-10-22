import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from settings import (SMTP_PORT, SMTP_SERVER, 
  SENDER_EMAIL, EMAIL_PASSWORD, API_URL)

def _getMessage(name: str, verification_id: str) -> tuple:
  text = """\
    Hi, %s!
    
    Please click on the link below to verify your email with IQTrace.

    %s/verification/%s

    Thank you for signing up with us. Stay safe!

    Sincerely,
    The IQTrace Team

    This is an automated message. Please do not reply directly to this email.""" % (name, API_URL, verification_id)

  html = """\
    <html>
      <head></head>
      <body>
        <p>Hi, %s!</p>
        
        <p>Please click on the link below to verify your email with IQTrace.</p>

        <p>%s/verification/%s</p>

        <p>Thank you for signing up with us. Stay safe!</p>

        <p>
          Sincerely,<br>
          <b>The IQTrace Team</b>
        </p>

        <i>This is an automated message. Please do not reply directly to this email.</i>
      </body>
    </html>
    """ % (name, API_URL, verification_id)

  return (text, html)

def send_verification_email(receiver_email: str, name: str, verification_id: str):
  message = MIMEMultipart("alternative")
  message["Subject"] = "IQTrace Email Verification"
  message["From"] = SENDER_EMAIL
  message["To"] = receiver_email
  
  (text, html) = _getMessage(name, verification_id)
  text_mime = MIMEText(text, "plain")
  html_mime = MIMEText(html, "html")

  message.attach(text_mime)
  message.attach(html_mime)

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg=message.as_string())
