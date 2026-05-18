from src.schemas.user import UserCreate, UserOut, UserUpdate
import src.data.user as user_data
from sqlalchemy.ext.asyncio import AsyncSession


class UserService:
    @staticmethod
    async def get_all(
        db: AsyncSession
    ) -> list[UserOut]:
        return await user_data.get_all()
        
        
    @staticmethod
    async def get_one(
        id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await user_data.get_one(id)
        

    @staticmethod
    async def create_user(
        payload: UserCreate,
        db: AsyncSession,
    ) -> UserOut:
        data = {payload}

        new_user = await user_data.create_user(data, db)

        return new_user
        

    @staticmethod
    async def modify_user(
        data: UserUpdate, 
        db: AsyncSession) -> UserOut:
        return await user_data.modify_user(data, db)
    

    @staticmethod
    async def delete_user(
        id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await user_data.delete_user(id, db)
    

    