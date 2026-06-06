from typing import Any, Dict, Optional
from fastapi import Form, HTTPException, Response, UploadFile
from settings import settings
from src.model.db_model import User
from src.utils.utils import hash_password, verify_password
from src.schemas.user import UserAdminCreate, UserCreate, UserLogin, UserOut, UserUpdate
from src.data.user import UserData
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.R2 import storage
from src.utils.auth import create_access_token
import math
from sqlalchemy.ext.asyncio import AsyncSession
from src.utils.utils import time_now

class UserService:
    @staticmethod
    async def get_all(
        db: AsyncSession
    ) -> list[UserOut]:
        res = await UserData.get_all(db)

        if not res:
            raise HTTPException(
                status_code=404, 
                detail="No users"
            )
        
        return res
        

    @staticmethod
    async def get_users_paginated(
        db: AsyncSession,
        page: int,
        size: int,
        search: Optional[str] = None
    ) -> Dict[str, Any]:
        offset = (page - 1) * size
        
        if search and search.strip():
            users, total_items = await UserData.get_paginated_search_raw(
                db=db, offset=offset, limit=size, search=search
            )
        else:
            users, total_items = await UserData.get_paginated_raw(
                db=db, offset=offset, limit=size
            )

        if not users:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        total_pages = math.ceil(total_items / size) if total_items > 0 else 1
        has_next = page < total_pages
        has_prev = page > 1

        return {
            "items": users,
            "meta": {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "per_page": size,
                "has_next": has_next,
                "has_prev": has_prev
            }
        }
    

    @staticmethod
    async def get_user_by_id(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        user =  await UserData.get_user_by_id(user_id, db)
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return {"body": user}
        

    @staticmethod
    async def get_by_name(
        name: str, 
        db: AsyncSession
    ) -> UserOut:
        user =  await UserData.get_by_name(name, db)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return {"body": user}
    

    @staticmethod
    async def get_by_email(
        email: str, 
        db: AsyncSession
    ) -> UserOut:
        user =  await UserData.get_by_email(email, db)

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        return {"body": user}
        

    @staticmethod
    async def login(
        payload: UserLogin,
        response: Response,
        db: AsyncSession      
    ):
        user = await UserData.get_by_email(payload.email, db)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail="Неверный email или пароль"
            )

        token_payload = {
            "sub": user.email,
            "id": str(user.id),
            "role": user.role
        }
        token = create_access_token(data=token_payload)
        

        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True, 
            samesite="lax",
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        print(user)
        return {
            "message": "Успешный вход", 
            "role": user.role,
            "user": user
        }
        

    @staticmethod
    async def create_user(
        payload: UserCreate,
        avatar: UploadFile,
        db: AsyncSession,
    ) -> UserOut:
        existing_user = await UserData.get_by_email(payload.email, db)
        
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Пользователь с таким email уже зарегистрирован"
            )

        avatar_url = None

        if avatar:
            
            file_path = f"avatars/{time_now().timestamp()}_{avatar.filename}"
            
            avatar_url = await storage.upload_file(avatar, file_path)


        user = User(
            name=payload.name,
            surname=payload.surname,

            password_hash=hash_password(payload.password),

            avatar_url=avatar_url,
            email=payload.email,

            status=payload.status,
            role=payload.role,
            theme=payload.theme,

            streak=payload.streak,
            max_streak=payload.max_streak,
            points=payload.points, 
            
            color=payload.color,
        )
        new_user = await UserData.create_user(user, db)

        return new_user
        
    
    # сделать отдельное обновление аватарки и все хдругих данных
    @staticmethod
    async def modify_user(
        user_data: UserUpdate, 
        avatar: Optional[UploadFile],
        db: AsyncSession,
        current_user: User
    ):
        avatar_url = None

        # 1. Если прилетел файл — изолированно грузим его в Cloudflare R2
        if avatar:
            from src.utils.utils import time_now
            file_path = f"avatars/{time_now().timestamp()}_{avatar.filename}"
            avatar_url = await storage.upload_file(avatar, file_path)

        # 2. Вызываем метод низкого уровня базы данных для обновления полей
        updated_user = await UserData.modify_user(
            user_id=current_user.id,
            user_data=user_data,
            db=db,
            avatar_url=avatar_url
        )

        # 3. Если на уровне БД что-то пошло не так (юзера удалили в параллельном потоке)
        if not updated_user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # 4. ИСПРАВЛЕНО: Возвращаем сам объект пользователя.
        # FastAPI автоматически пропустит его через вашу response_model=UserOut
        print(f"Пользователь {updated_user} успешно обновлен")

        return {"body":updated_user}
    

    @staticmethod
    async def delete_user(
        user_id: str,
        db: AsyncSession
    ) -> UserOut:
        return await UserData.delete_user(user_id, db)
    

    @staticmethod
    async def deactivate_user(
        user_id: str, 
        db: AsyncSession
    ) -> UserOut:
        return await UserData.deactivate_user(user_id, db)
    


    @staticmethod
    async def get_user_modify_payload(
        name: Optional[str] = Form(None),
        surname: Optional[str] = Form(None),
        color: Optional[str] = Form(None)
    ) -> UserUpdate:
        return UserUpdate(
            name=name,
            surname=surname,
            color=color
        )
    
    @staticmethod
    async def get_user_payload(
        name: str = Form(...),
        surname: str = Form(...),
        password: str = Form(...),
        color: str = Form(...),
        email: Optional[str] = Form(None)
    ) -> UserCreate:
        return UserCreate(
            name=name,
            surname=surname,
            password=password,
            color=color,
            email=email
        ) 
    
    @staticmethod
    async def get_admin_user_payload(
        name: str = Form(...),
        surname: str = Form(...),
        password: str = Form(...),
        color: str = Form(...),
        email: Optional[str] = Form(None),
        status: str = Form(...),
        role: str = Form(...),
        theme: str = Form(...),
        streak: str = Form(...),
        max_streak: str = Form(...),
        points: str = Form(...),
    ) -> UserAdminCreate:
        return UserAdminCreate(
            name=name,
            surname=surname,
            password=password,
            color=color,
            email=email,
            status=status,
            role=role,
            theme=theme,
            streak=streak,
            max_streak=max_streak,
            points=points,
        ) 