from typing import Optional

from pydantic import BaseModel


class BucketInfo(BaseModel):
    bucket_name: str
    object_lock: bool = False


class ObjectInfo(BaseModel):
    object_name: str
    file_path: Optional[str] = None
    expire_days: int = 7
    version_id: Optional[str] = None
