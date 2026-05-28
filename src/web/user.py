from typing import Optional
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from src.model.user import User
from src.utils.error import Missing, Duplicate
from src.service.user import UserService
from src.schemas.user import PaginatedResponse, UserOut, UserCreate, UserOutBody, UserUpdate
from src.utils.auth import get_current_admin, get_current_user
from src.utils.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

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
        return await UserService.get_pag(db, page, size)
    except Missing as exc:
        raise HTTPException(status_code=404, datail=exc.msg)
    

@router.get('/getall', response_model=list[UserOutBody])
@router.get('/getall/', response_model=list[UserOutBody])
async def get_all(
    db: AsyncSession = Depends(get_db)
) -> list[UserOutBody]:
    try:
        return await UserService.get_all(db)
    except Missing as exc:
        raise HTTPException(status_code=404, datail=exc.msg)


@router.get('/byid/{id}', response_model=UserOut, response_model_exclude_none=True)
@router.get('/byid/{id}/', response_model=UserOut, response_model_exclude_none=True)
# Убрать в админа
async def get_by_id(
    id: str, 
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    try:
        return await UserService.get_by_id(id, db)
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