from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel


class Pipeline(BaseModel):
    pipeline_id: str
    pipeline_name: str
    pipeline_description: Optional[str] = None
    version_name: Optional[str] = None
    version_description: Optional[str] = None
    nodes: List[Dict]
    edges: List[Dict]
    position: List[float]
    zoom: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
