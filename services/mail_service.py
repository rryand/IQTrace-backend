import smtplib, ssl

from settings import (SMTP_PORT, SMTP_SERVER, 
  SENDER_EMAIL, EMAIL_PASSWORD, API_URL)

def _getMessage(receiver_email: str, verification_id: str) -> str:
  subject = "IQTrace Email Verification"
  body = """\
    Please click on the link below to verify.
    
    %s/verification/%s""" % (API_URL, verification_id)

  return """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (SENDER_EMAIL, receiver_email, subject, body)

def send_verification_email(receiver_email: str, verification_id: str):
  context = ssl.create_default_context()
  message = _getMessage(receiver_email, verification_id)
  with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
    server.login(SENDER_EMAIL, EMAIL_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg=message)
