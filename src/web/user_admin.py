from src.schemas.user import PaginatedResponse, UserCreate, UserOut, UserOutBody
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.error import Duplicate, Missing 
from src.utils.auth import get_current_admin
from src.service.user import UserService
from src.model.db_model import User
from src.utils.db import get_db
from typing import Optional

router = APIRouter(
    prefix="/admin/users", 
    tags=["Admin: Users"]
)


@router.post('/create', status_code=201, response_model=UserOut, response_model_exclude_none=True)
@router.post('/create/', status_code=201, response_model=UserOut, response_model_exclude_none=True)
async def admin_create_user(
    form_data: UserCreate = Depends(UserService.get_admin_user_payload),
    avatar: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    # current_admin: User = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.create_user(form_data, avatar, db)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.delete("/delete/{user_id}", response_model=UserOut, response_model_exclude_none=True)
@router.delete("/delete/{user_id}/", response_model=UserOut, response_model_exclude_none=True)
async def admin_delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.delete_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)


@router.patch("/deactivate/{user_id}", response_model=UserOut, response_model_exclude_none=True)
@router.patch("/deactivate/{user_id}/", response_model=UserOut, response_model_exclude_none=True)
async def admin_deactivate_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.deactivate_user(user_id, db)
    except Missing as ecx:
        raise HTTPException(status_code=408, detail=ecx.msg)
    

@router.get('/byid/{id}', response_model=UserOut, response_model_exclude_none=True)
@router.get('/byid/{id}/', response_model=UserOut, response_model_exclude_none=True)
async def admin_get_by_id(
    id: str,
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.get_by_id(id, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    

@router.get('/byname/{name}', response_model=UserOut, response_model_exclude_none=True)
@router.get('/byname/{name}/', response_model=UserOut, response_model_exclude_none=True)
async def admin_get_by_name(
    name: str, 
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.get_by_name(name, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    

@router.get('/byemail/{email}', response_model=UserOut, response_model_exclude_none=True)
@router.get('/byemail/{email}/', response_model=UserOut, response_model_exclude_none=True)
async def admin_get_by_email(
    email: str, 
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> UserOut:
    try:
        return await UserService.get_by_email(email, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    
    
# Нужен ли он вообще???????????
@router.get('/getall', response_model=list[UserOutBody])
@router.get('/getall/', response_model=list[UserOutBody])
async def admin_get_all(
    db: AsyncSession = Depends(get_db),
    current_admin = Depends(get_current_admin)
) -> list[UserOutBody]:
    try:
        return await UserService.get_all(db)
    except Missing as exc:
        raise HTTPException(status_code=404, datail=exc.msg)