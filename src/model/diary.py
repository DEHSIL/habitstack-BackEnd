import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.user import User

from src.utils.db import Base
from src.utils.utils import time_now


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