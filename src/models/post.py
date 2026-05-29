from datetime import datetime
from .base import Base

from sqlalchemy import String, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy import func, ForeignKey, Text

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enums import PostStatus


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    author_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    # Using Python Enum for type-safe status
    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(PostStatus),
        default=PostStatus.draft
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # Relationship with the author (Many-to-One)
    author: Mapped["User"] = relationship(back_populates="posts")

    # Relationship with tags (Many-to-Many via post_tags)
    # tags: Mapped[List["Tag"]] = relationship(
    #     secondary="post_tags", 
    #     back_populates="posts"
    # )
