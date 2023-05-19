from typing import Optional, Dict, Any

from pydantic import BaseModel

from src.mlflow_client.models import Tag


class RunInfo(BaseModel):
    experiment_id: str
    start_time: Optional[int] = None
    tags: Optional[Dict[str, Any]] = None
    run_name: Optional[str] = None


class RunOptions(BaseModel):
    name: str = ""
    tag: Optional[Tag] = None
    status: Optional[str] = None
    end_time: Optional[int] = None
