from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.response import Response
from src.workflow_pipeline_module import workflow_pipeline_service
from src.workflow_pipeline_module.config import MODULE_CODE
from src.workflow_pipeline_module.database import get_db
from src.workflow_pipeline_module.schemas import PipelineDto

router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=Response)
def create_pipeline(pipeline: PipelineDto, db: Session = Depends(get_db)):
    result = workflow_pipeline_service.create_pipeline(db=db, pipeline=pipeline)
    return Response.from_result(MODULE_CODE, result)


@router.get("", response_model=Response)
def get_pipelines(pipeline_name: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pipelines = workflow_pipeline_service.get_pipelines(db, pipeline_name=pipeline_name, skip=skip, limit=limit)
    return Response.from_result(MODULE_CODE, pipelines)


@router.get("/{pipeline_id}", response_model=Response)
def get_pipeline(pipeline_id: str, db: Session = Depends(get_db)):
    pipelines = workflow_pipeline_service.get_pipeline_by_id(db, pipeline_id)
    return Response.from_result(MODULE_CODE, pipelines)
