import re
from datetime import datetime
from typing import Optional, Dict, List

from pydantic import BaseModel, Field, validator

from src.workflow_pipeline_module.exceptions import RequestValidationError


class PipelineDto(BaseModel):
    pipeline_id: str = Field(
        title="pipeline_id",
        description="파이프라인 아이디"
    )
    pipeline_name: str = Field(
        title="pipeline_name",
        description="파이프라인 이름"
    )
    pipeline_description: Optional[str] = Field(
        title="pipeline_description",
        description="파이프라인 설명"
    )
    # version_info: Optional[Dict] = Field(
    #     title="version_info",
    #     description="파이프라인의 버전 정보"
    # )
    nodes: List[Dict] = Field(
        title="nodes",
        description="파이프라인 노드 정보"
    )
    edges: List[Dict] = Field(
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
    created_at: Optional[datetime] = Field(
        title="created_at",
        description="파이프라인 생성 시간"
    )
    updated_at: Optional[datetime] = Field(
        title="updated_at",
        description="파이프라인 수정 시간"
    )

    @validator('pipeline_name')
    def check_pipeline_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the pipeline name.",
                result={"current_name": v}
            )
        return v
