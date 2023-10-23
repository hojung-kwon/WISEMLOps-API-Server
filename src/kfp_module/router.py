from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kfp_module import kfp_service
from src.kfp_module.schemas import Experiment, Pipeline, PipelineVersion, Run, RecurringRun, RunPipelinePackage
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
async def list_experiments(page_token: str = '', page_size: int = 10, sort_by: str = ''):
    return Response.from_result(MODULE_CODE, kfp_service.list_experiments(page_token=page_token,
                                                                          page_size=page_size,
                                                                          sort_by=sort_by))


@router.get("/archive-experiments", tags=["kfp"], response_model=Response)
async def list_archive_experiments(page_token: str = '', page_size: int = 10, sort_by: str = ''):
    return Response.from_result(MODULE_CODE, kfp_service.list_archive_experiments(page_token=page_token,
                                                                                  page_size=page_size,
                                                                                  sort_by=sort_by))


@router.get("/unarchive-experiments", tags=["kfp"], response_model=Response)
async def list_unarchive_experiments(page_token: str = '', page_size: int = 10, sort_by: str = ''):
    return Response.from_result(MODULE_CODE, kfp_service.list_unarchive_experiments(page_token=page_token,
                                                                                    page_size=page_size,
                                                                                    sort_by=sort_by))


@router.post("/experiments", tags=["kfp"], response_model=Response)
async def create_experiment(experiment: Experiment):
    return Response.from_result(MODULE_CODE, kfp_service.create_experiment(experiment))


@router.get("/experiments/{experiment_id}", tags=["kfp"], response_model=Response)
async def get_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_experiment(experiment_id=experiment_id))


@router.patch("/experiments/{experiment_id}/archive", tags=["kfp"], response_model=Response)
async def archive_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.archive_experiment(experiment_id=experiment_id))


@router.patch("/experiments/{experiment_id}/unarchive", tags=["kfp"], response_model=Response)
async def unarchive_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.unarchive_experiment(experiment_id=experiment_id))


@router.delete("/experiments/{experiment_id}", tags=["kfp"], response_model=Response)
async def delete_experiment(experiment_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_experiment(experiment_id=experiment_id))


@router.get("/pipelines", tags=["kfp"], response_model=Response)
async def list_pipelines(page_token: str = '', page_size: int = 10, sort_by: str = ''):
    return Response.from_result(MODULE_CODE, kfp_service.list_pipelines(page_token=page_token,
                                                                        page_size=page_size,
                                                                        sort_by=sort_by))


@router.post("/pipelines", tags=["kfp"], response_model=Response)
async def upload_pipeline(pipeline: Pipeline):
    return Response.from_result(MODULE_CODE, kfp_service.upload_pipeline(pipeline))


@router.get("/pipelines/{pipeline_id}", tags=["kfp"], response_model=Response)
async def get_pipeline(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline(pipeline_id))


@router.delete("/pipelines/{pipeline_id}", tags=["kfp"], response_model=Response)
async def delete_pipeline(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_pipeline(pipeline_id))


@router.post("/pipelines/versions", tags=["kfp"], response_model=Response)
async def upload_pipeline_version(pipeline_version: PipelineVersion):
    return Response.from_result(MODULE_CODE, kfp_service.upload_pipeline_version(pipeline_version))


@router.get("/pipelines/versions/{pipeline_id}", tags=["kfp"], response_model=Response)
async def list_pipeline_versions(pipeline_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.list_pipeline_versions(pipeline_id))


@router.get("/pipelines/versions/{pipeline_id}/{version_id}", tags=["kfp"], response_model=Response)
async def get_pipeline_version(pipeline_id: str, version_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_pipeline_version(pipeline_id, version_id))


@router.delete("/pipelines/versions/{pipeline_id}/{version_id}", tags=["kfp"], response_model=Response)
async def delete_pipeline_version(pipeline_id: str, version_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_pipeline_version(pipeline_id, version_id))


@router.get("/runs", tags=["kfp"], response_model=Response)
async def list_runs(page_token: str = '', page_size: int = 10, sort_by: str = '', experiment_id: Optional[str] = None):
    return Response.from_result(MODULE_CODE, kfp_service.list_runs(page_token=page_token,
                                                                   page_size=page_size,
                                                                   sort_by=sort_by,
                                                                   experiment_id=experiment_id))


@router.post("/runs", tags=["kfp"], response_model=Response)
async def run_pipeline(run: Run):
    return Response.from_result(MODULE_CODE, kfp_service.run_pipeline(run))


@router.post("/runs/package", tags=["kfp"], response_model=Response)
async def create_run_from_pipeline_package(run: RunPipelinePackage):
    return Response.from_result(MODULE_CODE, kfp_service.create_run_from_pipeline_package(run))


@router.get("/runs/{run_id}", tags=["kfp"], response_model=Response)
async def get_run(run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_run(run_id))


@router.get("/runs/{run_id}/{timeout}", tags=["kfp"], response_model=Response)
async def wait_for_run_completion(run_id: str, timeout: int):
    return Response.from_result(MODULE_CODE, kfp_service.wait_for_run_completion(run_id, timeout))


@router.get("/recurring-runs", tags=["kfp"], response_model=Response)
async def list_recurring_runs(page_token: str = '', page_size: int = 10, sort_by: str = '',
                              experiment_id: Optional[str] = None):
    return Response.from_result(MODULE_CODE, kfp_service.list_recurring_runs(page_token=page_token,
                                                                             page_size=page_size,
                                                                             sort_by=sort_by,
                                                                             experiment_id=experiment_id))


@router.post("/recurring-runs", tags=["kfp"], response_model=Response)
async def create_recurring_run(recurring_run: RecurringRun):
    return Response.from_result(MODULE_CODE, kfp_service.create_recurring_run(recurring_run))


@router.get("/recurring-runs/{recurring_run_id}", tags=["kfp"], response_model=Response)
async def get_recurring_run(recurring_run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.get_recurring_run(recurring_run_id))


@router.delete("/recurring-runs/{recurring_run_id}", tags=["kfp"], response_model=Response)
async def delete_recurring_run(recurring_run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.delete_recurring_run(recurring_run_id))


@router.patch("/recurring-runs/{recurring_run_id}/disable", tags=["kfp"], response_model=Response)
async def disable_recurring_run(recurring_run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.disable_recurring_run(recurring_run_id))


@router.patch("/recurring-runs/{recurring_run_id}/enable", tags=["kfp"], response_model=Response)
async def enable_recurring_run(recurring_run_id: str):
    return Response.from_result(MODULE_CODE, kfp_service.enable_recurring_run(recurring_run_id))
