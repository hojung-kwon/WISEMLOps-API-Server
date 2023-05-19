from typing import Any

from pydantic import BaseModel
from pydantic.schema import datetime
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Metadata(BaseModel):
    name: str
    create_date: datetime
    annotations: dict | None
    labels: dict | None
    api_version: str | None


class APIResponseModel(BaseModel):
    """기본 API 응답 포맷 by AI플랫폼 Restful API 디자인 가이드"""
    code: int = 200000
    message: str = "API response success"
    result: Any
