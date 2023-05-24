from kubernetes import config
from src import app_config


def load_cluster_config():
    config.load_kube_config(config_file=app_config.CLUSTER_KUBE_CONFIG_PATH)


def get_nfs_config():
    nfs_server = app_config.CLUSTER_VOLUME_NFS_SERVER
    nfs_path = app_config.CLUSTER_VOLUME_NFS_PATH
    return nfs_server, nfs_path


