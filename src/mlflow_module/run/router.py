from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_module.config import MODULE_CODE
from src.mlflow_module.run import service
from src.mlflow_module.schemas import RunInfo, RunOptions
from src.response import Response

router = APIRouter(
    prefix="/run",
    tags=["run"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=Response)
async def create_run(run_info: RunInfo):
    result = service.create_run(run_info.experiment_id, start_time=run_info.start_time, tags=run_info.tags,
                                run_name=run_info.run_name)
    return Response.from_result(MODULE_CODE, result)


@router.get("", response_model=Response)
async def search_runs(experiment_id: int, filter_string: str = '', run_view_type: int = 1,
                      max_results: int = 1000, order_by: Optional[str] = None, page_token: Optional[str] = None):
    experiment_ids = [str(experiment_id)]
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    result = service.search_runs(experiment_ids, filter_string=filter_string, run_view_type=run_view_type,
                                 max_results=max_results, order_by=order_by_list, page_token=page_token)
    return Response.from_result(MODULE_CODE, result)


@router.get("/{run_id}", response_model=Response)
async def get_run(run_id: str):
    result = service.get_run(run_id)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{run_id}", response_model=Response)
async def update_run(run_id: str, run_options: RunOptions):
    result = service.update_run(run_id, status=run_options.status, name=run_options.name)
    return Response.from_result(MODULE_CODE, result)


@router.delete("/{run_id}", response_model=Response)
async def delete_run(run_id: str):
    result = service.delete_run(run_id)
    return Response.from_result(MODULE_CODE, result)


@router.get("/{run_id}/artifacts", response_model=Response)
async def list_artifacts(run_id: str):
    result = service.list_artifacts(run_id)
    return Response.from_result(MODULE_CODE, result)


@router.post("/{run_id}/restore", response_model=Response)
async def restore_run(run_id: str):
    result = service.restore_run(run_id)
    return Response.from_result(MODULE_CODE, result)


@router.post("/{run_id}/terminated", response_model=Response)
async def set_terminated(run_id: str, run_options: RunOptions):
    result = service.set_terminated(run_id, run_options.status, run_options.end_time)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{run_id}/tag", response_model=Response)
async def set_tag(run_id: str, run_options: RunOptions):
    tag = run_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    result = service.set_tag(run_id, key, value)
    return Response.from_result(MODULE_CODE, result)


@router.delete("/{run_id}/tag/{tag_key}", response_model=Response)
async def delete_tag(run_id: str, tag_key: str):
    result = service.delete_tag(run_id, tag_key)
    return Response.from_result(MODULE_CODE, result)


@router.get("/{run_id}/metric/{metric_name}", response_model=Response)
async def get_metric_history(run_id: str, metric_name: str):
    result = service.get_metric_history(run_id, key=metric_name)
    return Response.from_result(MODULE_CODE, result)
