import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    JSON
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.habit_log import HabitLog
from src.model.prize import Prize
from src.model.user import User

from src.utils.db import Base
from src.utils.utils import time_now

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

