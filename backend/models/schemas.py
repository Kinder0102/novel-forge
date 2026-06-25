from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database import Base


# ── SQLAlchemy Models ──────────────────────────────────────

class Worldbuilding(Base):
    __tablename__ = "worldbuilding"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), default="")
    genre = Column(String(100), default="")
    description = Column(Text, default="")
    setting = Column(Text, default="")
    rules = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    characters = relationship("Character", back_populates="worldbuilding", cascade="all, delete-orphan")
    outlines = relationship("Outline", back_populates="worldbuilding", cascade="all, delete-orphan")


class Character(Base):
    __tablename__ = "character"

    id = Column(Integer, primary_key=True, index=True)
    worldbuilding_id = Column(Integer, ForeignKey("worldbuilding.id"), nullable=False)
    name = Column(String(100), default="")
    role = Column(String(100), default="")
    personality = Column(Text, default="")
    background = Column(Text, default="")
    appearance = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    worldbuilding = relationship("Worldbuilding", back_populates="characters")


class Outline(Base):
    __tablename__ = "outline"

    id = Column(Integer, primary_key=True, index=True)
    worldbuilding_id = Column(Integer, ForeignKey("worldbuilding.id"), nullable=False)
    title = Column(String(255), default="")
    summary = Column(Text, default="")
    chapters_json = Column(Text, default="[]")  # JSON array of {title, summary}
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    worldbuilding = relationship("Worldbuilding", back_populates="outlines")
    chapter_contents = relationship("ChapterContent", back_populates="outline", cascade="all, delete-orphan")


class Scene(Base):
    __tablename__ = "scene"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("outline.id"), nullable=False)
    scene_number = Column(Integer, default=0)
    title = Column(String(255), default="")
    summary = Column(Text, default="")
    content = Column(Text, nullable=True)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChapterContent(Base):
    __tablename__ = "chapter_content"

    id = Column(Integer, primary_key=True, index=True)
    outline_id = Column(Integer, ForeignKey("outline.id"), nullable=False)
    chapter_index = Column(Integer, default=0)
    title = Column(String(255), default="")
    content = Column(Text, default="")
    status = Column(String(20), default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    outline = relationship("Outline", back_populates="chapter_contents")


class ModuleConfigModel(Base):
    __tablename__ = "module_config"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, unique=True, nullable=False)
    api_key = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    model = Column(String, nullable=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


# ── Pydantic Schemas ───────────────────────────────────────

# --- Worldbuilding ---
class WorldbuildingCreate(BaseModel):
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


class WorldbuildingResponse(BaseModel):
    id: int
    title: str
    genre: str
    description: str
    setting: str
    rules: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Character ---
class CharacterCreate(BaseModel):
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


class CharacterResponse(BaseModel):
    id: int
    worldbuilding_id: int
    name: str
    role: str
    personality: str
    background: str
    appearance: str
    created_at: datetime

    model_config = {"from_attributes": True}


# --- Outline ---
class OutlineCreate(BaseModel):
    worldbuilding_id: int
    title: str = ""
    summary: str = ""
    chapters_json: str = "[]"


class OutlineUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    chapters_json: Optional[str] = None


class OutlineResponse(BaseModel):
    id: int
    worldbuilding_id: int
    title: str
    summary: str
    chapters_json: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- Scene ---
class SceneCreate(BaseModel):
    outline_id: int
    chapter_index: int
    scene_number: int
    title: str = ""
    summary: str = ""


class SceneUpdate(BaseModel):
    scene_number: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class SceneResponse(BaseModel):
    id: int
    chapter_id: int
    scene_number: int
    title: str
    summary: str
    content: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- ChapterContent ---
class ChapterContentCreate(BaseModel):
    outline_id: int
    chapter_index: int
    title: str = ""
    content: str = ""


class ChapterContentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None


class ChapterContentResponse(BaseModel):
    id: int
    outline_id: int
    chapter_index: int
    title: str
    content: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# --- ModuleConfig ---
class ModuleConfigCreate(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None


class ModuleConfigResponse(BaseModel):
    id: Optional[int] = None
    module_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
