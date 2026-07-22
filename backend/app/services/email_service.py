import logging
import smtplib
import ssl

from email.message import EmailMessage
from email.utils import formataddr

from app.core.config import settings


logger = logging.getLogger("portfolio-api")


class EmailService:


    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ) -> bool:

        try:

            self._send_sync(
                recipient,
                subject,
                body
            )

            logger.info(
                f"Email sent successfully: {recipient}"
            )

            return True


        except Exception as error:

            logger.exception(
                f"Email failed: {error}"
            )

            return False



    def _send_sync(
        self,
        recipient: str,
        subject: str,
        body: str
    ):

        message = EmailMessage()

        message["From"] = formataddr(
            (
                "Portfolio Bot",
                settings.SMTP_USER
            )
        )

        message["To"] = recipient

        message["Subject"] = subject


        message.set_content(
            body,
            charset="utf-8"
        )


        logger.info(
            f"SMTP connect {settings.SMTP_HOST}:{settings.SMTP_PORT}"
        )


        context = ssl.create_default_context()


        with smtplib.SMTP_SSL(
            settings.SMTP_HOST,
            int(settings.SMTP_PORT),
            timeout=20,
            context=context
        ) as server:


            logger.info(
                "SMTP SSL connected"
            )


            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD
            )


            logger.info(
                "SMTP login OK"
            )


            server.send_message(
                message
            )


            logger.info(
                "SMTP send OK"
            )



email_service = EmailService()