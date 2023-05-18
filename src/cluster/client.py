from kubernetes import client
from src.cluster.config import load_config, create_config
from src.cluster.models import Volume, VolumeClaim, ConfigMap, Secret, Container, Pod, ContainerVolume, \
    ContainerVolumeType
from src.config import app_config


def create_client(with_token: bool = False):
    if with_token:
        return client.CoreV1Api(api_client=client.ApiClient(create_config()))
    else:
        load_config()
        return client.CoreV1Api()


def create_custom_api(with_token: bool = False):
    if with_token:
        return client.CustomObjectsApi(api_client=client.ApiClient(create_config()))
    else:
        load_config()
        return client.CustomObjectsApi()


def template_namespace(namespace: str, labels=None):
    return client.V1Namespace(
        metadata=client.V1ObjectMeta(
            name=namespace,
            labels=labels
        )
    )


def get_nfs_volume():
    return client.V1NFSVolumeSource(
        server=app_config.CLUSTER_VOLUME_NFS_SERVER,
        path=app_config.CLUSTER_VOLUME_NFS_PATH,
        read_only=False
    )


def template_pv(pv: Volume):
    _volume = client.V1PersistentVolume(
        metadata=client.V1ObjectMeta(name=pv.name),
        spec=client.V1PersistentVolumeSpec(
            capacity={'storage': pv.storage_size},
            volume_mode=pv.volume_mode,
            access_modes=[pv.access_mode],
            storage_class_name=pv.storage_class,
            persistent_volume_reclaim_policy=pv.policy,
        )
    )
    if pv.volume_type == 'nfs':
        _volume.spec.nfs = get_nfs_volume()
    return _volume


def template_pvc(pvc: VolumeClaim):
    _claim = client.V1PersistentVolumeClaim(
        metadata=client.V1ObjectMeta(name=pvc.name),
        spec=client.V1PersistentVolumeClaimSpec(
            storage_class_name=pvc.storage_class,
            resources=client.V1ResourceRequirements(
                requests={'storage': pvc.storage_size}
            ),
            access_modes=[pvc.access_mode],
        )
    )
    return _claim


def template_configmap(config_map: ConfigMap):
    return client.V1ConfigMap(
        metadata=client.V1ObjectMeta(
            name=config_map.name,
            labels=config_map.labels
        ),
        data=config_map.data
    )


def template_secret(secret: Secret):
    return client.V1Secret(
        metadata=client.V1ObjectMeta(
            name=secret.name,
            labels=secret.labels
        ),
        data=secret.data,
        type=secret.type
    )


def template_container(container: Container):
    return client.V1Container(
        name=container.name,
        image=container.image,
        image_pull_policy=container.image_pull_policy,
        args=container.args,
        env=[client.V1EnvVar(name=key, value=value) for key, value in container.env.items()],
        command=container.command,
        volume_mounts=[client.V1VolumeMount(
            name=container.volume_mounts.name,
            mount_path=container.volume_mounts.mount_path)],
    )


def template_container_volume(container_volume: ContainerVolume):
    volume = client.V1Volume(name=container_volume.name)

    if container_volume.type == ContainerVolumeType.PersistentVolumeClaim:
        volume.persistent_volume_claim = client.V1PersistentVolumeClaimVolumeSource(claim_name=container_volume.type_name)
    if container_volume.type == ContainerVolumeType.Secret:
        volume.secret = client.V1SecretVolumeSource(secret_name=container_volume.type_name)
    if container_volume.type == ContainerVolumeType.ConfigMap:
        volume.config_map = client.V1ConfigMapVolumeSource(name=container_volume.type_name)

    return volume


def template_image_pull_secrets(secrets: list):
    if secrets is None:
        return None
    return [client.V1LocalObjectReference(name=item) for item in secrets]


def template_pod(pod: Pod):
    return client.V1Pod(
        metadata=client.V1ObjectMeta(
            name=pod.name,
            labels=pod.labels
        ),
        spec=client.V1PodSpec(
            containers=[template_container(container) for container in pod.containers],
            image_pull_secrets=template_image_pull_secrets(pod.image_pull_secrets),
            volumes=[template_container_volume(volume) for volume in pod.volumes],
        )
    )