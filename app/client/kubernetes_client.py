from kubernetes import client
import kfp
import ssl
import os
ssl._create_default_https_context = ssl._create_unverified_context

# 환경변수 설정
currentPath = os.getcwd()
CLUSTER_URL = 'https://211.39.140.43:6443'
BEARER_TOKEN = open(currentPath + '\\client\\bearer_token').read()
CA_CERT = currentPath + '\\client\\k8s-ca.cert'

# Kubernetes 클러스터 구성 가져오기
config = client.Configuration()
config.host = CLUSTER_URL
config.api_key['authorization'] = BEARER_TOKEN
config.api_key_prefix['authorization'] = 'Bearer'
config.ssl_ca_cert = CA_CERT
config.verify_ssl = True

# Kubernetes API 클라이언트 생성
k8s_client = client.CoreV1Api(api_client=client.ApiClient(config))

# Kubeflow Pipeline 클라이언트 생성
kfp_client = kfp.Client(
    host=CLUSTER_URL,
    existing_token=BEARER_TOKEN,
    ssl_ca_cert=CA_CERT,
    namespace='kubeflow',
    verify_ssl=True
)