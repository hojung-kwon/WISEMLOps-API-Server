from typing import List, Dict, Optional

from pydantic import BaseModel


class NodeDataToolbar(BaseModel):
    position: str


class NodeDataAttribute(BaseModel):
    inputParams: str
    outputParams: str
    args: str
    command: str
    image: str


class NodeData(BaseModel):
    toolbar: NodeDataToolbar
    attribute: NodeDataAttribute


class NodePosition(BaseModel):
    x: float
    y: float


class NodeInfo(BaseModel):
    type: str
    data: NodeData
    events: Dict
    id: str
    label: str
    position: NodePosition


class EdgeData(BaseModel):
    text: str


class EdgeInfo(BaseModel):
    sourceHandle: str
    targetHandle: str
    type: str
    source: str
    target: str
    data: EdgeData
    events: Dict
    id: str
    markerEnd: str
    sourceX: float
    sourceY: float
    targetX: float
    targetY: float


class PipelineInfo(BaseModel):
    pipeline_name: Optional[str] = None
    pipeline_description: Optional[str] = None
    nodes: List[NodeInfo]
    edges: List[EdgeInfo]
    position: List[float]
    zoom: int
