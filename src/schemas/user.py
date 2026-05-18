from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    surname: str
    password: str

    avatarUrl: Optional[str] = None
    email: Optional[EmailStr] = None

    status: Literal['free', 'premium', 'admin'] = 'free'

    theme: Literal['light', 'dark', 'system'] = 'system'

    streak: int = 0
    points: int = 0

    color: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None

    avatarUrl: Optional[str] = None
    email: Optional[EmailStr] = None

    status: Optional[
        Literal['free', 'premium', 'admin']
    ] = None

    theme: Optional[
        Literal['light', 'dark', 'system']
    ] = None

    streak: Optional[int] = None
    points: Optional[int] = None

    color: Optional[str] = None

    active: Optional[bool] = None


class UserOut(BaseModel):
    id: str

    name: str
    surname: str

    avatarUrl: Optional[str]
    email: Optional[str]

    status: str
    theme: str

    streak: int
    points: int

    color: str

    createAt: datetime
    updatedAt: datetime

    active: bool
    deactivatedAt: Optional[datetime]

    class Config:
        from_attributes = True