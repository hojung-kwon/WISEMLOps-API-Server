from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_client.model_version import service, models
from src.models import APIResponseModel

router = APIRouter(
    prefix="/model-version",
    tags=["model-version"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=APIResponseModel)
async def create_model_version(model_version_info: models.ModelVersionInfo):
    return service.create_model_version(model_version_info.name, model_version_info.source,
                                        run_id=model_version_info.run_id, tags=model_version_info.tags,
                                        run_link=model_version_info.run_link,
                                        description=model_version_info.description,
                                        await_creation_for=model_version_info.await_creation_for)


@router.get("", response_model=APIResponseModel)
async def search_model_versions(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                order_by: Optional[str] = None, page_token: Optional[str] = None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_model_versions(max_results=max_results, filter_string=filter_string, order_by=order_by_list,
                                         page_token=page_token)


@router.get("/{model_name}/latest", response_model=APIResponseModel)
async def get_latest_versions(model_name: str, stage: str = None):
    stages = None
    if stage:
        stages = [stage]
    return service.get_latest_versions(model_name, stages)


@router.get("/{model_name}/{version}", response_model=APIResponseModel)
async def get_model_version(model_name: str, version: int):
    return service.get_model_version(model_name, str(version))


@router.delete("/{model_name}/{version}", response_model=APIResponseModel)
async def delete_model_version(model_name: str, version: int):
    return service.delete_model_version(model_name, str(version))


@router.put("/{model_name}/{version}/description", response_model=APIResponseModel)
async def update_model_version(model_name: str, version: int, model_version_options: models.ModelVersionOptions):
    return service.update_model_version(model_name, str(version), model_version_options.description)


@router.get("/{model_name}/{version}/uri", response_model=APIResponseModel)
async def get_model_version_download_uri(model_name: str, version: int):
    return service.get_model_version_download_uri(model_name, str(version))


@router.get("/{model_name}/{version}/stages", response_model=APIResponseModel)
async def get_model_version_stages(model_name: str, version: int):
    return service.get_model_version_stages(model_name, str(version))


@router.put("/{model_name}/{version}/{stage}", response_model=APIResponseModel)
async def transition_model_version_stage(model_name: str, version: int, stage: str,
                                         model_version_options: models.ModelVersionOptions):
    return service.transition_model_version_stage(model_name, str(version), stage,
                                                  archive_existing_versions=model_version_options.archive_existing_version)


@router.put("/{model_name}/{version_or_stage}/tag", response_model=APIResponseModel)
async def set_model_version_tag(model_name: str, version_or_stage: str,
                                model_version_options: models.ModelVersionOptions):
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
    return service.set_model_version_tag(model_name, version=version, stage=stage, key=key, value=value)


@router.delete("/{model_name}/{version_or_stage}/tag/{tag_key}", response_model=APIResponseModel)
async def delete_model_version_tag(model_name: str, version_or_stage: str, tag_key: str):
    version = None
    stage = None
    if version_or_stage.isdigit():
        version = version_or_stage
    else:
        stage = version_or_stage
    return service.delete_model_version_tag(model_name, version=version, stage=stage, key=tag_key)


@router.get("/{model_name}/alias/{alias}", response_model=APIResponseModel)
async def get_model_version_by_alias(model_name: str, alias: str):
    return service.get_model_version_by_alias(model_name, alias)
