import logging
import smtplib
import asyncio

from email.message import EmailMessage

from app.core.config import settings


logger = logging.getLogger("portfolio-api")


class EmailService:

    async def send_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ) -> bool:

        if not settings.SMTP_USER:
            logger.warning(
                "SMTP is not configured. Email skipped."
            )
            return False


        try:

            result = await asyncio.wait_for(
                asyncio.to_thread(
                    self._send_sync_email,
                    recipient,
                    subject,
                    body
                ),
                timeout=10
            )

            return result


        except asyncio.TimeoutError:

            logger.error(
                "Email sending timeout"
            )

            return False


        except Exception as error:

            logger.exception(
                f"Email error: {error}"
            )

            return False



    def _send_sync_email(
        self,
        recipient: str,
        subject: str,
        body: str
    ) -> bool:


        message = EmailMessage()

        message["From"] = settings.SMTP_USER
        message["To"] = recipient
        message["Subject"] = subject


        message.set_content(
            body,
            charset="utf-8"
        )


        with smtplib.SMTP(
            settings.SMTP_HOST,
            settings.SMTP_PORT,
            timeout=10
        ) as server:


            server.starttls()


            server.login(
                settings.SMTP_USER,
                settings.SMTP_PASSWORD
            )


            server.send_message(message)


        logger.info(
            f"Email sent to {recipient}"
        )


        return True



email_service = EmailService()