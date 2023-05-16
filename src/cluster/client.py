from kubernetes import client
from src.cluster.config import VOLUME_NFS_SERVER, VOLUME_NFS_PATH, CLUSTER_CONFIG


def create_client():
    return client.CoreV1Api(api_client=client.ApiClient(CLUSTER_CONFIG))


def create_custom_api():
    return client.CustomObjectsApi(api_client=client.ApiClient(CLUSTER_CONFIG))


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
        server=VOLUME_NFS_SERVER,
        path=VOLUME_NFS_PATH,
        read_only=False
    )


def template_pv(name, size, volume_mode, access_mode, storage_class, policy, volume_type):
    _volume = client.V1PersistentVolume(
        api_version='v1', kind='PersistentVolume',
        metadata=client.V1ObjectMeta(name=name),
        spec=client.V1PersistentVolumeSpec(
            capacity={'storage': size},
            volume_mode=volume_mode,
            access_modes=[access_mode],
            storage_class_name=storage_class,
            persistent_volume_reclaim_policy=policy,
        )
    )
    if volume_type == 'nfs':
        _volume.spec.nfs = get_nfs_volume()
    return _volume