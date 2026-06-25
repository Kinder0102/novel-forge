from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True, index=True)
    novel_id = Column(Integer, ForeignKey("novel.id"), nullable=False)
    worldbuilding_id = Column(Integer, ForeignKey("worldbuilding.id"), nullable=False)
    name = Column(String(100), default="")
    role = Column(String(100), default="")
    personality = Column(Text, default="")
    background = Column(Text, default="")
    appearance = Column(Text, default="")
    summary = Column(Text, default="")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    novel = relationship("Novel", back_populates="characters")
    worldbuilding = relationship("Worldbuilding", back_populates="characters")


class CharacterCreate(BaseModel):
    novel_id: int
    worldbuilding_id: int
    name: str = ""
    role: str = ""
    personality: str = ""
    background: str = ""
    appearance: str = ""


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    personality: Optional[str] = None
    background: Optional[str] = None
    appearance: Optional[str] = None
    summary: Optional[str] = None


class CharacterResponse(BaseModel):
    id: int
    novel_id: int
    worldbuilding_id: int
    name: str
    role: str
    personality: str
    background: str
    appearance: str
    summary: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
