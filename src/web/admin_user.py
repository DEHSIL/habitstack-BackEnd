from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.db import get_db
from src.service.user import UserService
from src.schemas.user import UserOut

# Предположим, у вас есть зависимость для проверки роли админа
from src.utils.auth import get_current_admin_user
from src.utils.error import Missing 

router = APIRouter(
    prefix="/admin/users", 
    tags=["Admin: Users"]
)

@router.delete("/{user_id}/delete")
@router.delete("/{user_id}/delete/")
async def admin_delete_user(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    # current_admin = Depends(get_current_admin_user)
) -> UserOut:
    try:
        return await UserService.delete_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)


@router.patch("/{user_id}/deactivate", response_model=UserOut)
@router.patch("/{user_id}/deactivate/", response_model=UserOut)
async def admin_deactivate_user(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    # current_admin = Depends(get_current_admin_user)
) -> UserOut:
    try:
        return await UserService.deactivate_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)