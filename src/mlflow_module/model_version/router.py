from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_module.model_version import service
from src.mlflow_module.schemas import ModelVersionInfo, ModelVersionOptions
from src.response import Response

router = APIRouter(
    prefix="/model-version",
    tags=["model-version"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=Response)
async def create_model_version(model_version_info: ModelVersionInfo):
    result = service.create_model_version(model_version_info.name, model_version_info.source,
                                          run_id=model_version_info.run_id, tags=model_version_info.tags,
                                          run_link=model_version_info.run_link,
                                          description=model_version_info.description,
                                          await_creation_for=model_version_info.await_creation_for)
    return Response.from_result(result)


@router.get("", response_model=Response)
async def search_model_versions(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                order_by: Optional[str] = None, page_token: Optional[str] = None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    result = service.search_model_versions(max_results=max_results, filter_string=filter_string, order_by=order_by_list,
                                           page_token=page_token)
    return Response.from_result(result)


@router.get("/{model_name}/latest", response_model=Response)
async def get_latest_versions(model_name: str, stage: str = None):
    stages = None
    if stage:
        stages = [stage]
    result = service.get_latest_versions(model_name, stages)
    return Response.from_result(result)


@router.get("/{model_name}/{version}", response_model=Response)
async def get_model_version(model_name: str, version: int):
    result = service.get_model_version(model_name, str(version))
    return Response.from_result(result)


@router.delete("/{model_name}/{version}", response_model=Response)
async def delete_model_version(model_name: str, version: int):
    result = service.delete_model_version(model_name, str(version))
    return Response.from_result(result)


@router.put("/{model_name}/{version}/description", response_model=Response)
async def update_model_version(model_name: str, version: int, model_version_options: ModelVersionOptions):
    result = service.update_model_version(model_name, str(version), model_version_options.description)
    return Response.from_result(result)


@router.get("/{model_name}/{version}/uri", response_model=Response)
async def get_model_version_download_uri(model_name: str, version: int):
    result = service.get_model_version_download_uri(model_name, str(version))
    return Response.from_result(result)


@router.get("/{model_name}/{version}/stages", response_model=Response)
async def get_model_version_stages(model_name: str, version: int):
    result = service.get_model_version_stages(model_name, str(version))
    return Response.from_result(result)


@router.put("/{model_name}/{version}/{stage}", response_model=Response)
async def transition_model_version_stage(model_name: str, version: int, stage: str,
                                         model_version_options: ModelVersionOptions):
    result = service.transition_model_version_stage(model_name, str(version), stage,
                                                    archive_existing_versions=model_version_options.archive_existing_version)
    return Response.from_result(result)


@router.put("/{model_name}/{version_or_stage}/tag", response_model=Response)
async def set_model_version_tag(model_name: str, version_or_stage: str,
                                model_version_options: ModelVersionOptions):
    tag = model_version_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    version = None
    stage = None
    if version_or_stage.isdigit():
        version = version_or_stage
    else:
        stage = version_or_stage
    result = service.set_model_version_tag(model_name, version=version, stage=stage, key=key, value=value)
    return Response.from_result(result)


@router.delete("/{model_name}/{version_or_stage}/tag/{tag_key}", response_model=Response)
async def delete_model_version_tag(model_name: str, version_or_stage: str, tag_key: str):
    version = None
    stage = None
    if version_or_stage.isdigit():
        version = version_or_stage
    else:
        stage = version_or_stage
    result = service.delete_model_version_tag(model_name, version=version, stage=stage, key=tag_key)
    return Response.from_result(result)


@router.get("/{model_name}/alias/{alias}", response_model=Response)
async def get_model_version_by_alias(model_name: str, alias: str):
    result = service.get_model_version_by_alias(model_name, alias)
    return Response.from_result(result)
