import re
from typing import List, Dict, Optional

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, validator


class Pipeline(BaseModel):
    pipeline_name: str = Field(
        title="pipeline_name",
        description="파이프라인 이름"
    )
    pipeline_package_path: str = Field(
        title="pipeline_package_path",
        description="파이프라인 생성 경로"
    )
    description: Optional[str] = Field(
        title="description",
        description="파이프라인 설명"
    )


class NodeDataToolbar(BaseModel):
    position: str = Field(
        title="position",
        description="파이프라인 노드 툴바 위치 정보"
    )


class NodeDataAttribute(BaseModel):
    inputParams: str = Field(
        title="inputParams",
        description="파이프라인 노드 속성 inputParams"
    )
    outputParams: str = Field(
        title="outputParams",
        description="파이프라인 노드 속성 outputParams"
    )
    args: str = Field(
        title="args",
        description="파이프라인 노드 속성 args"
    )
    command: str = Field(
        title="command",
        description="파이프라인 노드 속성 command"
    )
    image: str = Field(
        title="image",
        description="파이프라인 노드 속성 image"
    )


class NodeData(BaseModel):
    toolbar: NodeDataToolbar = Field(
        title="toolbar",
        description="파이프라인 노드 툴바 정보"
    )
    attribute: Dict = Field(
        title="attribute",
        description="파이프라인 노드 속성 정보"
    )


class NodePosition(BaseModel):
    x: float = Field(
        title="x",
        description="파이프라인 노드 위치 x"
    )
    y: float = Field(
        title="y",
        description="파이프라인 노드 위치 y"
    )


class NodeInfo(BaseModel):
    type: str = Field(
        title="type",
        description="파이프라인 노드 타입"
    )
    data: NodeData = Field(
        title="data",
        description="파이프라인 노드 data"
    )
    events: Dict = Field(
        title="events",
        description="파이프라인 노드 이벤트"
    )
    id: str = Field(
        title="id",
        description="파이프라인 노드 아이디"
    )
    label: str = Field(
        title="label",
        description="파이프라인 노드 라벨"
    )
    position: NodePosition = Field(
        title="position",
        description="파이프라인 노드 위치 정보"
    )


class EdgeData(BaseModel):
    text: str = Field(
        title="text",
        description="파이프라인 엣지 텍스트"
    )


class EdgeInfo(BaseModel):
    sourceHandle: str = Field(
        title="sourceHandle",
        description="파이프라인 엣지 sourceHandle"
    )
    targetHandle: str = Field(
        title="targetHandle",
        description="파이프라인 엣지 targetHandle"
    )
    type: str = Field(
        title="type",
        description="파이프라인 엣지 type"
    )
    source: str = Field(
        title="source",
        description="파이프라인 엣지 source"
    )
    target: str = Field(
        title="target",
        description="파이프라인 엣지 target"
    )
    data: EdgeData = Field(
        title="data",
        description="파이프라인 엣지 data"
    )
    events: Dict = Field(
        title="events",
        description="파이프라인 엣지 events"
    )
    id: str = Field(
        title="id",
        description="파이프라인 엣지 id"
    )
    markerEnd: str = Field(
        title="markerEnd",
        description="파이프라인 엣지 markerEnd"
    )
    sourceX: float = Field(
        title="sourceX",
        description="파이프라인 엣지 sourceX"
    )
    sourceY: float = Field(
        title="sourceY",
        description="파이프라인 엣지 sourceY"
    )
    targetX: float = Field(
        title="targetX",
        description="파이프라인 엣지 targetX"
    )
    targetY: float = Field(
        title="targetY",
        description="파이프라인 엣지 targetY"
    )


class PipelineInfo(BaseModel):
    pipeline_name: Optional[str] = Field(
        title="pipeline_name",
        description="파이프라인 이름"
    )
    pipeline_description: Optional[str] = Field(
        title="pipeline_description",
        description="파이프라인 설명"
    )
    nodes: List[NodeInfo] = Field(
        title="nodes",
        description="파이프라인 노드 정보"
    )
    edges: List[EdgeInfo] = Field(
        title="edges",
        description="파이프라인 엣지 정보"
    )
    position: List[float] = Field(
        title="position",
        description="파이프라인 위치 정보"
    )
    zoom: int = Field(
        title="zoom",
        description="파이프라인 zoom 정보"
    )

    @validator('pipeline_name')
    def check_pipeline_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message=f"Only alphabetic characters, numbers, and underscores are allowed in the pipeline name.",
                result={"current_name": v}
            )
        return v


class Date(BaseModel):
    year: str = Field(
        title="year",
        description="year"
    )
    month: str = Field(
        title="month",
        description="month"
    )
    day: str = Field(
        title="day",
        description="day"
    )


class DagInfo(BaseModel):
    dag_id: str = Field(
        title="dag_id",
        description="dag dag_id"
    )
    description: str = Field(
        title="description",
        description="dag description"
    )
    schedule: str = Field(
        title="schedule",
        description="dag schedule"
    )
    start_date: Date = Field(
        title="start_date",
        description="dag start_date"
    )
    end_date: str = Field(
        title="end_date",
        description="dag end_date"
    )
    retries: str = Field(
        title="retries",
        description="dag retries"
    )
    retry_delay: str = Field(
        title="retry_delay",
        description="dag retry_delay"
    )
    owner: str = Field(
        title="owner",
        description="dag owner"
    )
    depends_on_past: str = Field(
        title="depends_on_past",
        description="dag depends_on_past"
    )
    queue: str = Field(
        title="queue",
        description="dag queue"
    )
    pool: str = Field(
        title="pool",
        description="dag pool"
    )
    priority_weight: str = Field(
        title="priority_weight",
        description="dag priority_weight"
    )
    template_undefined: str = Field(
        title="template_undefined",
        description="dag template_undefined"
    )
    user_defined_filters: str = Field(
        title="user_defined_filters",
        description="dag user_defined_filters"
    )
    params: str = Field(
        title="params",
        description="dag params"
    )
    tags: List[str] = Field(
        title="tags",
        description="dag tags"
    )
    max_active_runs: str = Field(
        title="max_active_runs",
        description="dag max_active_runs"
    )
    dagrun_timeout: str = Field(
        title="dagrun_timeout",
        description="dag dagrun_timeout"
    )
    sla_miss_callback: str = Field(
        title="sla_miss_callback",
        description="dag sla_miss_callback"
    )
    default_view: str = Field(
        title="default_view",
        description="dag default_view"
    )
    orientation: str = Field(
        title="orientation",
        description="dag orientation"
    )
    catchup: str = Field(
        title="catchup",
        description="dag catchup"
    )
    on_failure_callback: str = Field(
        title="on_failure_callback",
        description="dag on_failure_callback"
    )
    is_paused_upon_creation: str = Field(
        title="is_paused_upon_creation",
        description="dag is_paused_upon_creation"
    )
    render_template_as_native_obj: str = Field(
        title="render_template_as_native_obj",
        description="dag render_template_as_native_obj"
    )
    owner_links: str = Field(
        title="owner_links",
        description="dag owner_links"
    )
