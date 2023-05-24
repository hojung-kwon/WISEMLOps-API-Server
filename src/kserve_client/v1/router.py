from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kserve_client.v1 import service, models
from src.models import APIResponseModel

router = APIRouter(
    prefix="/v1",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("", response_model=APIResponseModel)
async def create_inference_service(inference_service_info: models.InferenceServiceInfo):
    return service.create_inference_service(inference_service_info.name, inference_service_info.namespace,
                                            storage_uri=inference_service_info.storage_uri,
                                            service_account_name=inference_service_info.service_account_name,
                                            model_format=inference_service_info.model_format,
                                            protocol_version=inference_service_info.protocol_version)


@router.patch("", response_model=APIResponseModel)
async def patch_inference_service(inference_service_info: models.InferenceServiceInfo):
    return service.patch_inference_service(inference_service_info.name, inference_service_info.namespace,
                                           storage_uri=inference_service_info.storage_uri,
                                           service_account_name=inference_service_info.service_account_name,
                                           model_format=inference_service_info.model_format,
                                           protocol_version=inference_service_info.protocol_version)


@router.put("", response_model=APIResponseModel)
async def replace_inference_service(inference_service_info: models.InferenceServiceInfo):
    return service.replace_inference_service(inference_service_info.name, inference_service_info.namespace,
                                             storage_uri=inference_service_info.storage_uri,
                                             service_account_name=inference_service_info.service_account_name,
                                             model_format=inference_service_info.model_format,
                                             protocol_version=inference_service_info.protocol_version)


@router.delete("", response_model=APIResponseModel)
async def delete_inference_service(inference_service_info: models.InferenceServiceInfo):
    return service.delete_inference_service(inference_service_info.name, inference_service_info.namespace)


@router.get("{name}", response_model=APIResponseModel)
async def delete_inference_service(name: str, namespace: str):
    return service.delete_inference_service(name, namespace)
