from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_module.experiment import service, models
from src.response import Response

router = APIRouter(
    prefix="/experiment",
    tags=["experiment"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=Response)
async def create_experiment(experiment_info: models.ExperimentInfo):
    result = service.create_experiment(experiment_info.name, artifact_location=experiment_info.artifact_location,
                                       tags=experiment_info.tags)
    return Response.from_result(result)


@router.get("", response_model=Response)
async def search_experiments(view_type: int = 1, max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                             order_by: Optional[str] = None, page_token: Optional[str] = None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    result = service.search_experiments(view_type=view_type, max_results=max_results, filter_string=filter_string,
                                        order_by=order_by_list, page_token=page_token)

    return Response.from_result(result)


@router.get("/{experiment_id}", response_model=Response)
async def get_experiment(experiment_id: int):
    result = service.get_experiment(str(experiment_id))
    return Response.from_result(result)


@router.delete("/{experiment_id}", response_model=Response)
async def delete_experiment(experiment_id: int):
    result = service.delete_experiment(str(experiment_id))
    return Response.from_result(result)


@router.post("/{experiment_id}/restore", response_model=Response)
async def restore_experiment(experiment_id: int):
    result = service.restore_experiment(str(experiment_id))
    return Response.from_result(result)


@router.put("/{experiment_id}/name", response_model=Response)
async def rename_experiment(experiment_id: int, experiment_options: models.ExperimentOptions):
    result = service.rename_experiment(str(experiment_id), experiment_options.name)
    return Response.from_result(result)


@router.put("/{experiment_id}/tag", response_model=Response)
async def set_experiment_tag(experiment_id: int, experiment_options: models.ExperimentOptions):
    tag = experiment_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    result = service.set_experiment_tag(str(experiment_id), key, value)
    return Response.from_result(result)


@router.get("/name/{experiment_name}", response_model=Response)
async def get_experiment_by_name(experiment_name: str):
    result = service.get_experiment_by_name(experiment_name)
    return Response.from_result(result)
