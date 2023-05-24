from kubernetes.client import CoreV1Api, AppsV1Api, NetworkingV1Api, ApiException

from src.kubernetes_client.client import ResourceFactory as Factory
from src.kubernetes_client.cluster.utils import Render, response, error_with_message, encode_to_base64
from src.kubernetes_client.models import Volume, VolumeClaim, ConfigMap, Secret, \
    Pod, Deployment, Service, Ingress, Metadata


class ClusterService:
    def __init__(self,
                 cluster_client: CoreV1Api,
                 deployment_client: AppsV1Api,
                 network_client: NetworkingV1Api):
        # Kubernetes API 클라이언트 생성
        self.cluster_client = cluster_client
        self.deployment_client = deployment_client
        self.network_client = network_client
        pass

    def get_nodes(self):
        try:
            result = self.cluster_client.list_node()
            return response(result, Render.to_node_status_list)
        except ApiException as e:
            return error_with_message(e)

    def get_namespaces(self):
        try:
            result = self.cluster_client.list_namespace()
            return response(result, Render.to_name_list)
        except ApiException as e:
            return error_with_message(e)

    def create_namespace(self, metadata: Metadata):
        try:
            body = Factory.build_namespace(metadata)
            result = self.cluster_client.create_namespace(body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_namespace(self, namespace: str):
        try:
            result = self.cluster_client.delete_namespace(name=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def update_namespace(self, metadata: Metadata):
        try:
            body = Factory.build_namespace(metadata)
            result = self.cluster_client.patch_namespace(name=metadata.name, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_volumes(self):
        try:
            result = self.cluster_client.list_persistent_volume()
            return response(result, Render.to_volume_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_volume(self, pv: Volume):
        try:
            body = Factory.build_pv(pv)
            result = self.cluster_client.create_persistent_volume(body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_volume(self, name):
        try:
            result = self.cluster_client.delete_persistent_volume(name=name)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_volume_claims(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_persistent_volume_claim(namespace=namespace)
            return response(result, Render.to_volume_claim_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_volume_claim(self, namespace: str, pvc: VolumeClaim):
        try:
            body = Factory.build_pvc(pvc)
            result = self.cluster_client.create_namespaced_persistent_volume_claim(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_volume_claim(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_persistent_volume_claim(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_config_maps(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_config_map(namespace=namespace)
            return response(result, Render.to_configmap_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_config_map(self, namespace: str, config_map: ConfigMap):
        try:
            body = Factory.build_configmap(config_map)
            result = self.cluster_client.create_namespaced_config_map(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_config_map(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_config_map(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_secrets(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_secret(namespace=namespace)
            return response(result, Render.to_secret_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_secret(self, namespace: str, secret: Secret):
        try:
            secret.data = encode_to_base64(secret.data)
            body = Factory.build_secret(secret)
            result = self.cluster_client.create_namespaced_secret(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_secret(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_secret(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_pods(self, namespace: str = 'default', label_selector: str = None):
        try:
            result = self.cluster_client.list_namespaced_pod(
                namespace=namespace,
                label_selector=label_selector
            )
            return response(result, Render.to_pod_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_pod(self, namespace: str, pod: Pod):
        try:
            body = Factory.build_pod(pod)
            result = self.cluster_client.create_namespaced_pod(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_pod(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_pod(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def find_specific_pod_logs(self, namespace: str = 'default', label_selector: str = None):
        try:
            read_pod_result = self.cluster_client.list_namespaced_pod(
                namespace=namespace,
                label_selector=label_selector,
            )
            result = {}
            if len(read_pod_result.items) == 0:
                return response(result, Render.to_no_content)

            pod = read_pod_result.items[0]
            for container in pod.spec.containers:
                logs = self.cluster_client.read_namespaced_pod_log(
                    namespace=namespace,
                    name=pod.metadata.name,
                    container=container.name,
                )
                result[container.name] = logs
            return response(result, Render.to_pod_logs)
        except ApiException as e:
            return error_with_message(e)

    def get_pod_logs(self, namespace: str = 'default', name: str = ''):
        try:
            read_pod_result = self.cluster_client.read_namespaced_pod(namespace=namespace, name=name)
            result = {}
            for container in read_pod_result.spec.containers:
                logs = self.cluster_client.read_namespaced_pod_log(
                    namespace=namespace,
                    name=name,
                    container=container.name,
                )
                result[container.name] = logs
            return response(result, Render.to_pod_logs)
        except ApiException as e:
            return error_with_message(e)

    def get_container_logs(self, namespace: str = 'default', name: str = '', container: str = ''):
        try:
            result = self.cluster_client.read_namespaced_pod_log(
                namespace=namespace,
                name=name,
                container=container,
            )
            return response(result, Render.to_container_logs)
        except ApiException as e:
            return error_with_message(e)

    def get_deployments(self, namespace: str = 'default'):
        try:
            result = self.deployment_client.list_namespaced_deployment(namespace=namespace)
            return response(result, Render.to_deployment_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_deployment(self, namespace: str, deployment: Deployment):
        try:
            body = Factory.build_deployment(deployment)
            result = self.deployment_client.create_namespaced_deployment(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_deployment(self, namespace: str, name: str):
        try:
            result = self.deployment_client.delete_namespaced_deployment(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_services(self, namespace: str = 'default'):
        try:
            result = self.cluster_client.list_namespaced_service(namespace=namespace)
            return response(result, Render.to_service_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_service(self, namespace: str, service: Service):
        try:
            body = Factory.build_service(service)
            result = self.cluster_client.create_namespaced_service(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_service(self, namespace: str, name: str):
        try:
            result = self.cluster_client.delete_namespaced_service(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def get_ingresses(self, namespace: str = 'default'):
        try:
            result = self.network_client.list_namespaced_ingress(namespace=namespace)
            return response(result, Render.to_ingress_status_list)
        except ApiException as e:
            return error_with_message(e)

    def create_ingress(self, namespace: str, ingress: Ingress):
        try:
            body = Factory.build_ingress(ingress)
            result = self.network_client.create_namespaced_ingress(namespace=namespace, body=body)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

    def delete_ingress(self, namespace: str, name: str):
        try:
            result = self.network_client.delete_namespaced_ingress(name=name, namespace=namespace)
            return response(result, Render.to_no_content)
        except ApiException as e:
            return error_with_message(e)

