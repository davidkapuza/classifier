from fastapi_mail import MessageSchema, MessageType

from .main import mail

from src.config import Config


class MailService:
    async def send_confirmation_email(self, email: str, token: str):
        confirmation_url = f"{Config.API_URL}/api/v1/auth/verify/{token}"

        message = MessageSchema(
            subject="Confirm your email",
            recipients=[email],
            template_body={
                "confirmation_url": confirmation_url,
                "expire_minutes": Config.AUTH_EMAIL_CONFIRMATION_EXPIRES,
                "user_email": email,
            },
            subtype=MessageType.html,
        )

        await mail.send_message(message, template_name="email_confirmation.html")
