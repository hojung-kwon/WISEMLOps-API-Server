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


class Date(BaseModel):
    year: str
    month: str
    day: str


class DagInfo(BaseModel):
    dag_id: str = ""
    description: str = ""
    schedule: str = ""
    start_date: Date = None
    end_date: str = ""
    retries: str = "1"
    retry_delay: str = ""
    owner: str = ""
    depends_on_past: str = ""
    queue: str = ""
    pool: str = ""
    priority_weight: str = ""
    template_undefined: str = ""
    user_defined_filters: str = ""
    params: str = ""
    tags: List[str] = list()
    max_active_runs: str = ""
    dagrun_timeout: str = ""
    sla_miss_callback: str = ""
    default_view: str = ""
    orientation: str = ""
    catchup: str = ""
    on_failure_callback: str = ""
    is_paused_upon_creation: str = ""
    render_template_as_native_obj: str = ""
    owner_links: str = ""
