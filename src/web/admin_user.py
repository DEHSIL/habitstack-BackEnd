from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.model.user import User
from src.utils.db import get_db
from src.service.user import UserService
from src.schemas.user import UserCreate, UserOut
from src.utils.auth import get_current_admin
from src.utils.error import Duplicate, Missing 

router = APIRouter(
    prefix="/admin/users", 
    tags=["Admin: Users"]
)



@router.post('/create', status_code=201, response_model=UserOut, response_model_exclude_none=True)
@router.post('/create/', status_code=201, response_model=UserOut, response_model_exclude_none=True)
async def create_user(
    form_data: UserCreate = Depends(UserService.get_user_payload), # Вот тут происходит магия
    avatar: Optional[UploadFile] = File(None),       # Файл идет отдельным аргументом
    db: AsyncSession = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.create_user(form_data, avatar, db)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.delete("/{user_id}/delete", response_model=UserOut, response_model_exclude_none=True)
@router.delete("/{user_id}/delete/", response_model=UserOut, response_model_exclude_none=True)
async def admin_delete_user(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.delete_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)


@router.patch("/{user_id}/deactivate", response_model=UserOut, response_model_exclude_none=True)
@router.patch("/{user_id}/deactivate/", response_model=UserOut, response_model_exclude_none=True)
async def admin_deactivate_user(
    user_id: str, 
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.deactivate_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)