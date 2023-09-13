from typing import Optional, Dict, List

from pydantic import BaseModel


class PipelineDto(BaseModel):
    pipeline_name: str
    pipeline_description: Optional[str] = None
    version_info: Optional[Dict] = None
    nodes: List[Dict]
    edges: List[Dict]
    position: List[float]
    zoom: int
