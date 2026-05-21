from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, users

app = FastAPI(
    title=settings.APP_NAME,
    description="""
## JWT Authentication Demo

Демонстрация JWT-аутентификации в FastAPI.

### Возможности
- **Регистрация** — `POST /auth/register`
- **Вход** — `POST /auth/login` → access + refresh токены
- **Обновление токена** — `POST /auth/refresh`
- **Выход** — `POST /auth/logout`
- **Защищённые маршруты** — `/users/me`, `/users/` (admin only)

### Тестовые учётные данные
| Username | Password | Role  |
|----------|----------|-------|
| alice    | alice123 | admin |
| bob      | bob456   | user  |
    """,
    version="1.0.0",
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/", tags=["root"])
def root():
    return {
        "app": settings.APP_NAME,
        "docs": "/docs",
        "redoc": "/redoc",
    }
