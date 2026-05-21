"""
Простая in-memory «база данных» пользователей для демонстрации.
В реальном проекте замените на SQLAlchemy
"""
from app.core.security import hash_password

# username -> user dict
USERS_DB: dict[str, dict] = {
    "alice": {
        "username": "alice",
        "hashed_password": hash_password("alice123"),
        "email": "alice@example.com",
        "role": "admin",
        "disabled": False,
    },
    "bob": {
        "username": "bob",
        "hashed_password": hash_password("bob456"),
        "email": "bob@example.com",
        "role": "user",
        "disabled": False,
    },
}


def get_user(username: str) -> dict | None:
    return USERS_DB.get(username)


def create_user(username: str, password: str, email: str, role: str = "user") -> dict:
    user = {
        "username": username,
        "hashed_password": hash_password(password),
        "email": email,
        "role": role,
        "disabled": False,
    }
    USERS_DB[username] = user
    return user
