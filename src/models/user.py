import datetime
import enum
from typing import List
from base import Base

from sqlalchemy import String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy import func

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .post import Post


class UserRole(str, enum.Enum):
    user="user"
    moderator="moderator"
    banned="banned"
    deleted="deleted"

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    firstName: Mapped[str] = mapped_column(String(32), nullable=False)
    lastName: Mapped[str] = mapped_column(String(32), nullable=False)

    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default="user")

    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    posts: Mapped[List[Post]] = relationship(back_populates="author", cascade="all, delete-orphan")

