from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.user import UserCreate, UserUpdate
from src.model.user import User
from src.utils.utils import time_now

class UserData:
    @staticmethod
    async def get_by_id(
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

        users = result.scalars().all()

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
        user_data: UserUpdate, 
        db:AsyncSession
    ):
        result = await db.execute(
            select(User).where(
                User.id == user_data.id
            )
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        update_data = user_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(user, key, value)
        user.updated_at = time_now()

        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)

        return {
            "message": "User updated",
            "body": user_data
        }
    
    
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