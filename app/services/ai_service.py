import json
import logging

from openai import AsyncOpenAI

from app.core.config import settings


logger = logging.getLogger("portfolio-api")


class AIService:

    def __init__(self):

        if settings.GROQ_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.GROQ_API_KEY,
                base_url=settings.GROQ_BASE_URL
            )
        else:
            self.client = None

    async def analyze_comment(
        self,
        comment: str
    ) -> dict:

        # Graceful fallback, если AI недоступен
        if not self.client:

            logger.warning(
                "Groq API key is missing. Using fallback."
            )

            return {
                "sentiment": "unknown",
                "category": "general",
                "reply": (
                    "Здравствуйте! Спасибо за ваше обращение. "
                    "Мы получили вашу заявку и свяжемся с вами в ближайшее время."
                )
            }

        try:

            response = await self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": """
Ты анализируешь обращения пользователей.
Пиши без приветствий и прощаний.

Определи:

1. sentiment:
positive / neutral / negative

2. category:
development / support / question / general

3. reply:
Напиши короткий, вежливый ответ пользователю
(2–3 предложения).

Верни только JSON.

Пример:

{
    "sentiment": "positive",
    "category": "development",
    "reply": "Спасибо за ваше обращение. Мы рассмотрим ваш запрос и свяжемся с вами в ближайшее время."
}
"""
                    },
                    {
                        "role": "user",
                        "content": comment
                    }
                ],
                temperature=0
            )

            content = response.choices[0].message.content

            logger.info(
                f"AI response: {content}"
            )

            return json.loads(content)

        except Exception as error:

            logger.exception(
                f"AI error: {error}"
            )

            # Graceful fallback
            return {
                "sentiment": "unknown",
                "category": "general",
                "reply": (
                    "Здравствуйте! Спасибо за ваше обращение. "
                    "Мы получили вашу заявку и свяжемся с вами в ближайшее время."
                )
            }


ai_service = AIService()