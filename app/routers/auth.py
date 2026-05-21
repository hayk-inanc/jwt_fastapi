from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
)
from app.models.user import get_user, create_user, USERS_DB
from app.schemas.auth import (
    TokenResponse,
    RefreshRequest,
    AccessTokenResponse,
    UserRegister,
    UserOut,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: UserRegister):
    """Регистрация нового пользователя."""
    if get_user(data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{data.username}' already taken",
        )
    user = create_user(data.username, data.password, data.email)
    return UserOut(**user)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Аутентификация через форму (username + password).
    Возвращает access_token и refresh_token.
    """
    user = get_user(form.username)
    if not user or not verify_password(form.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user["disabled"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is disabled")

    token_data = {"sub": user["username"], "role": user["role"]}
    return TokenResponse(
        access_token=create_access_token(token_data),
        refresh_token=create_refresh_token(token_data),
    )


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(body: RefreshRequest):
    """
    Обновление access-токена с помощью refresh-токена.
    Refresh-токен не обновляется (rotation — на ваше усмотрение).
    """
    payload = decode_token(body.refresh_token)

    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type — expected refresh token",
        )

    username = payload.get("sub")
    user = get_user(username) if username else None
    if not user or user["disabled"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or disabled")

    new_access = create_access_token({"sub": username, "role": user["role"]})
    return AccessTokenResponse(access_token=new_access)


@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user)):
    """
    «Выход» — на стороне сервера при stateless JWT ничего не инвалидируется.
    В продакшене здесь нужен blocklist (Redis и т.п.).
    """
    return {"message": f"User '{current_user['username']}' logged out. Please discard your tokens."}
