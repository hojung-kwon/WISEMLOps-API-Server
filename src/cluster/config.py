from kubernetes import client, config
from src.config import app_config


def create_config():
    # Kubernetes 클러스터 구성 가져오기
    _config = client.Configuration()
    _config.host = app_config.CLUSTER_HOST
    _config.api_key['authorization'] = app_config.CLUSTER_BEARER_TOKEN_PATH
    _config.api_key_prefix['authorization'] = 'Bearer'
    _config.ssl_ca_cert = app_config.CLUSTER_CA_CERT_PATH
    _config.verify_ssl = True

    return _config


def load_config():
    config.load_kube_config(config_file=app_config.CLUSTER_KUBE_CONFIG_PATH)
    return None
