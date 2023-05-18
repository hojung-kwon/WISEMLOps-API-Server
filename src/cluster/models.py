

from pydantic import BaseModel
from pydantic.schema import datetime


class Metadata(BaseModel):
    name: str
    create_date: datetime
    annotations: dict | None
    labels: dict | None
    api_version: str | None


class Volume(BaseModel):
    name: str
    storage_class: str = 'default-storage-class'
    storage_size: str = '3Gi'
    access_mode: str = 'ReadWriteOnce'
    volume_mode: str = 'Filesystem'
    policy: str = 'Delete'
    volume_type: str = 'nfs'


class VolumeClaim(BaseModel):
    name: str
    storage_class: str = 'default-storage-class'
    storage_size: str = '3Gi'
    access_mode: str = 'ReadWriteOnce'


class ConfigMap(BaseModel):
    name: str
    data: dict = {}
    labels: dict = {}
    namespace: str = 'default'