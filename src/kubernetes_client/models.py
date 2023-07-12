from enum import Enum
from typing import List, Optional, Mapping

from pydantic import BaseModel
from pydantic.schema import datetime


class Metadata(BaseModel):
    name: str
    labels: Optional[dict] = None
    annotations: Optional[dict] = None
    create_date: datetime = None


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
    env: Optional[dict] = None
    args: Optional[List[str]] = None
    command: Optional[List[str]] = None
    volume_mounts: Optional[List[ContainerVolumeMounts]] = None
    cpu: str = '0.5'
    memory: str = '1Gi'
    gpu: str = '0'


class Pod(BaseModel):
    metadata: Metadata
    containers: List[Container]
    image_pull_secrets: Optional[List[str]] = None
    volumes: Optional[List[ContainerVolume]] = None
    service_account_name: Optional[str] = None


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
    node_port: Optional[int] = None
    protocol: str = 'TCP'


class Service(BaseModel):
    metadata: Metadata
    type: ServiceType = ServiceType.ClusterIP
    ports: List[ServicePort]
    selectors: dict = {}


class IngressPath(BaseModel):
    path: str
    path_type: str = 'Prefix'
    service_name: Optional[str] = None
    service_port: int


class IngressRule(BaseModel):
    host: str
    paths: List[IngressPath]


class Ingress(BaseModel):
    metadata: Metadata
    ingress_class_name: str = 'nginx'
    rules: List[IngressRule]


class Notebook(BaseModel):
    metadata: Metadata
    template_pod: Pod


class Experiment(BaseModel):
    name: str
    description: Optional[str] = None


class Pipeline(BaseModel):
    pipeline_name: str
    pipeline_package_path: str
    description: Optional[str] = None


class PipelineVersion(BaseModel):
    pipeline_version_name: str
    pipeline_package_path: str
    pipeline_id: Optional[str] = None
    pipeline_name: Optional[str] = None
    description: Optional[str] = None


class Run(BaseModel):
    pipeline_file: str
    arguments: Mapping[str, str]
    run_name: Optional[str] = None
    experiment_name: Optional[str] = None
    pipeline_root: Optional[str] = None
    enable_caching: Optional[bool] = None


class RecurringRun(BaseModel):
    experiment_id: str
    job_name: str
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    interval_second: Optional[int] = None
    cron_expression: Optional[str] = None
    max_concurrency: Optional[int] = 1
    no_catchup: Optional[bool] = None
    params: Optional[dict] = None
    pipeline_package_path: Optional[str] = None
    pipeline_id: Optional[str] = None
    version_id: Optional[str] = None
    enabled: bool = True
    enable_caching: Optional[bool] = None

