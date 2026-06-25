from datetime import datetime
from typing import Optional
import json
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base


class LLMCallLog(Base):
    __tablename__ = "llm_call_log"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    llm_url = Column(String(500), nullable=False)
    status = Column(String(20), default="pending")
    request_payload = Column(Text, nullable=True)
    response_content = Column(Text, nullable=True)
    prompt_tokens = Column(Integer, nullable=True)
    completion_tokens = Column(Integer, nullable=True)
    total_tokens = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class LLMCallLogResponse(BaseModel):
    id: int
    module_name: str = Field(serialization_alias="module")
    model: str
    llm_url: str
    status: str
    request_payload: Optional[dict] = Field(None, serialization_alias="request")
    response_content: Optional[str] = Field(None, serialization_alias="response")
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    duration_ms: Optional[int] = None
    error_message: Optional[str] = Field(None, serialization_alias="error")
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("request_payload", mode="before")
    @classmethod
    def parse_request_payload(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return None
        return v
