from typing import Optional, Dict, Any

from pydantic import BaseModel

from src.mlflow_client_module.models import Tag


class ModelVersionInfo(BaseModel):
    name: str
    source: str
    run_id: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    run_link: Optional[str] = None
    description: Optional[str] = None
    await_creation_for: int = 300


class ModelVersionOptions(BaseModel):
    archive_existing_version: bool = False
    description: Optional[str] = None
    tag: Optional[Tag] = None
