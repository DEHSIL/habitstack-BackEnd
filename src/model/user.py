from sqlalchemy import Column, Integer, String
from src.utils.db import Base
import uuid

from sqlalchemy import (
    String,
    Boolean,
    Integer,
    DateTime
)

from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, UTC



class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    name: Mapped[str] = mapped_column(String(255))
    surname: Mapped[str] = mapped_column(String(255))

    passwordHash: Mapped[str] = mapped_column(String)

    avatarUrl: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String,
        unique=True,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String,
        default='free'
    )

    theme: Mapped[str] = mapped_column(
        String,
        default='system'
    )

    streak: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    points: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    color: Mapped[str] = mapped_column(String)

    createAt: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow()
    )

    updatedAt: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    deactivatedAt: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )