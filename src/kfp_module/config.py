from src import app_config

MODULE_CODE = 101


def get_kube_config_path():
    return app_config.CLUSTER_KUBE_CONFIG_PATH


def get_kubeflow_pipelines_endpoint():
    return app_config.KUBEFLOW_PIPELINES_ENDPOINT
