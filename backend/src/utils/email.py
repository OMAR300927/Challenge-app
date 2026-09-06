import smtplib
from email.message import EmailMessage

from ..core.config import settings


def send_email(subject: str, body: str) -> None:
    message = EmailMessage()

    message["Subject"] = subject
    message["From"] = (
      f"{settings.mailtrap_from_name} "
      f"<{settings.mailtrap_from_email}>"
    )
    message["To"] = settings.mailtrap_to_email

    message.set_content(body)

    with smtplib.SMTP(
      settings.mailtrap_host,
      settings.mailtrap_port,
    ) as server:
      server.starttls()

      server.login(
        settings.mailtrap_username,
        settings.mailtrap_password,
      )

      server.send_message(message)