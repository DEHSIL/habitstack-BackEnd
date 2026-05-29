import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.prize import Prize
from src.model.project import Project
from src.model.user import User

from src.utils.db import Base
from src.utils.utils import time_now


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