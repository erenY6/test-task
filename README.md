# Backend Service — Developer Landing API

Backend-сервис для лендинг-презентации разработчика с API обратной связи, AI-анализом обращений и автоматической отправкой email-уведомлений.

## Возможности

- REST API для формы обратной связи
- Валидация входящих данных
- Отправка email владельцу сайта и пользователю
- AI-анализ комментариев
- Генерация ответа пользователю с помощью AI
- Graceful fallback при недоступности AI
- Rate limiting для защиты от спама
- Логирование запросов
- Статистика обращений
- Swagger/OpenAPI документация

# 1. Запуск проекта

## Требования

- Python 3.9+
- pip

## Установка

Клонировать репозиторий:

```bash
git clone <repository_url>
cd backend
```

Создать виртуальное окружение:

```bash
python -m venv venv
```

Активация:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Установка зависимостей:

```bash
pip install -r requirements.txt
```

## Настройка переменных окружения

Создать файл `.env`:

```env
APP_NAME=Developer Landing API

OPENAI_API_KEY=your_openai_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=password

OWNER_EMAIL=owner_email@gmail.com

CORS_ORIGINS=http://localhost:3000
```

## Запуск

```bash
uvicorn app.main:app --reload
```

После запуска:

Swagger:

```
http://localhost:8000/docs
```

API:

```
http://localhost:8000
```

---

# 2. Стек технологий

## Backend

- Python 3.13
- FastAPI
- Pydantic
- Uvicorn
- python-dotenv
- SMTP
- Logging

## AI

Используется OpenAI API.

AI используется для:

- анализа тональности сообщения
- классификации обращения
- генерации автоматического ответа пользователю

---

# 3. Архитектура проекта

Проект построен по слоистой архитектуре:

```
app/

├── api/
│   └── endpoints
│
├── schemas/
│   └── Pydantic модели
│
├── services/
│   ├── AI
│   ├── Email
│   └── Rate limiting
│
├── repositories/
│   └── работа с файлами
│
├── core/
│   ├── config
│   ├── logging
│   └── exceptions
│
└── main.py
```

## Использованные паттерны

### Controller-Service

API-слой отвечает только за HTTP:

```
Request
 ↓
Controller
 ↓
Service
 ↓
Repository
 ↓
Response
```

### Repository Pattern

Работа с хранением данных вынесена отдельно от бизнес-логики.

## Почему FastAPI

FastAPI выбран из-за:

- автоматической OpenAPI документации
- встроенной валидации через Pydantic
- высокой производительности
- удобной работы с REST API

---

# 4. Реализация API

## POST /api/contact

Создание обращения.

### Request

```json
{
  "name": "Иван",
  "email": "ivan@mail.com",
  "phone": "+79999999999",
  "comment": "Хочу заказать разработку сайта"
}
```

### Response

```json
{
  "success": true,
  "message": "Заявка успешно отправлена",
  "ai_analysis": {
    "sentiment": "positive",
    "category": "development",
    "reply": "Спасибо за обращение. Мы свяжемся с вами."
  }
}
```

## GET /api/health

Проверка состояния сервиса.

Response:

```json
{
  "status": "ok"
}
```

## GET /api/metrics

Возвращает статистику обращений.

---

# Валидация данных

Используется Pydantic.

Проверяется:

- обязательность полей
- корректность email
- формат телефона
- максимальная длина комментария
- очистка входных данных

---

# Обработка ошибок

Реализован глобальный обработчик ошибок.

Используемые HTTP-коды:

| Код | Описание                |
| --- | ----------------------- |
| 200 | Успешный запрос         |
| 400 | Ошибка данных           |
| 422 | Ошибка валидации        |
| 429 | Превышен лимит запросов |
| 500 | Ошибка сервера          |

---

# 5. AI-интеграция

## Используемый инструмент

OpenAI API.

## Функции AI

После получения комментария пользователя отправляется запрос:

- определить тональность
- определить категорию обращения
- сформировать ответ

Пример результата:

```json
{
  "sentiment": "neutral",
  "category": "question",
  "reply": "Спасибо за обращение..."
}
```

## Fallback механизм

Если AI API недоступен:

- ошибка перехватывается
- сервис продолжает работу
- возвращается стандартный ответ

Пример:

```json
{
  "sentiment": "unknown",
  "category": "other",
  "reply": "Спасибо за обращение. Мы скоро свяжемся."
}
```

## Использованный промпт

```
Проанализируй сообщение пользователя.

Верни JSON:

{
 sentiment:"",
 category:"",
 reply:""
}

Сообщение:
{comment}
```

---

# 6. Использование AI при разработке

AI использовался как вспомогательный инструмент разработки.

Использованные задачи:

- генерация структуры проекта
- помощь в написании FastAPI компонентов
- подготовка схем Pydantic
- создание AI-интеграции
- поиск ошибок и оптимизация

Примеры промптов:

```
Создай REST API на FastAPI
с разделением Controller-Service-Repository
```

```
Добавь обработку ошибок
и graceful fallback для OpenAI API
```

Все сгенерированные части были проверены,
адаптированы под проект и исправлены вручную.

---

# 7. Хранение данных

## Логи

Все запросы сохраняются в файл:

```
logs/app.log
```

Логируется:

- время запроса
- HTTP метод
- endpoint
- IP клиента
- статус ответа
- время выполнения

---

## Rate limiting

Используется файловое хранилище:

```
storage/rate_limit.json
```

Ограничение:

```
5 запросов в минуту от одного IP
```

При превышении возвращается:

```
HTTP 429 Too Many Requests
```

---

## Статистика

Статистика обращений хранится:

```
storage/requests.json
```

Сохраняется:

- количество обращений
- время создания
- категория обращения
- результат AI анализа

---

# Примеры запросов

curl:

```bash
curl -X POST http://localhost:8000/api/contact \
-H "Content-Type: application/json" \
-d '{
"name":"Alex",
"email":"alex@mail.com",
"phone":"+79999999999",
"comment":"Need a website"
}'
```

---

# Автор

Developer Landing API Test Task
