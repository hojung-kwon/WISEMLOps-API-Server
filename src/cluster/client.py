from kubernetes import client
from src.cluster.config import load_config, create_config
from src.cluster.models import Volume, VolumeClaim
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


def template_metadata(name: str, namespace: str = 'default', labels=None):
    return client.V1ObjectMeta(
        name=name,
        namespace=namespace,
        labels=labels
    )


def template_namespace(namespace: str, labels=None):
    return client.V1Namespace(
        metadata=template_metadata(name=namespace, labels=labels)
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