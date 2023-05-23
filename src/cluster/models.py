from enum import Enum
from typing import List

from pydantic import BaseModel


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
    name: str
    labels: dict = {}
    annotations: dict = {}
    containers: List[Container]
    image_pull_secrets: List[str] | None = []
    volumes: List[ContainerVolume] | None = []
    service_account_name: str | None = ""


class Deployment(BaseModel):
    name: str
    replicas: int = 1
    labels: dict = {}
    annotations: dict = {}
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
    name: str
    labels: dict = {}
    type: ServiceType = ServiceType.ClusterIP
    ports: List[ServicePort]


class IngressPath(BaseModel):
    path: str
    path_type: str = 'Prefix'
    service_name: str | None = None
    service_port: int


class IngressRule(BaseModel):
    host: str
    paths: List[IngressPath]


class Ingress(BaseModel):
    name: str
    labels: dict = {}
    annotations: dict = {'nginx.ingress.kubernetes.io/rewrite-target': '/'}
    ingress_class_name: str = 'nginx'
    rules: List[IngressRule]