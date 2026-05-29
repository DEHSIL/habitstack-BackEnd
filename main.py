# main.py
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi import Form, File, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.R2 import storage
from src.utils.db import engine, Base, get_db
from fastapi.middleware.cors import CORSMiddleware
from src.model.model import User

from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserOut
)
 
from src.web import user, admin_user, auth
from src.utils.utils import hash_password
from src.utils.error import Missing

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    response_model_exclude_none=True
)
origins = [
    "http://localhost:3000",  # Твой фронтенд на Next.js
    "http://127.0.0.1:3000",  # На всякий случай локальный IP
]

# Добавляем CORSMiddleware в приложение
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Разрешаем запросы с этих адресов
    allow_credentials=True,           # Разрешаем передачу кук и заголовков авторизации
    allow_methods=["*"],              # Разрешаем все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],              # Разрешаем любые HTTP-заголовки
)
app.include_router(user.router)
app.include_router(admin_user.router)
app.include_router(auth.router)

# GET USER BY ID
@app.get(
    "/users/{user_id}",
    response_model=UserOut
)
async def get_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise Missing(
            status_code=404,
            detail="User not found"
        )

    return user


# UPDATE USER
@app.put(
    "/users/{user_id}",
    response_model=UserOut
)
async def update_user(
    user_id: str,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(user, key, value)

    user.updatedAt = datetime.utcnow()

    await db.commit()
    await db.refresh(user)

    return user


# DELETE USER
@app.delete("/users/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()

    return {
        "message": "User deleted"
    }


# DEACTIVATE USER

# Дать доступ только админам !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@app.patch(
    "/users/{user_id}/deactivate",
    response_model=UserOut
)
async def deactivate_user(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.active = False
    user.deactivatedAt = datetime.utcnow()

    await db.commit()
    await db.refresh(user)

    return user


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app" , reload=True, port=8000, host='0.0.0.0')