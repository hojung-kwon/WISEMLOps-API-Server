from kubernetes import client
import os

# 클러스터 환경 변수
CLUSTER_URL = 'https://211.39.140.43:6443'
BEARER_TOKEN_FILE = open(os.environ['CERTS_PATH'] + 'bearer_token').read()
CA_CERT_PATH = os.environ['CERTS_PATH'] + 'k8s-ca.cert'

# NFS 환경 변수
VOLUME_NFS_SERVER = '211.39.140.43'
VOLUME_NFS_PATH = '/home/wisenut/nfs4share'


def _create_config(ssl_ca_cert_path, bearer_token_file, cluster_url):
    # Kubernetes 클러스터 구성 가져오기
    _config = client.Configuration()
    _config.host = cluster_url
    _config.api_key['authorization'] = bearer_token_file
    _config.api_key_prefix['authorization'] = 'Bearer'
    _config.ssl_ca_cert = ssl_ca_cert_path
    _config.verify_ssl = True

    return _config


CLUSTER_CONFIG = _create_config(CA_CERT_PATH, BEARER_TOKEN_FILE, CLUSTER_URL)
