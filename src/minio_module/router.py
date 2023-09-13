from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.minio_module import service
from src.minio_module.config import MODULE_CODE
from src.minio_module.schemas import BucketInfo, ObjectInfo
from src.response import Response

router = APIRouter(
    prefix="/minio",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("/bucket", tags=["bucket"], response_model=Response)
async def list_buckets():
    return Response.from_result(MODULE_CODE, service.list_buckets())


@router.post("/bucket", tags=["bucket"], response_model=Response)
async def make_bucket(bucket_info: BucketInfo):
    return Response.from_result(MODULE_CODE, service.make_bucket(bucket_info))


@router.get("/bucket/{bucket_name}", tags=["bucket"], response_model=Response)
async def bucket_exists(bucket_name: str):
    return Response.from_result(MODULE_CODE, service.bucket_exists(bucket_name))


@router.delete("/bucket/{bucket_name}", tags=["bucket"], response_model=Response)
async def remove_bucket(bucket_name: str):
    return Response.from_result(MODULE_CODE, service.remove_bucket(bucket_name))


@router.get("/object/{bucket_name}", tags=["object"], response_model=Response)
async def list_objects(bucket_name: str,
                       prefix: Optional[str] = None,
                       recursive: bool = False,
                       start_after: Optional[str] = None):
    return Response.from_result(MODULE_CODE,
                                service.list_objects(bucket_name, prefix=prefix, recursive=recursive,
                                                     start_after=start_after))


@router.post("/object/{bucket_name}/stat", tags=["object"], response_model=Response)
def stat_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(MODULE_CODE, service.stat_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/download", tags=["object"], response_model=Response)
def fget_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(MODULE_CODE, service.fget_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/download/url", tags=["object"], response_model=Response)
def presigned_get_object(bucket_name: str,
                         object_info: ObjectInfo):
    return Response.from_result(MODULE_CODE, service.presigned_get_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/upload", tags=["object"], response_model=Response)
def fput_object(bucket_name: str,
                object_info: ObjectInfo):
    return Response.from_result(MODULE_CODE, service.fput_object(bucket_name, object_info))


@router.post("/object/{bucket_name}/delete", tags=["object"], response_model=Response)
def remove_object(bucket_name: str,
                  object_info: ObjectInfo):
    return Response.from_result(MODULE_CODE, service.remove_object(bucket_name, object_info))
