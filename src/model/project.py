import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.task import Task
from src.model.prize import Prize
from src.model.user import User

from src.utils.db import Base
from src.utils.utils import time_now


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