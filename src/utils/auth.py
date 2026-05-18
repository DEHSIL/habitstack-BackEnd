from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, Cookie
from settings import settings  # Добавили src. для абсолютного импорта

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 1. Генерация токена (Чистая функция, никаких запросов к БД внутри!)
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 2. Базовая верификация токена и извлечение Payload
def verify_token(access_token: Annotated[str | None, Cookie()] = None) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Недействительный или истекший токен",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    # Если кука пустая
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизованы")
        
    try:
        # Декодируем токен
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return payload  # Возвращаем весь словарь (там лежит sub, role и exp)
    except JWTError:
        raise credentials_exception

# 3. Зависимость для обычного пользователя (возвращает username)
def get_current_user(payload: dict = Depends(verify_token)) -> str:
    return payload.get("sub")

# 4. ЗАВИСИМОСТЬ ДЛЯ АДМИНА (Проверяет роль внутри JWT)
def get_current_admin_user(payload: dict = Depends(verify_token)) -> str:
    user_role = payload.get("role")
    
    # Строгая проверка роли. Если не "admin" -> 403 Forbidden
    if user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Доступ запрещен. Требуются права администратора"
        )
        
    return payload.get("sub")