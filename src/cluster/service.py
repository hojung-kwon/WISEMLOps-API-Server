import ssl

from kubernetes import client
from src.cluster.client import create_client, create_custom_api, template_pv
from src.cluster.utils import response, error_with_message, success_with_no_content, success_with_name_list

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
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_pods(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_pod(namespace=namespace)
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_namespaces(self):
        try:
            result = self.cluster_client.list_namespace()
            return response(result, success_with_name_list)
        except client.ApiException as e:
            return error_with_message(e)

    def get_services(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_service(namespace=namespace)
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_secrets(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_secret(namespace=namespace)
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_volumes(self):
        try:
            result = self.cluster_client.list_persistent_volume()
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def create_volume(self, name, size, volume_mode, access_mode, storage_class, policy, volume_type):
        try:
            body = template_pv(name, size, volume_mode, access_mode, storage_class, policy, volume_type)
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
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_config_maps(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_config_map(namespace=namespace)
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def create_namespace(self, namespace: str):
        try:
            body = client.V1Namespace()
            body.metadata = client.V1ObjectMeta(name=namespace)
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


cluster_service = ClusterService()