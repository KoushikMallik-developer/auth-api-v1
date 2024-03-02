import logging

from fastapi_mail import FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader
from pydantic import EmailStr
from core.config import EmailConfig
from core.services.email_services.types.email_content_type import EmailContentType


class EmailService:
    def __init__(self):
        self.template_env = Environment(
            loader=FileSystemLoader("./core/services/email_services/templates")
        )
        self.config = EmailConfig().get_config()
        self.client = FastMail(self.config)

    async def send_email(self, to: EmailStr, content: EmailContentType):
        message_schema = MessageSchema(
            subject=content.subject,
            recipients=[to],
            cc=content.cc,
            bcc=content.bcc,
            body=content.content,
            subtype=MessageType.html,
        )

        try:
            await self.client.send_message(message=message_schema)
        except Exception as e:
            logging.error(f"EmailNotSentError: {e}")

    def create_verification_code_email(
        self, verification_code: str, name: str
    ) -> EmailContentType:
        email = EmailContentType(subject="Shoopixa User Verification")
        template = self.template_env.get_template(
            "verification_code_email_template.html"
        )
        html_content = template.render(fname=name, otp=verification_code)
        email.content = html_content
        return email
