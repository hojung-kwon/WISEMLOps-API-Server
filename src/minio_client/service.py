from datetime import timedelta
from typing import Optional

from minio import Minio
from minio.error import MinioException

from src.minio_client.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE
from src.minio_client.models import BucketInfo, ObjectInfo
from src.minio_client.utils import response_error, response_success
from src.models import APIResponseModel

_minio_client = Minio(endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY,
                      secure=MINIO_SECURE)


def list_buckets() -> APIResponseModel:
    try:
        result = _minio_client.list_buckets()
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def bucket_exists(bucket_name: str) -> APIResponseModel:
    try:
        result = _minio_client.bucket_exists(bucket_name)
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def make_bucket(bucket_info: BucketInfo) -> APIResponseModel:
    try:
        available = not _minio_client.bucket_exists(bucket_info.bucket_name)
        if available:
            _minio_client.make_bucket(bucket_info.bucket_name, object_lock=bucket_info.object_lock)
    except MinioException as me:
        return response_error(me)
    return response_success(available)


def remove_bucket(bucket_name: str) -> APIResponseModel:
    try:
        available = _minio_client.bucket_exists(bucket_name)
        if available:
            _minio_client.remove_bucket(bucket_name)
    except MinioException as me:
        return response_error(me)
    return response_success(available)


def list_objects(bucket_name: str,
                 prefix: Optional[str] = None,
                 recursive: bool = False,
                 start_after: Optional[str] = None) -> APIResponseModel:
    try:
        result = [*_minio_client.list_objects(bucket_name, prefix=prefix, recursive=recursive, start_after=start_after)]
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def fget_object(bucket_name: str,
                object_info: ObjectInfo) -> APIResponseModel:
    try:
        if object_info.file_path is None:
            object_info.file_path = object_info.object_name
        result = _minio_client.fget_object(bucket_name, object_info.object_name, object_info.file_path,
                                           version_id=object_info.version_id)
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def fput_object(bucket_name: str,
                object_info: ObjectInfo) -> APIResponseModel:
    try:
        result = _minio_client.fput_object(bucket_name, object_info.object_name, object_info.file_path)
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def stat_object(bucket_name: str,
                object_info: ObjectInfo) -> APIResponseModel:
    try:
        result = _minio_client.stat_object(bucket_name, object_info.object_name, version_id=object_info.version_id)
    except MinioException as me:
        return response_error(me)
    return response_success(result)


def remove_object(bucket_name: str,
                  object_info: ObjectInfo) -> APIResponseModel:
    try:
        _minio_client.remove_object(bucket_name, object_info.object_name, version_id=object_info.version_id)
    except MinioException as me:
        return response_error(me)
    return response_success(None)


def presigned_get_object(bucket_name: str,
                         object_info: ObjectInfo) -> APIResponseModel:
    try:
        if object_info.expire_days > 7 or object_info.expire_days < 1:
            expires = timedelta(days=7)
        else:
            expires = timedelta(days=object_info.expire_days)

        result = _minio_client.presigned_get_object(bucket_name, object_info.object_name, expires=expires,
                                                    version_id=object_info.version_id)
    except MinioException as me:
        return response_error(me)
    return response_success(result)
