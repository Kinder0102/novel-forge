from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship
from database import Base


class Novel(Base):
    __tablename__ = "novel"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="draft")
    writing_style = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    worldbuilding_entries = relationship("Worldbuilding", back_populates="novel", cascade="all, delete-orphan")
    characters = relationship("Character", back_populates="novel", cascade="all, delete-orphan")
    outlines = relationship("Outline", back_populates="novel", cascade="all, delete-orphan")


class NovelCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "draft"
    create_worldbuilding: bool = False


class NovelUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    writing_style: Optional[str] = None


class NovelResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    writing_style: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
