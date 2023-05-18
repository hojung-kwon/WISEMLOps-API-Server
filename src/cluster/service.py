import ssl

from kubernetes import client
from src.cluster.client import create_client, create_custom_api, template_pv, template_namespace, template_pvc, \
    template_configmap, template_secret, template_pod
from src.cluster.models import Volume, VolumeClaim, ConfigMap, Secret, Pod
from src.cluster.utils import response, error_with_message, success_with_no_content, success_with_name_list, \
    success_with_node_status, success_with_volume_status, success_with_volume_claim_status, \
    success_with_config_map_status, success_with_secret_status, encode_to_base64, success_with_pod_status

ssl._create_default_https_context = ssl._create_unverified_context


class ClusterService:
    def __init__(self):
        # Kubernetes API 클라이언트 생성
        self.cluster_client = create_client()
        self.cluster_crd_client = create_custom_api()
        pass

    def get_nodes(self):
        try:
            result = self.cluster_client.list_node()
            return response(result, success_with_node_status)
        except client.ApiException as e:
            return error_with_message(e)

    def get_namespaces(self):
        try:
            result = self.cluster_client.list_namespace()
            return response(result, success_with_name_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_namespace(self, namespace: str, labels: dict = None, istio: bool = False):
        try:
            labels['istio-injection'] = 'enabled' if istio else 'disabled'
            body = template_namespace(namespace, labels)
            result = self.cluster_client.create_namespace(body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_namespace(self, namespace: str):
        try:
            result = self.cluster_client.delete_namespace(name=namespace)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def update_namespace(self, namespace: str, labels: dict = None, istio: bool = False):
        try:
            labels['istio-injection'] = 'enabled' if istio else 'disabled'
            body = template_namespace(namespace, labels)
            result = self.cluster_client.patch_namespace(name=namespace, body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_volumes(self):
        try:
            result = self.cluster_client.list_persistent_volume()
            return response(result, success_with_volume_status)
        except client.ApiException as e:
            return error_with_message(e)

    def create_volume(self, pv: Volume):
        try:
            body = template_pv(pv)
            result = self.cluster_client.create_persistent_volume(body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_volume(self, name):
        try:
            result = self.cluster_client.delete_persistent_volume(name=name)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_volume_claims(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_persistent_volume_claim(namespace=namespace)
            return response(result, success_with_volume_claim_status)
        except client.ApiException as e:
            return error_with_message(e)

    def create_volume_claim(self, namespace: str, pvc: VolumeClaim):
        try:
            body = template_pvc(pvc)
            result = self.cluster_client.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_volume_claim(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_config_maps(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_config_map(namespace=namespace)
            return response(result, success_with_config_map_status)
        except client.ApiException as e:
            return error_with_message(e)

    def create_config_map(self, namespace: str, config_map: ConfigMap):
        try:
            body = template_configmap(config_map)
            result = self.cluster_client.create_namespaced_config_map(namespace=namespace, body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_config_map(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_config_map(name=name, namespace=namespace)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_secrets(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_secret(namespace=namespace)
            return response(result, success_with_secret_status)
        except client.ApiException as e:
            return error_with_message(e)

    def create_secret(self, namespace: str, secret: Secret):
        try:
            secret.data = encode_to_base64(secret.data)
            body = template_secret(secret)
            result = self.cluster_client.create_namespaced_secret(namespace=namespace, body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_secret(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_secret(name=name, namespace=namespace)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_pods(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_pod(namespace=namespace)
            return response(result, success_with_pod_status)
        except client.ApiException as e:
            return error_with_message(e)

    def create_pod(self, namespace: str, pod: Pod):
        try:
            body = template_pod(pod)
            result = self.cluster_client.create_namespaced_pod(namespace=namespace, body=body)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_pod(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_pod(name=name, namespace=namespace)
            return response(result, success_with_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_services(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_service(namespace=namespace)
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)


cluster_service = ClusterService()