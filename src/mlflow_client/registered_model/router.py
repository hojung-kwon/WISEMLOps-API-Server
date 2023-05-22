from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_client.registered_model import service, models
from src.models import APIResponseModel

router = APIRouter(
    prefix="/registered-model",
    tags=["registered-model"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=APIResponseModel)
async def create_registered_model(registered_model_info: models.RegisteredModelInfo):
    return service.create_registered_model(registered_model_info.name, tags=registered_model_info.tags,
                                           description=registered_model_info.description)


@router.get("", response_model=APIResponseModel)
async def search_registered_models(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                   order_by: Optional[str] = None, page_token: Optional[str] = None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_registered_models(max_results=max_results, filter_string=filter_string,
                                            order_by=order_by_list, page_token=page_token)


@router.get("/{model_name}", response_model=APIResponseModel)
async def get_registered_model(model_name: str):
    return service.get_registered_model(model_name)


@router.delete("/{model_name}", response_model=APIResponseModel)
async def delete_registered_model(model_name: str):
    return service.delete_registered_model(model_name)


@router.put("/{model_name}/name", response_model=APIResponseModel)
async def rename_registered_model(model_name: str, registered_model_options: models.RegisteredModelOptions):
    return service.rename_registered_model(model_name, registered_model_options.name)


@router.put("/{model_name}/description", response_model=APIResponseModel)
async def update_registered_model(model_name: str, registered_model_options: models.RegisteredModelOptions):
    return service.update_registered_model(model_name, registered_model_options.description)


@router.put("/{model_name}/alias/{version}", response_model=APIResponseModel)
async def set_registered_model_alias(model_name: str, version: int,
                                     registered_model_options: models.RegisteredModelOptions):
    return service.set_registered_model_alias(model_name, registered_model_options.alias, str(version))


@router.delete("/{model_name}/alias/{alias}", response_model=APIResponseModel)
async def delete_registered_model_alias(model_name: str, alias: str):
    return service.delete_registered_model_alias(model_name, alias)


@router.put("/{model_name}/tag", response_model=APIResponseModel)
async def set_registered_model_tag(model_name: str, registered_model_options: models.RegisteredModelOptions):
    tag = registered_model_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    return service.set_registered_model_tag(model_name, key, value)


@router.delete("/{model_name}/tag/{tag_key}", response_model=APIResponseModel)
async def delete_registered_model_tag(model_name: str, tag_key: str):
    return service.delete_registered_model_tag(model_name, tag_key)
