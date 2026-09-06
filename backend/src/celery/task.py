from .celery import celery_app

from ..utils.email import send_email

@celery_app.task
def send_challenge_create_message():
  send_email(
    subject="Challenge App",
    body="Challenge created successfully"
  )