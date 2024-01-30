from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from src.conf.config import settings
from src.services.auth import auth_service


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="Our service feedback",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates',
)


async def send_email(email: EmailStr, username: str, host: str, payload: dict):
    """
    The send_email function is used to send an email to a user.
        It takes in the following parameters:
            - email: The recipient's email address.
            - username: The recipient's username. This will be used for personalization purposes in the template body of the message being sent out.
            - host: The hostname of where this service is running on (e.g., http://localhost). This will be used for personalization purposes in the template body of the message being sent out, as well as for generating a link that can be clicked by users to verify their emails and complete registration/password reset processes

    :param email: EmailStr: Validate the email address
    :param username: str: Pass the username to the template
    :param host: str: Pass the hostname of the server to the template
    :param payload: dict: Pass the subject, template_name and other parameters
    :return: A coroutine object, which is a special kind of iterator
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject=payload["subject"],
            recipients=[email],
            template_body={"host": host, "username": username, "token": token_verification},
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name=payload["template_name"])
    except ConnectionErrors as err:
        print(err)