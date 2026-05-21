# JWT FastAPI Demo

Демонстрационный проект: **JWT-аутентификация** (access + refresh токены) на **FastAPI**.

## Структура проекта

```
jwt_fastapi/
├── app/
│   ├── core/
│   │   ├── config.py       # Настройки (Pydantic Settings)
│   │   └── security.py     # JWT: создание, декодирование, хэширование паролей
│   ├── models/
│   │   └── user.py         # In-memory «база данных» пользователей
│   ├── routers/
│   │   ├── auth.py         # /auth/register, /login, /refresh, /logout
│   │   └── users.py        # /users/me, /users/ (admin), /users/{username}
│   ├── schemas/
│   │   └── auth.py         # Pydantic-схемы запросов и ответов
│   └── main.py             # FastAPI app
├── tests/
│   └── test_auth.py        # Pytest-тесты всего JWT-флоу
├── .env.example
└── requirements.txt
```

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Скопировать .env
cp .env.example .env

# 3. Запустить сервер
uvicorn app.main:app --reload

# 4. Открыть документацию
# http://127.0.0.1:8000/docs
```

## JWT-флоу

```
POST /auth/register   → создать пользователя
POST /auth/login      → получить access_token + refresh_token
GET  /users/me        → защищённый маршрут (нужен access_token)
POST /auth/refresh    → обновить access_token через refresh_token
POST /auth/logout     → выйти (клиент удаляет токены)
```

## Тестовые пользователи

| Username | Password | Role  |
|----------|----------|-------|
| alice    | alice123 | admin |
| bob      | bob456   | user  |

## Запуск тестов

```bash
pytest tests/ -v
```

## Ключевые концепции

- **Access token** — короткоживущий (30 мин), используется для каждого запроса.
- **Refresh token** — долгоживущий (7 дней), только для обновления access-токена.
- **RBAC** — роль хранится в payload токена; `require_admin` — пример dependency.
- **Logout** — при stateless JWT токен не инвалидируется на сервере. В продакшене нужен Redis-blocklist.
