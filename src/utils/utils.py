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

def time_now():
    return datetime.now()
