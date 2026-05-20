from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from src.utils.error import Missing, Duplicate
from src.service.user import UserService
from src.schemas.user import UserOut, UserCreate, UserUpdate
from settings import settings
from src.utils.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.utils import get_user_payload

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('', response_model=list[UserOut])
@router.get('/', response_model=list[UserOut])
async def get_all(db: AsyncSession = Depends(get_db)) -> list[UserOut]:
    return await UserService.get_all(db)


@router.get('/{id}', response_model=UserOut)
async def get_one(id: str, db: AsyncSession = Depends(get_db)) -> UserOut:
    try:
        return await UserService.get_one(id, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post('', status_code=201, response_model=UserOut)
@router.post('/', status_code=201, response_model=UserOut)
async def create_user(
    payload: UserCreate = Depends(get_user_payload), # Вот тут происходит магия
    avatar: Optional[UploadFile] = File(None),       # Файл идет отдельным аргументом
    db: AsyncSession = Depends(get_db)
) -> UserOut:
    try:
        return await UserService.create_user(
            payload, avatar, db)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)
    

#Проверять есть ли айдишник внутри
@router.patch('', response_model=UserOut)
@router.patch('/', response_model=UserOut)
async def modify_user(data: UserUpdate, db: AsyncSession = Depends(get_db)) -> UserOut:
    try:
        return await UserService.modify_user(data, db)
    except Missing as exc:
        raise HTTPException(status_code=404, detail=exc.msg)