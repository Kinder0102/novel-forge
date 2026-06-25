from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class GenerateChapterRequest(BaseModel):
    novel_id: int
    worldbuilding_id: int
    chapter_title_id: int
    chapter_id: Optional[int] = None
    description: str = ""


class ChapterContent(Base):
    __tablename__ = "chapter_content"

    id = Column(Integer, primary_key=True, index=True)
    chapter_title_id = Column(Integer, ForeignKey("chapter_title.id"), unique=True, nullable=False)
    content = Column(Text, default="")
    summary = Column(Text, default="")
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    chapter_title = relationship("ChapterTitle", back_populates="chapter_content")


class ChapterContentCreate(BaseModel):
    chapter_title_id: int
    content: str = ""
    summary: str = ""
    status: Optional[str] = None


class ChapterContentUpdate(BaseModel):
    content: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None


class ChapterContentResponse(BaseModel):
    id: int
    chapter_title_id: int
    content: str = ""
    summary: str = ""
    status: str = ""
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
