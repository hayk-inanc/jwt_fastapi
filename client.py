
import requests

BASE_URL = "http://127.0.0.1:8000"


def register(username: str, password: str, email: str) -> dict:
    """Зарегистрировать нового пользователя."""
    r = requests.post(f"{BASE_URL}/auth/register", json={
        "username": username,
        "password": password,
        "email": email,
    })
    return r.json()


def login(username: str, password: str) -> dict:
    """Войти. Возвращает словарь с access_token и refresh_token."""
    r = requests.post(f"{BASE_URL}/auth/login", data={
        "username": username,
        "password": password,
    })
    return r.json()


def refresh(refresh_token: str) -> dict:
    """Получить новый access_token по refresh_token."""
    r = requests.post(f"{BASE_URL}/auth/refresh", json={
        "refresh_token": refresh_token,
    })
    return r.json()


def logout(access_token: str) -> dict:
    """Выйти из системы."""
    r = requests.post(f"{BASE_URL}/auth/logout", headers={
        "Authorization": f"Bearer {access_token}",
    })
    return r.json()


def get_me(access_token: str) -> dict:
    """Получить профиль текущего пользователя."""
    r = requests.get(f"{BASE_URL}/users/me", headers={
        "Authorization": f"Bearer {access_token}",
    })
    return r.json()


def get_users(access_token: str) -> list:
    """Получить список всех пользователей (только для admin)."""
    r = requests.get(f"{BASE_URL}/users/", headers={
        "Authorization": f"Bearer {access_token}",
    })
    return r.json()


def get_user(access_token: str, username: str) -> dict:
    """Получить пользователя по username (только для admin)."""
    r = requests.get(f"{BASE_URL}/users/{username}", headers={
        "Authorization": f"Bearer {access_token}",
    })
    return r.json()


if __name__ == "__main__":
    # Регистрация
    print(register("charlie", "charlie789", "charlie@example.com"))

    # Логин
    tokens = login("alice", "alice123")
    access  = tokens["access_token"]
    refresh_tok = tokens["refresh_token"]

    # Профиль
    print(get_me(access))

    # Список пользователей (alice — admin)
    print(get_users(access))

    # Обновление токена
    new_tokens = refresh(refresh_tok)
    print(new_tokens)

    # Выход
    print(logout(access))
