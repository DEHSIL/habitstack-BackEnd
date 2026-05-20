from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional, Literal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str

    avatar_url: Optional[str] = None
    email: Optional[EmailStr] = None

    status: Literal['free', 'premium'] = 'free'

    role: Literal['user', 'admin'] = 'user'

    theme: Literal['light', 'dark', 'system'] = 'system'

    streak: int = 0
    points: int = 0

    color: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None

    avatar_url: Optional[str] = None
    email: Optional[EmailStr] = None

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
    points: Optional[int] = None

    color: Optional[str] = None

    active: Optional[bool] = None


class UserOutBody(BaseModel):
    id: str

    name: str
    surname: str

    avatar_url: Optional[str]
    email: Optional[str]

    status: str
    role: str
    theme: str

    streak: int
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
    message: Optional[str]
    body: Optional[UserOutBody]
   
    