from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Worldbuilding(Base):
    __tablename__ = "worldbuilding"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novel.id"), nullable=True)
    title = Column(String(255), default="")
    genre = Column(String(100), default="")
    description = Column(Text, default="")
    setting = Column(Text, default="")
    rules = Column(Text, default="")
    summary = Column(Text, default="")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    novel = relationship("Novel", back_populates="worldbuilding_entries")
    characters = relationship("Character", back_populates="worldbuilding", cascade="all, delete-orphan")
    outlines = relationship("Outline", back_populates="worldbuilding", cascade="all, delete-orphan")


class WorldbuildingCreate(BaseModel):
    novel_id: int
    title: str = ""
    genre: str = ""
    description: str = ""
    setting: str = ""
    rules: str = ""


class WorldbuildingUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    setting: Optional[str] = None
    rules: Optional[str] = None
    summary: Optional[str] = None


class WorldbuildingResponse(BaseModel):
    id: int
    novel_id: int
    title: str
    genre: str
    description: str
    setting: str
    rules: str
    summary: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
