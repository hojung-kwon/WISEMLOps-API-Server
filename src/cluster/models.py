from enum import Enum
from typing import List

from pydantic import BaseModel
from pydantic.schema import datetime


class Metadata(BaseModel):
    name: str
    labels: dict = {}
    annotations: dict = {}
    create_date: datetime | None = None


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
    metadata: Metadata
    data: dict = {}


class Secret(BaseModel):
    metadata: Metadata
    type: str = 'Opaque'
    data: dict = {}


class ContainerVolumeMounts(BaseModel):
    name: str
    mount_path: str = '/home/volume'


class ContainerVolumeType(Enum):
    PersistentVolumeClaim = 'pvc'
    Secret = 'secret'
    ConfigMap = 'configmap'
    EmptyDir = 'emptydir'


class ContainerVolume(BaseModel):
    name: str
    type: ContainerVolumeType = ContainerVolumeType.PersistentVolumeClaim
    type_name: str


class Container(BaseModel):
    name: str
    image: str = 'nginx'
    image_pull_policy: str = 'IfNotPresent'
    env: dict | None
    args: List[str] | None = []
    command: List[str] | None = []
    volume_mounts: List[ContainerVolumeMounts] | None
    cpu: str = '0.5'
    memory: str = '1Gi'
    gpu: str | None = '0'


class Pod(BaseModel):
    metadata: Metadata
    containers: List[Container]
    image_pull_secrets: List[str] | None = []
    volumes: List[ContainerVolume] | None = []
    service_account_name: str | None = ""


class Deployment(BaseModel):
    metadata: Metadata
    replicas: int = 1
    template_pod: Pod


class ServiceType(Enum):
    ClusterIP = 'ClusterIP'
    NodePort = 'NodePort'
    LoadBalancer = 'LoadBalancer'


class ServicePort(BaseModel):
    name: str
    port: int
    target_port: int
    node_port: int | None = None
    protocol: str = 'TCP'


class Service(BaseModel):
    metadata: Metadata
    type: ServiceType = ServiceType.ClusterIP
    ports: List[ServicePort]
    selectors: dict = {}


class IngressPath(BaseModel):
    path: str
    path_type: str = 'Prefix'
    service_name: str | None = None
    service_port: int


class IngressRule(BaseModel):
    host: str
    paths: List[IngressPath]


class Ingress(BaseModel):
    metadata: Metadata
    ingress_class_name: str = 'nginx'
    rules: List[IngressRule]