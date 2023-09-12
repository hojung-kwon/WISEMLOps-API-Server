from typing import Optional, Dict, Any

from pydantic import BaseModel

from src.mlflow_module.models import Tag


class ExperimentInfo(BaseModel):
    name: str
    artifact_location: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


class ExperimentOptions(BaseModel):
    name: str = ""
    tag: Optional[Tag] = None
