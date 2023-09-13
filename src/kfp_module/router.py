from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kfp_module import kfp_service
from src.kfp_module.schemas import Experiment, Pipeline, PipelineVersion, Run, RecurringRun
from src.kserve_module.config import MODULE_CODE
from src.response import Response

router = APIRouter(
    prefix="/kfp",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("", tags=["kfp"], response_model=Response)
async def get_kfp_healthz():
    return Response.from_result(MODULE_CODE, kfp_service.get_kfp_healthz())


@router.get("/namespace", tags=["kfp"], response_model=Response)
async def get_user_namespace():
    return Response.from_result(MODULE_CODE, kfp_service.get_user_namespace())


@router.get("/experiments", tags=["kfp"], response_model=Response)
async def list_experiments():
    return Response.from_result(MODULE_CODE, kfp_service.list_experiments())


@router.post("/experiments", tags=["kfp"], response_model=Response)
async def create_experiment(experiment: Experiment):
    return Response.from_result(MODULE_CODE, kfp_service.create_experiment(experiment))


@router.get("/experiments/{experiment_id}", tags=["kfp"], response_model=Response)
async def get_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_experiment(experiment_id=experiment_id))


@router.get("/experiments/{experiment_id}/archive", tags=["kfp"], response_model=Response)
async def archive_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.archive_experiment(experiment_id=experiment_id))


@router.delete("/experiments/{experiment_id}", tags=["kfp"], response_model=Response)
async def delete_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_experiment(experiment_id=experiment_id))


@router.get("/pipelines", tags=["kfp"], response_model=Response)
async def list_pipelines():
    return Response.from_result(MODULE_CODE, kfp_service.list_pipelines())


@router.post("/pipelines", tags=["kfp"], response_model=Response)
async def upload_pipeline(pipeline: Pipeline):
    return Response.from_result(MODULE_CODE, kfp_service.upload_pipeline(pipeline))


@router.get("/pipelines/{pipeline_id}", tags=["kfp"], response_model=Response)
async def get_pipeline(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline(pipeline_id))


@router.get("/pipelines/{pipeline_id}/template", tags=["kfp"], response_model=Response)
async def get_pipeline_template(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline_template(pipeline_id))


@router.get("/pipelines/{pipeline_id}/versions", tags=["kfp"], response_model=Response)
async def list_pipeline_versions(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.list_pipeline_versions(pipeline_id))


@router.delete("/pipelines/{pipeline_id}", tags=["kfp"], response_model=Response)
async def delete_pipeline(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_pipeline(pipeline_id))


@router.get("/pipelines/{pipeline_name}/id", tags=["kfp"], response_model=Response)
async def get_pipeline_id(pipeline_name: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline_id(pipeline_name))


@router.post("/pipelines/versions", tags=["kfp"], response_model=Response)
async def upload_pipeline_version(pipeline_version: PipelineVersion):
    return Response.from_result(MODULE_CODE, kfp_service.upload_pipeline_version(pipeline_version))


@router.get("/pipelines/versions/{version_id}", tags=["kfp"], response_model=Response)
async def get_pipeline_version(version_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline_version(version_id))


@router.get("/pipelines/versions/{version_id}/template", tags=["kfp"], response_model=Response)
async def get_pipeline_version_template(version_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline_version_template(version_id))


@router.delete("/pipelines/versions/{version_id}", tags=["kfp"], response_model=Response)
async def delete_pipeline_version(version_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_pipeline_version(version_id))


@router.get("/runs", tags=["kfp"], response_model=Response)
async def list_runs():
    return Response.from_result(MODULE_CODE, kfp_service.list_runs())


@router.post("/runs", tags=["kfp"], response_model=Response)
async def create_run_from_pipeline_package(run: Run):
    return Response.from_result(MODULE_CODE, kfp_service.create_run_from_pipeline_package(run))


@router.get("/runs/{run_id}", tags=["kfp"], response_model=Response)
async def get_run(run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_run(run_id))


@router.get("/runs/{run_id}/{timeout}", tags=["kfp"], response_model=Response)
async def wait_for_run_completion(run_id: str, timeout: int):
    return Response.from_result(MODULE_CODE, kfp_service.wait_for_run_completion(run_id, timeout))


@router.get("/recurring-runs", tags=["kfp"], response_model=Response)
async def list_recurring_runs():
    return Response.from_result(MODULE_CODE, kfp_service.list_recurring_runs())


@router.post("/recurring-runs", tags=["kfp"], response_model=Response)
async def create_recurring_run(recurring_run: RecurringRun):
    return Response.from_result(MODULE_CODE, kfp_service.create_recurring_run(recurring_run))


@router.get("/recurring-runs/{job_id}", tags=["kfp"], response_model=Response)
async def get_recurring_run(job_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_recurring_run(job_id))


@router.delete("/recurring-runs/{job_id}", tags=["kfp"], response_model=Response)
async def delete_job(job_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_job(job_id))


@router.patch("/recurring-runs/{job_id}", tags=["kfp"], response_model=Response)
async def disable_job(job_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.disable_job(job_id))


@router.get("/artifact/{run_id}/{node_id}/{artifact_name}", tags=["kfp"], response_model=Response)
async def read_artifact(run_id: str, node_id: str, artifact_name: str):
    return Response.from_result(MODULE_CODE, kfp_service.read_artifact(run_id, node_id, artifact_name))


@router.get("/detail/{run_id}", tags=["kfp"], response_model=Response)
async def get_run_detail(run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_run_detail(run_id))
