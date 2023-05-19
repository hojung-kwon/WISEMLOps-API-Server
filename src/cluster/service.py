from src.cluster.client import ClusterTemplateFactory as Factory, client
from src.cluster.utils import Render, response, error_with_message, encode_to_base64
from src.cluster.models import \
    Volume, VolumeClaim, \
    ConfigMap, Secret, \
    Pod, Deployment, Service


class ClusterService:
    def __init__(self):
        # Kubernetes API 클라이언트 생성
        self.cluster_client = Factory.create_client()
        self.deployment_client = Factory.create_deployment_client()
        pass

    def get_nodes(self):
        try:
            result = self.cluster_client.list_node()
            return response(result, Render.to_node_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def get_namespaces(self):
        try:
            result = self.cluster_client.list_namespace()
            return response(result, Render.to_name_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_namespace(self, namespace: str, labels: dict = None, istio: bool = False):
        try:
            labels['istio-injection'] = 'enabled' if istio else 'disabled'
            body = Factory.build_namespace(namespace, labels)
            result = self.cluster_client.create_namespace(body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_namespace(self, namespace: str):
        try:
            result = self.cluster_client.delete_namespace(name=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def update_namespace(self, namespace: str, labels: dict = None, istio: bool = False):
        try:
            labels['istio-injection'] = 'enabled' if istio else 'disabled'
            body = Factory.build_namespace(namespace, labels)
            result = self.cluster_client.patch_namespace(name=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_volumes(self):
        try:
            result = self.cluster_client.list_persistent_volume()
            return response(result, Render.to_volume_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_volume(self, pv: Volume):
        try:
            body = Factory.build_pv(pv)
            result = self.cluster_client.create_persistent_volume(body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_volume(self, name):
        try:
            result = self.cluster_client.delete_persistent_volume(name=name)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_volume_claims(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_persistent_volume_claim(namespace=namespace)
            return response(result, Render.to_volume_claim_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_volume_claim(self, namespace: str, pvc: VolumeClaim):
        try:
            body = Factory.build_pvc(pvc)
            result = self.cluster_client.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_volume_claim(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_config_maps(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_config_map(namespace=namespace)
            return response(result, Render.to_configmap_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_config_map(self, namespace: str, config_map: ConfigMap):
        try:
            body = Factory.build_configmap(config_map)
            result = self.cluster_client.create_namespaced_config_map(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_config_map(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_config_map(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_secrets(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_secret(namespace=namespace)
            return response(result, Render.to_secret_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_secret(self, namespace: str, secret: Secret):
        try:
            secret.data = encode_to_base64(secret.data)
            body = Factory.build_secret(secret)
            result = self.cluster_client.create_namespaced_secret(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_secret(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_secret(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_pods(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_pod(namespace=namespace)
            return response(result, Render.to_pod_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_pod(self, namespace: str, pod: Pod):
        try:
            body = Factory.build_pod(pod)
            result = self.cluster_client.create_namespaced_pod(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_pod(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_pod(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_deployments(self, namespace: str = 'default'):
        try:
            result = self.deployment_client.list_namespaced_deployment(namespace=namespace)
            return response(result, Render.to_deployment_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_deployment(self, namespace: str, deployment: Deployment):
        try:
            body = Factory.build_deployment(deployment)
            result = self.deployment_client.create_namespaced_deployment(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_deployment(self, namespace: str, name: str):
        try:
            result = self.deployment_client.delete_namespaced_deployment(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_services(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_service(namespace=namespace)
            return response(result, Render.to_service_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_service(self, namespace: str, service: Service):
        try:
            body = Factory.build_service(service)
            result = self.cluster_client.create_namespaced_service(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_service(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_service(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

