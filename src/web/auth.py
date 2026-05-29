from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.db import get_db
from src.schemas.user import UserLogin, UserOut
from src.data.user import UserData
from src.model.db_model import User
from src.utils.utils import verify_password, hash_password
from src.utils.auth import create_access_token, get_current_admin, get_current_user
from src.utils.R2 import storage
from src.service.user import UserService
from settings import settings
from src.utils.error import Duplicate

router = APIRouter(
    prefix="/auth", 
    tags=["Authentication"]
)

# 1. РЕГИСТРАЦИЯ (multipart/form-data для поддержки файлов)
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@router.post("/register/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(
    form_data: dict = Depends(UserService.get_user_payload),
    avatar: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        return await UserService.create_user(form_data, avatar, db)
    except Duplicate as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


# 2. ВХОД (Для всех: и юзер, и админ заходят через этот роут)
@router.post("/login")
@router.post("/login/")
async def login(
    login_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    try: 
        return await UserService.login(login_data, response, db)
    except:
        raise HTTPException(
            status_code=401,
            detail=""
        )
    

# 3. ВЫХОД (Очистка кук)
@router.post("/logout")
@router.post("/logout/")
async def logout(response: Response):
    try:
        response.delete_cookie(key="access_token")
        return {"message": "Вы успешно вышли из системы"}
    except:
        raise HTTPException(status_code=0, detail="Logout error")

# 4. ПРОВЕРКА ТЕКУЩЕГО ЮЗЕРА (Доступно любому авторизованному)
@router.get("/me", response_model=UserOut)
@router.get("/me/", response_model=UserOut)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return {"body": current_user}


# 5. ПРОВЕРКА ДОСТУПА АДМИНА (Сюда обычный юзер не попадет — вернет 403)
@router.get("/admin-only")
@router.get("/admin-only/")
async def get_admin_dashboard( current_admin = Depends(get_current_admin)):
    return {
        "message": f"Приветствуем в админ-панели, {current_admin.name}!",
        "secret_admin_data": "Вся власть Советам"
    }