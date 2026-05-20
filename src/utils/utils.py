from datetime import datetime, timezone
from typing import Optional
from passlib.context import CryptContext
from fastapi import Form
from api.schemas import UserCreate

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

time_now = lambda: datetime.now()


async def get_user_payload(
    name: str = Form(...),
    surname: str = Form(...),
    password: str = Form(...),
    color: str = Form(...),
    email: Optional[str] = Form(None)
) -> UserCreate:
    # FastAPI сам провалидирует поля, а мы просто упаковываем их в модель
    return UserCreate(
        name=name,
        surname=surname,
        password=password,
        color=color,
        email=email
    )