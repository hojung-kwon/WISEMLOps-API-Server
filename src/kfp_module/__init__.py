from kubernetes import config, client

from src import app_config
from src.kfp_module.service import KfpService

config.load_kube_config(config_file=app_config.CLUSTER_KUBE_CONFIG_PATH)
KUBEFLOW_PIPELINES_ENDPOINT = app_config.KUBEFLOW_PIPELINES_ENDPOINT

kfp_service = KfpService(
    host=KUBEFLOW_PIPELINES_ENDPOINT,
    cluster_client=client.CoreV1Api()
)
