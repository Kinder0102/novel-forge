from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base


class ModuleConfigModel(Base):
    __tablename__ = "module_config"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, unique=True, nullable=False)
    api_key = Column(String, nullable=True)
    base_url = Column(String, nullable=True)
    model = Column(String, nullable=True)
    system_prompt = Column(Text, nullable=True)
    user_prompt_template = Column(Text, nullable=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ModuleConfigCreate(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None


class ModuleConfigResponse(BaseModel):
    id: Optional[int] = None
    module_name: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt_template: Optional[str] = None
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
