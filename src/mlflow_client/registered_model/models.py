from typing import Optional, Dict, Any

from pydantic import BaseModel

from src.mlflow_client.models import Tag


class RegisteredModelInfo(BaseModel):
    name: str
    tags: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class RegisteredModelOptions(BaseModel):
    name: str = ""
    alias: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[Tag] = None
