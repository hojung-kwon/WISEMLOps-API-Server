from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kubernetes_client import kfp_service
from src.kubernetes_client.models import Experiment, Pipeline, PipelineVersion, Run, RecurringRun
from src.models import APIResponseModel

router = APIRouter(
    prefix="/kfp",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("/", tags=["kfp"], response_model=APIResponseModel)
async def get_kfp_healthz():
    return kfp_service.get_kfp_healthz()


@router.get("/namespace", tags=["kfp"], response_model=APIResponseModel)
async def get_user_namespace():
    return kfp_service.get_user_namespace()


@router.get("/experiments", tags=["kfp"], response_model=APIResponseModel)
async def list_experiments():
    return kfp_service.list_experiments()


@router.post("/experiments", tags=["kfp"], response_model=APIResponseModel)
async def create_experiment(experiment: Experiment):
    return kfp_service.create_experiment(experiment)


@router.get("/experiments/{experiment_id}/id", tags=["kfp"], response_model=APIResponseModel)
async def get_experiment_by_id(experiment_id: str):
    return kfp_service.get_experiment(experiment_id=experiment_id)


@router.get("/experiments/{experiment_name}/name", tags=["kfp"], response_model=APIResponseModel)
async def get_experiment_by_name(experiment_name: str):
    return kfp_service.get_experiment(experiment_name=experiment_name)


@router.get("/experiments/{experiment_id}/archive", tags=["kfp"], response_model=APIResponseModel)
async def archive_experiment(experiment_id: str):
    return kfp_service.archive_experiment(experiment_id=experiment_id)


@router.delete("/experiments/{experiment_id}", tags=["kfp"], response_model=APIResponseModel)
async def delete_experiment(experiment_id: str):
    return kfp_service.delete_experiment(experiment_id=experiment_id)


@router.get("/pipelines", tags=["kfp"], response_model=APIResponseModel)
async def list_pipelines():
    return kfp_service.list_pipelines()


@router.post("/pipelines", tags=["kfp"], response_model=APIResponseModel)
async def upload_pipeline(pipeline: Pipeline):
    return kfp_service.upload_pipeline(pipeline)


@router.get("/pipelines/{pipeline_name}", tags=["kfp"], response_model=APIResponseModel)
async def get_pipeline(pipeline_name: str):
    pipeline_id = kfp_service.get_pipeline_id(pipeline_name)
    return kfp_service.get_pipeline(pipeline_id)


@router.delete("/pipelines/{pipeline_name}", tags=["kfp"], response_model=APIResponseModel)
async def delete_pipeline(pipeline_name: str):
    pipeline_id = kfp_service.get_pipeline_id(pipeline_name)
    return kfp_service.delete_pipeline(pipeline_id)


@router.get("/pipelines/{pipeline_name}/versions", tags=["kfp"], response_model=APIResponseModel)
async def list_pipeline_versions(pipeline_name: str):
    pipeline_id = kfp_service.get_pipeline_id(pipeline_name)
    return kfp_service.list_pipeline_versions(pipeline_id)


@router.post("/pipelines/{pipeline_name}/versions", tags=["kfp"], response_model=APIResponseModel)
async def upload_pipeline_version(pipeline_name: str, pipeline_version: PipelineVersion):
    if pipeline_version.pipeline_name is None or pipeline_version.pipeline_name != pipeline_name:
        pipeline_version.pipeline_name = pipeline_name
    if pipeline_version.pipeline_id is None:
        pipeline_version.pipeline_id = kfp_service.get_pipeline_id(pipeline_name)
    return kfp_service.upload_pipeline_version(pipeline_version)


@router.get("/pipelines/{pipeline_name}/id", tags=["kfp"], response_model=APIResponseModel)
async def get_pipeline_id(pipeline_name: str):
    return kfp_service.get_pipeline_id(pipeline_name)


@router.get("/runs", tags=["kfp"], response_model=APIResponseModel)
async def list_runs():
    return kfp_service.list_runs()


@router.post("/runs", tags=["kfp"], response_model=APIResponseModel)
async def create_run_from_pipeline_package(run: Run):
    return kfp_service.create_run_from_pipeline_package(run)


@router.get("/runs/{run_id}", tags=["kfp"], response_model=APIResponseModel)
async def get_run(run_id: str):
    return kfp_service.get_run(run_id)


@router.get("/runs/{run_id}/{timeout}", tags=["kfp"], response_model=APIResponseModel)
async def wait_for_run_completion(run_id: str, timeout: int):
    return kfp_service.wait_for_run_completion(run_id, timeout)


@router.get("/recurring-runs", tags=["kfp"], response_model=APIResponseModel)
async def list_recurring_runs():
    return kfp_service.list_recurring_runs()


@router.post("/recurring-runs", tags=["kfp"], response_model=APIResponseModel)
async def create_recurring_run(recurring_run: RecurringRun):
    return kfp_service.create_recurring_run(recurring_run)


@router.get("/recurring-runs/{job_id}", tags=["kfp"], response_model=APIResponseModel)
async def get_recurring_run(job_id: str):
    return kfp_service.get_recurring_run(job_id)


@router.delete("/recurring-runs/{job_id}", tags=["kfp"], response_model=APIResponseModel)
async def delete_job(job_id: str):
    return kfp_service.delete_job(job_id)


@router.patch("/recurring-runs/{job_id}", tags=["kfp"], response_model=APIResponseModel)
async def disable_job(job_id: str):
    return kfp_service.disable_job(job_id)
