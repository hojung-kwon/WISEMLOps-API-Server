from datetime import timedelta
from typing import Optional

from minio import Minio

from src.minio_module.schemas import BucketInfo, ObjectInfo


class MinIOService:
    def __init__(self, endpoint, access_key, secret_key):
        endpoint_split = endpoint.split("://")
        self.endpoint = endpoint_split[-1]
        self.access_key = access_key
        self.secret_key = secret_key
        self.secure = True if endpoint_split[0] == "https" else False

    def get_client(self):
        return Minio(endpoint=self.endpoint, access_key=self.access_key, secret_key=self.secret_key, secure=self.secure)

    def list_buckets(self):
        client = self.get_client()
        return client.list_buckets()

    def bucket_exists(self, bucket_name: str):
        client = self.get_client()
        return client.bucket_exists(bucket_name)

    def make_bucket(self, bucket_info: BucketInfo):
        client = self.get_client()
        available = not client.bucket_exists(bucket_info.bucket_name)
        if available:
            client.make_bucket(bucket_info.bucket_name, object_lock=bucket_info.object_lock)
        return available

    def remove_bucket(self, bucket_name: str):
        client = self.get_client()
        available = client.bucket_exists(bucket_name)
        if available:
            client.remove_bucket(bucket_name)
        return available

    def list_objects(self, bucket_name: str,
                     prefix: Optional[str] = None,
                     recursive: bool = False,
                     start_after: Optional[str] = None):
        client = self.get_client()
        return [*client.list_objects(bucket_name, prefix=prefix, recursive=recursive, start_after=start_after)]

    def fget_object(self, bucket_name: str,
                    object_info: ObjectInfo):
        client = self.get_client()
        if object_info.file_path is None:
            object_info.file_path = object_info.object_name
        return client.fget_object(bucket_name, object_info.object_name, object_info.file_path,
                                  version_id=object_info.version_id)

    def fput_object(self, bucket_name: str,
                    object_info: ObjectInfo):
        client = self.get_client()
        return client.fput_object(bucket_name, object_info.object_name, object_info.file_path)

    def stat_object(self, bucket_name: str,
                    object_info: ObjectInfo):
        client = self.get_client()
        return client.stat_object(bucket_name, object_info.object_name, version_id=object_info.version_id)

    def remove_object(self, bucket_name: str,
                      object_info: ObjectInfo):
        client = self.get_client()
        client.remove_object(bucket_name, object_info.object_name, version_id=object_info.version_id)
        return None

    def presigned_get_object(self, bucket_name: str,
                             object_info: ObjectInfo):
        client = self.get_client()
        if object_info.expire_days > 7 or object_info.expire_days < 1:
            expires = timedelta(days=7)
        else:
            expires = timedelta(days=object_info.expire_days)
        return client.presigned_get_object(bucket_name, object_info.object_name, expires=expires,
                                           version_id=object_info.version_id)
