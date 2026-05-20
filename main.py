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

from src.model.user import User

from src.schemas.user import (
    UserCreate,
    UserUpdate,
    UserOut
)
 
from src.web import user, admin_user
from src.utils.utils import hash_password
from src.utils.error import Missing

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(admin_user.router)




# CREATE USER
# @app.post(
#     "/users",
#     response_model=UserOut
# )
# async def create_user(
#     name: str = Form(...),
#     surname: str = Form(...),
#     password: str = Form(...),
#     color: str = Form(...),
#     email: Optional[str] = Form(None),
#     avatar: UploadFile = File(None), # Для получения файла
#     db: AsyncSession = Depends(get_db)
# ):
#     avatar_url = None

#     if avatar:
#         # Формируем уникальный путь: avatars/timestamp_filename
#         from datetime import datetime
#         file_path = f"avatars/{datetime.now().timestamp()}_{avatar.filename}"
        
#         # Загружаем в Cloudflare R2
#         avatar_url = await storage.upload_file(avatar, file_path)

#     # Теперь создаем пользователя в БД

#     # print(data)
#     user = User(
#         name=name,
#         surname=surname,

#         password_hash=hash_password(password),

#         avatar_url=avatar_url,
#         email=email,

#         color=color,
#     )
    
#     db.add(user)
#     await db.commit()
#     await db.refresh(user)

#     return user


# GET ALL USERS
# @app.get(
#     "/users",
#     response_model=list[UserOut]
# )
# async def get_users(
#     db: AsyncSession = Depends(get_db)
# ):
#     result = await db.execute(
#         select(User)
#     )

#     return result.scalars().all()


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