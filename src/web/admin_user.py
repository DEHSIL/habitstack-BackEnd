from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.service.user import UserService
from src.schemas.user import UserOut

# Предположим, у вас есть зависимость для проверки роли админа
from src.utils.auth import get_current_admin_user 

router = APIRouter(
    prefix="/admin/users", 
    tags=["Admin: Users"]
)

@router.delete("/{user_id}", response_model=UserOut)
async def admin_delete_user(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin_user) # Защита: сюда пройдут ТОЛЬКО админы
):
    # Если зависимость выше сработала, значит это точно админ. Вызываем общий сервис.
    return await UserService.delete_user(user_id, db)