from enum import Enum
from typing import List

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
    labels: dict | None = {}


class Secret(BaseModel):
    name: str
    data: dict = {}
    labels: dict = {}
    type: str = 'Opaque'


class ContainerVolumeMounts(BaseModel):
    name: str
    mount_path: str = '/home/volume'


class ContainerVolumeType(Enum):
    PersistentVolumeClaim = 'pvc'
    Secret = 'secret'
    ConfigMap = 'configmap'


class ContainerVolume(BaseModel):
    name: str
    type: ContainerVolumeType = ContainerVolumeType.PersistentVolumeClaim
    type_name: str


class Container(BaseModel):
    name: str
    image: str = 'nginx'
    image_pull_policy: str = 'IfNotPresent'
    env: dict | None
    args: List[str] | None
    command: List[str] | None
    volume_mounts: ContainerVolumeMounts | None


class Pod(BaseModel):
    name: str
    labels: dict = {}
    containers: List[Container]
    image_pull_secrets: List[str] | None
    volumes: List[ContainerVolume] | None
