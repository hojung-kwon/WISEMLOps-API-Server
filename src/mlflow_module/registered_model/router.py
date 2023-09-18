from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_module.config import MODULE_CODE
from src.mlflow_module.registered_model import service
from src.mlflow_module.schemas import RegisteredModelInfo, RegisteredModelOptions
from src.response import Response

router = APIRouter(
    prefix="/registered-model",
    tags=["registered-model"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=Response)
async def create_registered_model(registered_model_info: RegisteredModelInfo):
    result = service.create_registered_model(registered_model_info.name, tags=registered_model_info.tags,
                                             description=registered_model_info.description)
    return Response.from_result(MODULE_CODE, result)


@router.get("", response_model=Response)
async def search_registered_models(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                   order_by: Optional[str] = None, page_token: Optional[str] = None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    result = service.search_registered_models(max_results=max_results, filter_string=filter_string,
                                              order_by=order_by_list, page_token=page_token)
    return Response.from_result(MODULE_CODE, result)


@router.get("/{model_name}", response_model=Response)
async def get_registered_model(model_name: str):
    result = service.get_registered_model(model_name)
    return Response.from_result(MODULE_CODE, result)


@router.delete("/{model_name}", response_model=Response)
async def delete_registered_model(model_name: str):
    result = service.delete_registered_model(model_name)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{model_name}/name", response_model=Response)
async def rename_registered_model(model_name: str, registered_model_options: RegisteredModelOptions):
    result = service.rename_registered_model(model_name, registered_model_options.name)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{model_name}/description", response_model=Response)
async def update_registered_model(model_name: str, registered_model_options: RegisteredModelOptions):
    result = service.update_registered_model(model_name, registered_model_options.description)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{model_name}/alias/{version}", response_model=Response)
async def set_registered_model_alias(model_name: str, version: int,
                                     registered_model_options: RegisteredModelOptions):
    result = service.set_registered_model_alias(model_name, registered_model_options.alias, str(version))
    return Response.from_result(MODULE_CODE, result)


@router.delete("/{model_name}/alias/{alias}", response_model=Response)
async def delete_registered_model_alias(model_name: str, alias: str):
    result = service.delete_registered_model_alias(model_name, alias)
    return Response.from_result(MODULE_CODE, result)


@router.put("/{model_name}/tag", response_model=Response)
async def set_registered_model_tag(model_name: str, registered_model_options: RegisteredModelOptions):
    tag = registered_model_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    result = service.set_registered_model_tag(model_name, key, value)
    return Response.from_result(MODULE_CODE, result)


@router.delete("/{model_name}/tag/{tag_key}", response_model=Response)
async def delete_registered_model_tag(model_name: str, tag_key: str):
    result = service.delete_registered_model_tag(model_name, tag_key)
    return Response.from_result(MODULE_CODE, result)
