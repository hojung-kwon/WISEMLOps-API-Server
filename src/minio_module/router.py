from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.minio_module import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from src.minio_module.schemas import BucketInfo, ObjectInfo
from src.minio_module.service import MinIOService
from src.models import APIResponseModel
from src.response import Response

router = APIRouter(
    prefix="/minio",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)

service = MinIOService(endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)


@router.get("/bucket", tags=["bucket"], response_model=APIResponseModel)
async def list_buckets():
    return Response.from_result(service.list_buckets())


@router.post("/bucket", tags=["bucket"], response_model=APIResponseModel)
async def make_bucket(bucket_info: BucketInfo):
    return Response.from_result(service.make_bucket(bucket_info))


@router.get("/bucket/{bucket_name}", tags=["bucket"], response_model=APIResponseModel)
async def bucket_exists(bucket_name: str):
    return Response.from_result(service.bucket_exists(bucket_name))


@router.delete("/bucket/{bucket_name}", tags=["bucket"], response_model=APIResponseModel)
async def remove_bucket(bucket_name: str):
    return Response.from_result(service.remove_bucket(bucket_name))


@router.get("/object/{bucket_name}", tags=["object"], response_model=APIResponseModel)
async def list_objects(bucket_name: str,
                       prefix: Optional[str] = None,
                       recursive: bool = False,
                       start_after: Optional[str] = None):
    return Response.from_result(
        service.list_objects(bucket_name, prefix=prefix, recursive=recursive, start_after=start_after))


@router.post("/object/{bucket_name}/stat", tags=["object"], response_model=APIResponseModel)
def stat_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(service.stat_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/download", tags=["object"], response_model=APIResponseModel)
def fget_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(service.fget_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/download/url", tags=["object"], response_model=APIResponseModel)
def presigned_get_object(bucket_name: str,
                         object_info: ObjectInfo):
    return Response.from_result(service.presigned_get_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/upload", tags=["object"], response_model=APIResponseModel)
def fput_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(service.fput_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/delete", tags=["object"], response_model=APIResponseModel)
def remove_object(bucket_name: str,
                  object_info: ObjectInfo):
    return Response.from_result(service.remove_object(bucket_name, object_info))
