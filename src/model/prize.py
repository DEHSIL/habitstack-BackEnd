import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.model.user import User

from src.utils.db import Base
from src.utils.utils import time_now


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