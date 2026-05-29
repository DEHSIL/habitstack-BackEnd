import uuid
from datetime import datetime
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.habit import Habit

from src.utils.db import Base
from src.utils.utils import time_now


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    habit_id: Mapped[str] = mapped_column(String, ForeignKey("habits.id", ondelete="CASCADE"))

    date: Mapped[str] = mapped_column(String) # YYYY-MM-DD
    status: Mapped[str] = mapped_column(String) # 'success' | 'fail' | 'skip'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=time_now)

    # Связи
    habit: Mapped["Habit"] = relationship(back_populates="logs")

