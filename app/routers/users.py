from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import get_user, USERS_DB
from app.schemas.auth import UserOut

router = APIRouter(prefix="/users", tags=["users"])


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Зависимость: разрешает доступ только пользователям с ролью admin."""
    if current_user["payload"].get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


@router.get("/me", response_model=UserOut)
def read_me(current_user: dict = Depends(get_current_user)):
    """Возвращает профиль текущего аутентифицированного пользователя."""
    user = get_user(current_user["username"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)


@router.get("/", response_model=list[UserOut])
def list_users(_admin: dict = Depends(require_admin)):
    """Только для admins: список всех пользователей."""
    return [UserOut(**u) for u in USERS_DB.values()]


@router.get("/{username}", response_model=UserOut)
def get_user_by_username(username: str, _admin: dict = Depends(require_admin)):
    """Только для admins: получить пользователя по username."""
    user = get_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(**user)
