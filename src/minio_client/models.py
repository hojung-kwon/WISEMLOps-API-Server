from pydantic import BaseModel
from datetime import timedelta


class BucketInfo(BaseModel):
    bucket_name: str
    object_lock: bool | None = False


class ObjectInfo(BaseModel):
    object_name: str
    file_path: str | None = None
    expires: timedelta | None = timedelta(days=7)
    version_id: str | None = None
