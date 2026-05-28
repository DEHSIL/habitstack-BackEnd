from typing import Optional
from fastapi import Form, HTTPException, Response, UploadFile
from sqlalchemy import func, select
import settings
from src.model.user import User
from src.utils.utils import hash_password, verify_password
from src.schemas.user import UserCreate, UserLogin, UserOut, UserUpdate
from src.data.user import UserData
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.R2 import storage
from src.utils.auth import create_access_token


class UserService:
    @staticmethod
    async def get_all(
        db: AsyncSession
    ) -> list[UserOut]:
        res = await UserData.get_all(db)
        if not res:
            raise HTTPException(
                status_code=404,
                detail="No users"
            )
        return res
        
    @staticmethod
    async def get_pag(
        db: AsyncSession,
        page: int,
        size:int
    ) -> list[UserOut]:
        # 1. Считаем общее количество пользователей
        count_query = select(func.count()).select_from(User) # Замени User на твою модель
        total_result = await db.execute(count_query)
        total = total_result.scalar() or 0

        # 2. Получаем пользователей для текущей страницы
        offset = (page - 1) * size
        query = select(User).offset(offset).limit(size)
        
        # Если нужен поиск или сортировка, они добавляются сюда:
        # query = query.where(User.username.ilike(f"%{search}%"))

        result = await db.execute(query)
        users = result.scalars().all()

        # Расчет общего количества страниц
        pages = (total + size - 1) // size 

        return {
            "items": users,
            "total": total,
            "page": page,
            "size": size,
            "pages": pages
        }

    @staticmethod
    async def get_by_id(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.get_by_id(user_id, db)
        

    @staticmethod
    async def login(
        payload: UserLogin,
        response: Response,
        db: AsyncSession      
    ):
        user = await UserData.get_by_email(payload.email, db)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Неверный email или пароль"
            )

        # Зашиваем в токен sub (email), id и роль из базы данных
        token_payload = {
            "sub": user.email,
            "id": str(user.id),
            "role": user.role
        }
        
        token = create_access_token(data=token_payload)

        # Записываем JWT в HttpOnly куку
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,  # Включите в продакшене (HTTPS)
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

        return {
            "message": "Успешный вход", 
            "role": user.role,
            "user": user
        }
        

    @staticmethod
    async def create_user(
        payload: UserCreate,
        avatar: UploadFile,
        db: AsyncSession,
    ) -> UserOut:
        existing_user = await UserData.get_by_email(payload.email, db)
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже зарегистрирован"
            )

        avatar_url = None

        if avatar:
            # Формируем уникальный путь: avatars/timestamp_filename
            from src.utils.utils import time_now
            file_path = f"avatars/{time_now().timestamp()}_{avatar.filename}"
            
            # Загружаем в Cloudflare R2
            avatar_url = await storage.upload_file(avatar, file_path)

        # Теперь создаем пользователя в БД

        # print(data)
        user = User(
            name=payload.name,
            surname=payload.surname,

            password_hash=hash_password(payload.password),

            avatar_url=avatar_url,
            email=payload.email,

            color=payload.color,
        )
        new_user = await UserData.create_user(user, db)

        return new_user
        
    
    # сделать отдельное обновление аватарки и все хдругих данных
    @staticmethod
    async def modify_user(
        payload: UserUpdate, 
        avatar: UploadFile,
        db: AsyncSession
    ) -> UserOut:
        
        avatar_url = None

        if avatar:
            # Формируем уникальный путь: avatars/timestamp_filename
            from src.utils.utils import time_now
            file_path = f"avatars/{time_now().timestamp()}_{avatar.filename}"
            
            # Загружаем в Cloudflare R2
            avatar_url = await storage.upload_file(avatar, file_path)

        # Теперь создаем пользователя в БД

        # print(data)
        data = User(
            name=payload.name,
            surname=payload.surname,

            avatar_url=avatar_url,
            email=payload.email,

            color=payload.color,
        )

        return await UserData.modify_user(data, db)
    

    @staticmethod
    async def delete_user(
        user_id: str,
        db: AsyncSession
    ) -> UserOut:
        # Проверять кто сделал запрос на удаление, если юзер, то нужно
        # проверить что его айдишник совпадает и айди запросом
        return await UserData.delete_user(user_id, db)
    

    @staticmethod
    async def deactivate_user(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.deactivate_user(user_id, db)
    

    @staticmethod
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