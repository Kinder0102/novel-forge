from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Float, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Scene(Base):
    __tablename__ = "scene"

    id = Column(Integer, primary_key=True, index=True)
    chapter_title_id = Column(Integer, ForeignKey("chapter_title.id"), nullable=False)
    scene_number = Column(Float, default=1.0)
    title = Column(String(255), default="")
    description = Column(Text, default="")
    summary = Column(Text, default="")
    content = Column(Text, nullable=True)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    chapter_title = relationship("ChapterTitle", back_populates="scenes")


class SceneCreate(BaseModel):
    chapter_title_id: int
    scene_number: float = 1.0
    title: str = ""
    description: str = ""
    summary: str = ""


class SceneUpdate(BaseModel):
    scene_number: Optional[float] = None
    title: Optional[str] = None
    description: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class SceneResponse(BaseModel):
    id: int
    chapter_title_id: int
    scene_number: float
    title: str
    description: str
    summary: str
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
