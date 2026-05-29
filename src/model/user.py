# from sqlalchemy import Integer, String
# from src.utils.db import Base
# import uuid
# from sqlalchemy import (
#     String,
#     Boolean,
#     Integer,
#     DateTime
# )
# from sqlalchemy.orm import Mapped, mapped_column
# from datetime import datetime
# from src.utils.utils import time_now


# class User(Base):
#     __tablename__ = "users"

#     id: Mapped[str] = mapped_column(
#         String,
#         primary_key=True,
#         default=lambda: str(uuid.uuid4())
#     )

#     name: Mapped[str] = mapped_column(String(255))
#     surname: Mapped[str] = mapped_column(String(255))

#     password_hash: Mapped[str] = mapped_column(String)

#     avatar_url: Mapped[str | None] = mapped_column(
#         String,
#         nullable=True
#     )

#     email: Mapped[str | None] = mapped_column(
#         String,
#         unique=True,
#         nullable=True
#     )

#     theme: Mapped[str] = mapped_column(
#         String,
#         default='system'
#     )

#     streak: Mapped[int] = mapped_column(
#         Integer,
#         default=0
#     )

#     max_streak: Mapped[int] = mapped_column(
#         Integer,
#         default=0
#     )

#     points: Mapped[int] = mapped_column(
#         Integer,
#         default=0
#     )

#     color: Mapped[str] = mapped_column(String)

#     status: Mapped[str] = mapped_column(
#         String,
#         default='free'
#     )

#     role: Mapped[str] = mapped_column(
#         String,
#         default='user'
#     )

#     active: Mapped[bool] = mapped_column(
#         Boolean,
#         default=True
#     )

#     updated_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=time_now(),
#         onupdate=time_now()
#     )

#     create_at: Mapped[datetime] = mapped_column(
#         DateTime,
#         default=time_now()
#         )
    
#     deactivated_at: Mapped[datetime | None] = mapped_column(
#         DateTime,
#         nullable=True
#     )

#     lastsync_at: Mapped[datetime | None] = mapped_column(
#         DateTime,
#         nullable=True
#     )



import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.diary import Diary
from src.model.habit import Habit
from src.model.prize import Prize
from src.model.project import Project
from src.model.task import Task

from src.utils.db import Base
from src.utils.utils import time_now


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String(255))
    surname: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String)
    avatar_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    theme: Mapped[str] = mapped_column(String, default='system')
    streak: Mapped[int] = mapped_column(Integer, default=0)
    max_streak: Mapped[int] = mapped_column(Integer, default=0)
    points: Mapped[int] = mapped_column(Integer, default=0)
    color: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default='free')
    role: Mapped[str] = mapped_column(String, default='user')
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Исправлено: передаем функцию, а не результат её вызова
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=time_now,
        onupdate=time_now
    )
    create_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=time_now
    )
    deactivated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    lastsync_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Связи (Relationships)
    habits: Mapped[List["Habit"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    tasks: Mapped[List["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    projects: Mapped[List["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    prizes: Mapped[List["Prize"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    diaries: Mapped[List["Diary"]] = relationship(back_populates="user", cascade="all, delete-orphan")