from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.response import Response
from src.workflow_generator import pipeline_gen_service
from src.workflow_generator.schemas import PipelineInfo, DagInfo

router = APIRouter(
    prefix="/workflow",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("/kfp", tags=["workflow"], response_model=Response)
async def make_kfp_pipeline_tar_gz(pipeline_info: PipelineInfo):
    return Response.from_result(pipeline_gen_service.make_kfp_pipeline_tar_gz(pipeline_info))


@router.post("/airflow", tags=["workflow"], response_model=Response)
async def make_airflow_dag_file(dag_info: DagInfo, pipeline_info: PipelineInfo):
    return Response.from_result(pipeline_gen_service.make_airflow_dag_file(dag_info, pipeline_info))
