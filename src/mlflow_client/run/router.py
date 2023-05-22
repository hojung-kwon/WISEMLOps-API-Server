from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_client.run import service, models
from src.models import APIResponseModel

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=APIResponseModel)
async def create_run(run_info: models.RunInfo):
    return service.create_run(run_info.experiment_id, start_time=run_info.start_time, tags=run_info.tags,
                              run_name=run_info.run_name)


@router.get("", response_model=APIResponseModel)
async def search_runs(experiment_id: int, filter_string: str = '', run_view_type: int = 1,
                      max_results: int = 1000, order_by: Optional[str] = None, page_token: Optional[str] = None):
    experiment_ids = [str(experiment_id)]
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_runs(experiment_ids, filter_string=filter_string, run_view_type=run_view_type,
                               max_results=max_results, order_by=order_by_list, page_token=page_token)


@router.get("/{run_id}", response_model=APIResponseModel)
async def get_run(run_id: str):
    return service.get_run(run_id)


@router.put("/{run_id}", response_model=APIResponseModel)
async def update_run(run_id: str, run_options: models.RunOptions):
    return service.update_run(run_id, status=run_options.status, name=run_options.name)


@router.delete("/{run_id}", response_model=APIResponseModel)
async def delete_run(run_id: str):
    return service.delete_run(run_id)


@router.get("/{run_id}/artifacts", response_model=APIResponseModel)
async def list_artifacts(run_id: str):
    return service.list_artifacts(run_id)


@router.post("/{run_id}/restore", response_model=APIResponseModel)
async def restore_run(run_id: str):
    return service.restore_run(run_id)


@router.post("/{run_id}/terminated", response_model=APIResponseModel)
async def set_terminated(run_id: str, run_options: models.RunOptions):
    return service.set_terminated(run_id, run_options.status, run_options.end_time)


@router.put("/{run_id}/tag", response_model=APIResponseModel)
async def set_tag(run_id: str, run_options: models.RunOptions):
    tag = run_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    return service.set_tag(run_id, key, value)


@router.delete("/{run_id}/tag/{tag_key}", response_model=APIResponseModel)
async def delete_tag(run_id: str, tag_key: str):
    return service.delete_tag(run_id, tag_key)


@router.get("/{run_id}/metric/{metric_name}", response_model=APIResponseModel)
async def get_metric_history(run_id: str, metric_name: str):
    return service.get_metric_history(run_id, key=metric_name)
