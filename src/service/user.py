from fastapi import UploadFile

from src.model.user import User
from src.utils.utils import hash_password
from src.schemas.user import UserCreate, UserOut, UserUpdate
from src.data.user import UserData
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.R2 import storage

class UserService:
    @staticmethod
    async def get_all(
        db: AsyncSession
    ) -> list[UserOut]:
        return await UserData.get_all(db)
        
        
    @staticmethod
    async def get_one(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.get_one(user_id, db)
        

    @staticmethod
    async def create_user(
        payload: UserCreate,
        avatar: UploadFile,
        db: AsyncSession,
    ) -> UserOut:
        avatar_url = None

        if avatar:
            # Формируем уникальный путь: avatars/timestamp_filename
            from datetime import datetime
            file_path = f"avatars/{datetime.now().timestamp()}_{avatar.filename}"
            
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
        

    @staticmethod
    async def modify_user(
        data: UserUpdate, 
        db: AsyncSession) -> UserOut:
        return await UserData.modify_user(data, db)
    

    @staticmethod
    async def delete_user(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.delete_user(user_id, db)
    
    @staticmethod
    async def deactivate_user(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.deactivate_user(user_id, db)
    

    