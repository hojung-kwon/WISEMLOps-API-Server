from datetime import timedelta
from typing import List

from minio import Minio
from minio.api import ObjectWriteResult
from minio.datatypes import Bucket, Object
from minio.error import MinioException

from src.minio_client.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY
from src.minio_client.models import BucketInfo, ObjectInfo
from src.minio_client.utils import response_error, response_success
from src.models import APIResponseModel


class _MinIOClient:
    def __init__(self,
                 endpoint: str,
                 access_key: str,
                 secret_key: str,
                 secure: bool = False):
        self.client = Minio(endpoint=endpoint,
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=secure)

    def list_buckets(self) -> List[Bucket]:
        return self.client.list_buckets()

    def bucket_exists(self,
                      bucket_name: str) -> bool:
        return self.client.bucket_exists(bucket_name)

    def make_bucket(self,
                    bucket_name: str,
                    object_lock: bool = False):
        self.client.make_bucket(bucket_name, object_lock=object_lock)

    def remove_bucket(self,
                      bucket_name: str):
        self.client.remove_bucket(bucket_name)

    def list_objects(self,
                     bucket_name: str,
                     prefix: str = None,
                     recursive: bool = False,
                     start_after: bool = None) -> List[Object]:
        return [*self.client.list_objects(bucket_name, prefix=prefix, recursive=recursive, start_after=start_after)]

    def fget_object(self,
                    bucket_name: str,
                    object_name: str,
                    file_path: str,
                    version_id: str = None) -> Object:
        return self.client.fget_object(bucket_name, object_name, file_path, version_id=version_id)

    def fput_object(self,
                    bucket_name: str,
                    object_name: str,
                    file_path: str) -> ObjectWriteResult:
        return self.client.fput_object(bucket_name, object_name, file_path)

    def stat_object(self,
                    bucket_name: str,
                    object_name: str,
                    version_id: str = None) -> Object:
        return self.client.stat_object(bucket_name, object_name, version_id=version_id)

    def remove_object(self,
                      bucket_name: str,
                      object_name: str,
                      version_id: str = None):
        self.client.remove_object(bucket_name, object_name, version_id=version_id)

    def presigned_get_object(self,
                             bucket_name: str,
                             object_name: str,
                             expires: timedelta = timedelta(days=7),
                             version_id: str = None):
        return self.client.presigned_get_object(bucket_name, object_name, expires=expires, version_id=version_id)


_minio_client = _MinIOClient(endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY)


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
            _minio_client.client.make_bucket(bucket_info.bucket_name, object_lock=bucket_info.object_lock)
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
                 prefix: str = None,
                 recursive: bool = False,
                 start_after: bool = None) -> APIResponseModel:
    try:
        result = _minio_client.list_objects(bucket_name, prefix=prefix, recursive=recursive, start_after=start_after)
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
        result = _minio_client.presigned_get_object(bucket_name, object_info.object_name, expires=object_info.expires,
                                                    version_id=object_info.version_id)
    except MinioException as me:
        return response_error(me)
    return response_success(result)
