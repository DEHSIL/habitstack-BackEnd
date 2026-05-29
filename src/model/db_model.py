from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.utils.utils import time_now
from typing import List, Optional
from src.utils.db import Base
from datetime import datetime
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    JSON
)
import uuid


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


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))
    prize_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("prizes.id", ondelete="SET NULL"), nullable=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Храним массивы строк как JSON для универсальности
    habit_days: Mapped[list] = mapped_column(JSON, default=list) 
    every_some_time: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    habit_type: Mapped[str] = mapped_column(String, default='good')      # 'good' | 'bad'
    habit_level: Mapped[str] = mapped_column(String, default='medium')   # 'low' | 'medium' | 'high'
    habit_time: Mapped[str] = mapped_column(String, default='allday')    # 'allday' | 'morning' | 'day' | 'evening' | 'night'

    streak: Mapped[int] = mapped_column(Integer, default=0)
    last_success_date: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Можно и Date, но если на фронте YYYY-MM-DD, String безопаснее

    active: Mapped[bool] = mapped_column(Boolean, default=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    color: Mapped[str] = mapped_column(String)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=time_now, onupdate=time_now)

    # Связи
    user: Mapped["User"] = relationship(back_populates="habits")
    prize: Mapped[Optional["Prize"]] = relationship()
    logs: Mapped[List["HabitLog"]] = relationship(back_populates="habit", cascade="all, delete-orphan")


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    habit_id: Mapped[str] = mapped_column(String, ForeignKey("habits.id", ondelete="CASCADE"))

    date: Mapped[str] = mapped_column(String) # YYYY-MM-DD
    status: Mapped[str] = mapped_column(String) # 'success' | 'fail' | 'skip'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)

    # Связи
    habit: Mapped["Habit"] = relationship(back_populates="logs")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))
    project_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    prize_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("prizes.id", ondelete="SET NULL"), nullable=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    # Фронтенд прислал habit_id как массив string[]. Сохраняем как JSON.
    habit_id: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    task_term: Mapped[str] = mapped_column(String, default='single') # 'single' | 'short' | 'medium' | 'long'
    task_level: Mapped[str] = mapped_column(String, default='medium') # 'low' | 'medium' | 'high'
    task_time: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    status: Mapped[str] = mapped_column(String, default='created') # 'created' | 'process' | 'completed'
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    expired: Mapped[bool] = mapped_column(Boolean, default=False)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=time_now, onupdate=time_now)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    color: Mapped[str] = mapped_column(String)

    # Связи
    user: Mapped["User"] = relationship(back_populates="tasks")
    project: Mapped[Optional["Project"]] = relationship(back_populates="tasks")
    prize: Mapped[Optional["Prize"]] = relationship()


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))
    prize_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("prizes.id", ondelete="SET NULL"), nullable=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True, default=list)
    due_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    project_term: Mapped[str] = mapped_column(String) # 'short' | 'medium' | 'long'
    project_level: Mapped[str] = mapped_column(String, default='medium') # 'low' | 'medium' | 'high'
    color: Mapped[str] = mapped_column(String)
    
    create_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=time_now, onupdate=time_now)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    status: Mapped[str] = mapped_column(String, default='proccess') # 'proccess' | 'completed'
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    expired: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связи
    user: Mapped["User"] = relationship(back_populates="projects")
    prize: Mapped[Optional["Prize"]] = relationship()
    # Задачи, привязанные к этому проекту (вместо tasks_id на фронтенде)
    tasks: Mapped[List["Task"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Prize(Base):
    __tablename__ = "prizes"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    level: Mapped[str] = mapped_column(String, default='medium') # 'low' | 'medium' | 'high'
    color: Mapped[str] = mapped_column(String)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    single: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=time_now, onupdate=time_now)

    # Связи
    user: Mapped["User"] = relationship(back_populates="prizes")


class Diary(Base):
    __tablename__ = "diaries"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Исправил опечатку descriprion с фронта
    emotion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    events: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    
    due_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)
    update_at: Mapped[datetime] = mapped_column(DateTime, default=time_now, onupdate=time_now)

    # Связи
    user: Mapped["User"] = relationship(back_populates="diaries")