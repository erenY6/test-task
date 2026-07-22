import logging

from app.models.contact import ContactRequest

from app.services.ai_service import ai_service
from app.services.email_service import email_service
from app.services.metrics_service import metrics_service

from app.core.config import settings


logger = logging.getLogger("portfolio-api")


class ContactService:

    async def process_contact(
        self,
        contact: ContactRequest
    ):

        logger.info(
            f"New contact request from {contact.email}"
        )


        # 1. AI анализ комментария
        ai_result = await ai_service.analyze_comment(
            contact.comment
        )


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

------------------------

AI анализ

Тональность:
{ai_result["sentiment"]}

Категория:
{ai_result["category"]}

Автоматический ответ пользователю:

{ai_result["reply"]}
"""


        await email_service.send_email(
            settings.OWNER_EMAIL,
            "Новое обращение с сайта",
            owner_message
        )


        # 3. Письмо пользователю
        user_message = f"""
Здравствуйте, {contact.name}!

{ai_result["reply"]}

--
Это автоматическое письмо.
"""


        await email_service.send_email(
            contact.email,
            "Ваше обращение получено",
            user_message
        )

        metrics_service.success()   

        return {
            "success": True,
            "message": "Contact request processed",
            "ai_analysis": ai_result
        }


contact_service = ContactService()