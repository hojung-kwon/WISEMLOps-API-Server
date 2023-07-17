from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models import APIResponseModel
from src.pipeline_generator import pipeline_gen_service
from src.pipeline_generator.models import PipelineInfo

router = APIRouter(
    prefix="/gen-pipeline",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("/", tags=["gen-pipeline"], response_model=APIResponseModel)
async def make_pipeline_tar_gz(pipeline_info: PipelineInfo):
    return pipeline_gen_service.make_pipeline_tar_gz(pipeline_info)
