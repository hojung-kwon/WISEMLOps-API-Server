from kubernetes import client
from src.crds.client import ClientFactory
from src.crds.utils import Render, response, error_with_message


class CrdService:
    def __init__(self):
        self.api_client = ClientFactory.create_api_client()
        self.crd_client = ClientFactory.create_crd_client()
        pass

    def get_notebooks(self, namespace: str):
        try:
            result = self.crd_client.list_namespaced_custom_object(
                group="kubeflow.org",
                version="v1alpha1",
                plural="notebooks",
                namespace=namespace
            )
            return response(result, Render.to_notebook_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def get_notebook(self, namespace: str, name: str):
        try:
            result = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org",
                version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return response(result, Render.to_notebook_status_list)
        except client.ApiException as e:
            return error_with_message(e)