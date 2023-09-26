from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src import app_config
from src.common_module import common_service
from src.response import Response
from src.workflow_generator_module.schemas import PipelineInfo
from src.workflow_pipeline_module.database import get_db

router = APIRouter(
    prefix="/workflow",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("/pipeline", tags=["workflow"], response_model=Response)
async def custom_pipeline(pipeline_info: PipelineInfo, db: Session = Depends(get_db)):
    return Response.from_result(app_config.SERVICE_CODE, common_service.make_pipeline(pipeline_info, db))
