from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime
from typing import Generic, TypeVar, List


class UserCreate(BaseModel):
    name: str
    surname: str
    password: str

    avatar_url: Optional[str] = None
    email: EmailStr = None

    status: Literal['free', 'premium'] = 'free'

    role: Literal['user', 'admin'] = 'user'

    theme: Literal['light', 'dark', 'system'] = 'system'

    streak: int = 0
    max_streak: int = 0 
    points: int = 0

    color: str

class UserAdminCreate(BaseModel):
    name: str
    surname: str
    password: str

    avatar_url: Optional[str] = None
    email: EmailStr = None

    status: Literal['free', 'premium'] = 'free'

    role: Literal['user', 'admin'] = 'user'

    theme: Literal['light', 'dark', 'system'] = 'system'

    streak: int = 0
    max_streak: int = 0 
    points: int = 0

    color: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None

    status: Optional[
        Literal['free', 'premium']
    ] = None

    role: Optional[
        Literal['user', 'admin']
    ] = None

    theme: Optional[
        Literal['light', 'dark', 'system']
    ] = None

    streak: Optional[int] = None
    max_streak: Optional[int] = None
    points: Optional[int] = None

    color: Optional[str] = None

    active: Optional[bool] = None


class UserOutBody(BaseModel):
    id: str

    name: str
    surname: str

    avatar_url: Optional[str]
    email: str

    status: str
    role: str
    theme: str

    streak: int
    max_streak: int
    points: int

    color: str

    create_at: datetime
    updated_at: datetime

    active: bool
    deactivated_at: Optional[datetime]

    lastsync_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserOut(BaseModel):
    message: Optional[str] = None

    body: Optional[UserOutBody] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    # Объявляем переменную типа для создания универсальной пагинации
T = TypeVar('T')

class ApiMeta(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    per_page: int
    has_next: bool
    has_prev: bool

# Универсальная схема ответа, которая примет список элементов и мету
class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    meta: ApiMeta