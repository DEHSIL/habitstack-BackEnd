from src.schemas.user import PaginatedResponse, UserOut, UserOutBody, UserUpdate
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.auth import get_current_user
from src.service.user import UserService
from src.model.db_model import User
from src.utils.error import Missing
from src.utils.db import get_db
from typing import Optional

router = APIRouter(
    prefix='/user',
    tags=['User'],
)


@router.get('/pag', response_model=PaginatedResponse[UserOutBody])
@router.get('/pag/', response_model=PaginatedResponse[UserOutBody])
async def get_pag(
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Элементов на странице"),
    db: AsyncSession = Depends(get_db)
) -> list[UserOutBody]:
    try:
        return await UserService.get_users_paginated(db, page, size)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    

@router.get('/pagsearch', response_model=PaginatedResponse[UserOutBody])
@router.get('/pagsearch/', response_model=PaginatedResponse[UserOutBody])
async def get_pag(
    search: Optional[str] = Query(None, description="Поиск по имени, фамилии, email или ID"),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Элементов на странице"),
    db: AsyncSession = Depends(get_db)
) -> dict: # Исправили тип с list на PaginatedResponse
    print(search)
    try:
        return await UserService.get_users_paginated(db, page, size, search)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg) # Исправили 'datail' на 'detail'


@router.get('/getall', response_model=list[UserOutBody])
@router.get('/getall/', response_model=list[UserOutBody])
async def get_all(
    db: AsyncSession = Depends(get_db)
) -> list[UserOutBody]:
    try:
        return await UserService.get_all(db)
    except Missing as exc:
        raise HTTPException(status_code=404, datail=exc.msg)


@router.get('/byname/{name}', response_model=UserOut, response_model_exclude_none=True)
@router.get('/byname/{name}/', response_model=UserOut, response_model_exclude_none=True)
# Убрать в админа
async def get_by_name(
    name: str, 
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    try:
        return await UserService.get_by_name(name, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


#Проверять есть ли айдишник внутри
@router.patch('/modify', status_code=200, response_model=UserOut, response_model_exclude_none=True)
@router.patch('/modify/', status_code=200, response_model=UserOut, response_model_exclude_none=True)
async def modify_user(
    form_data: UserUpdate = Depends(UserService.get_user_payload), # Вот тут происходит магия
    avatar: Optional[UploadFile] = File(None), 
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
) -> UserOut:
    try:
        return await UserService.modify_user(form_data, avatar, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)