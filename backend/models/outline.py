from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Outline(Base):
    __tablename__ = "outline"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novel.id"), nullable=False)
    worldbuilding_id = Column(Integer, ForeignKey("worldbuilding.id"), nullable=False)
    title = Column(String(255), default="")
    description = Column(Text, default="")
    summary = Column(Text, default="")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    novel = relationship("Novel", back_populates="outlines")
    worldbuilding = relationship("Worldbuilding", back_populates="outlines")
    chapter_titles = relationship("ChapterTitle", back_populates="outline", cascade="all, delete-orphan")


class ChapterTitle(Base):
    __tablename__ = "chapter_title"

    id = Column(Integer, primary_key=True, index=True)
    outline_id = Column(Integer, ForeignKey("outline.id"), nullable=False)
    title = Column(String(255), default="")
    idx = Column(Float, default=1.0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    outline = relationship("Outline", back_populates="chapter_titles")
    chapter_content = relationship("ChapterContent", back_populates="chapter_title", uselist=False, cascade="all, delete-orphan")
    scenes = relationship("Scene", back_populates="chapter_title", cascade="all, delete-orphan")


class OutlineCreate(BaseModel):
    novel_id: int
    worldbuilding_id: int
    title: str = ""
    description: str = ""
    summary: str = ""


class OutlineUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None


class OutlineResponse(BaseModel):
    id: int
    novel_id: int
    worldbuilding_id: int
    title: str
    description: str
    summary: str
    chapter_titles: list["ChapterTitleResponse"] = []
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ChapterTitleCreate(BaseModel):
    outline_id: int
    title: str = ""
    idx: Optional[float] = None


class ChapterTitleUpdate(BaseModel):
    title: Optional[str] = None
    idx: Optional[float] = None


class ChapterTitleResponse(BaseModel):
    id: int
    outline_id: int
    title: str
    idx: float
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
