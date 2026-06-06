from typing import List, Optional
import uuid
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, or_, select
from src.schemas.user import UserCreate, UserUpdate
from src.model.db_model import User
from src.utils.utils import time_now

class UserData:

    @staticmethod
    async def get_paginated_raw(
        db: AsyncSession, 
        offset: int, 
        limit: int
    ) -> tuple[List[User], int]:
        count_query = select(func.count()).select_from(User)
        total_result = await db.execute(count_query)
        total_items = total_result.scalar() or 0

        query = select(User).offset(offset).limit(limit)
        result = await db.execute(query)
        users = result.scalars().all()

        return users, total_items

    @staticmethod
    async def get_paginated_search_raw(
        db: AsyncSession, 
        offset: int, 
        limit: int, 
        search: str
    ) -> tuple[List[User], int]: 
        conditions = []
        search_query = search.strip()
        like_filter = f"%{search_query}%"
        
        conditions.extend([
            User.name.ilike(like_filter),
            User.surname.ilike(like_filter),
            User.email.ilike(like_filter)
        ])
        
        try:
            uuid.UUID(search_query)
            conditions.append(User.id == search_query)
        except ValueError:
            pass

        count_query = select(func.count()).select_from(User).where(or_(*conditions))
        total_result = await db.execute(count_query)
        total_items = total_result.scalar() or 0

        query = (
            select(User)
            .where(or_(*conditions))
            .order_by(User.create_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(query)
        users = result.scalars().all()

        return users, total_items

    @staticmethod
    async def get_user_by_id(
        user_id: str, 
        db: AsyncSession
    ):
        result = await db.execute(
            select(User).where(
                User.id == user_id
            )
        )

        user = result.scalar_one_or_none()

        return user
    

    @staticmethod
    async def get_by_name(
        name: str, 
        db: AsyncSession
    ):
        result = await db.execute(
            select(User).where(
                User.name == name
            )
        )

        users = result.scalars().all()

        return users
    

    @staticmethod
    async def get_by_email(
        email: str, 
        db: AsyncSession
    ):
        result = await db.execute(
            select(User).where(
                User.email == email
            )
        )

        users = result.scalars().one_or_none()

        return users
    

    @staticmethod
    async def get_all(
        db: AsyncSession
    ):
        result = await db.execute(
            select(User)
        )

        users = result.scalars().all()

        return users
    

    @staticmethod
    async def create_user(
        user_data: UserCreate, 
        db:AsyncSession
    ):
        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)

        return {
            "message": f"User {user_data.name} creater",
            "body": user_data
        }
    
    
    @staticmethod
    async def delete_user(
        user_id: str, 
        db:AsyncSession
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
            "message": f"User: {user_id} deleted"
        }
    

    @staticmethod
    async def modify_user(
        user_id: int,  # Передаем id вместо всего объекта сессии, так чище для DAL
        user_data: UserUpdate, 
        db: AsyncSession,
        avatar_url: Optional[str] = None # Принимаем уже готовую строку-ссылку из сервиса
    ) -> User:
        # 1. Ищем пользователя в БД
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        db_user = result.scalar_one_or_none()

        if not db_user:
            return None # На уровне БД лучше возвращать None, а HTTPException вызывать в сервисе

        # 2. Превращаем Pydantic-схему в словарь (только измененные поля)
        update_data = user_data.model_dump(exclude_unset=True)

        # 3. Динамически обновляем текстовые поля модели
        for key, value in update_data.items():
            setattr(db_user, key, value)

        # 4. Если в сервис загрузили аватар, обновляем ссылку в модели БД
        if avatar_url:
            db_user.avatar_url = avatar_url

        # Обновляем дату модификации
        db_user.updated_at = time_now()

        # 5. ИСПРАВЛЕНО: Сохраняем именно модель SQLAlchemy (db_user)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user
        
    
    @staticmethod
    async def deactivate_user(
        user_id:str, 
        db:AsyncSession
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
        user.deactivated_at = time_now()

        await db.commit()
        await db.refresh(user)

        return {
            "message": f"User: {user_id} deactivated"
        }