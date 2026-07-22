import logging

from backend.app.models.contact import ContactRequest

from backend.app.services.ai_service import ai_service
from backend.app.services.email_service import email_service
from backend.app.services.metrics_service import metrics_service

from backend.app.core.config import settings


logger = logging.getLogger("portfolio-api")


class ContactService:

    async def process_contact(
        self,
        contact: ContactRequest
    ):

        logger.info(
            f"New contact request from {contact.email}"
        )

        # AI анализ
        try:
            ai_result = await ai_service.analyze_comment(
                contact.comment
            )

        except Exception as e:
            logger.error(
                f"AI service error: {e}"
            )

            ai_result = {
                "sentiment": "unknown",
                "category": "other",
                "reply": (
                    "Спасибо за обращение. "
                    "Мы свяжемся с вами в ближайшее время."
                )
            }


        logger.info(
            f"AI result: {ai_result}"
        )


        owner_message = f"""
Новое обращение с сайта

Имя:
{contact.name}

Email:
{contact.email}

Телефон:
{contact.phone}

Комментарий:
{contact.comment}


AI анализ:

Тональность:
{ai_result.get("sentiment")}

Категория:
{ai_result.get("category")}

Ответ:
{ai_result.get("reply")}
"""


        # Отправка владельцу
        try:
            await email_service.send_email(
                settings.OWNER_EMAIL,
                "Новое обращение с сайта",
                owner_message
            )

            logger.info(
                "Owner email sent successfully"
            )

        except Exception as e:
            logger.error(
                f"Owner email error: {e}"
            )


        user_message = f"""
Здравствуйте, {contact.name}!

Спасибо за ваше обращение.

{ai_result.get("reply")}

--
Это автоматическое письмо.
"""


        # Отправка пользователю
        try:
            await email_service.send_email(
                contact.email,
                "Ваше обращение получено",
                user_message
            )

            logger.info(
                "User email sent successfully"
            )

        except Exception as e:
            logger.error(
                f"User email error: {e}"
            )


        # статистика всегда увеличивается
        try:
            metrics_service.success()

        except Exception as e:
            logger.error(
                f"Metrics error: {e}"
            )


        return {
            "success": True,
            "message": "Contact request processed",
            "ai_analysis": ai_result
        }


contact_service = ContactService()