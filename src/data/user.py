from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.model.user import User
from src.utils.utils import time_now

class UserData:
    @staticmethod
    async def get_one_by_id(id: str, db: AsyncSession):
        result = await db.execute(
            select(User).where(
                User.id == id
            )
        )
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user
    

    @staticmethod
    async def get_by_name(name: str, db: AsyncSession):
        result = await db.execute(
            select(User).where(
                User.name == name
            )
        )
        users = result.scalars().all()
        if not users:
            raise HTTPException(
                status_code=404,
                detail="Users not found"
            )
        return users
    

    @staticmethod
    async def get_all(db: AsyncSession):
        result = await db.execute(
            select(User)
        )
        users = result.scalars().all()
        if not users:
            raise HTTPException(
                status_code=404,
                detail="No users"
            )
        return users
    

    @staticmethod
    async def create_user(user_data, db:AsyncSession):
        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)

        return user_data
    
    
    @staticmethod
    async def delete_user(user_id, db:AsyncSession):
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
            "message": f"User:({user_id}) deleted"
        }
    

    @staticmethod
    async def update_user(user_id:str, user_data, db:AsyncSession):
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
        

        update_data = user_data.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(user, key, value)
        user.updatedAt = time_now

        db.add(user_data)
        await db.commit()
        await db.refresh(user_data)

        return user_data
    
    
    @staticmethod
    async def deactivate_user(user_id:str, db:AsyncSession):
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
        user.deactivatedAt = time_now

        await db.commit()
        await db.refresh(user)

        return user
