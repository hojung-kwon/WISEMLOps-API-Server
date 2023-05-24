import yaml
from kubernetes import client
from src.kubernetes_client.crds.utils import Render, response, error_with_message
from src.kubernetes_client.client import ClientFactory, ResourceFactory
from src.kubernetes_client.models import Notebook


class CrdService:
    def __init__(self):
        self.api_client = ClientFactory.create_api_client()
        self.crd_client = ClientFactory.create_crd_client()
        pass

    def get_notebooks(self, namespace: str):
        try:
            result = self.crd_client.list_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace
            )
            return response(result, Render.to_notebook_status_list)
        except client.ApiException as e:
            return error_with_message(e)

    def create_notebook(self, namespace: str, notebook: Notebook):
        try:
            body = ResourceFactory.build_notebook(notebook)
            result = self.crd_client.create_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                body=body
            )
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def delete_notebook(self, namespace: str, name: str):
        try:
            result = self.crd_client.delete_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return response(result, Render.to_no_content)
        except client.ApiException as e:
            return error_with_message(e)

    def get_notebook(self, namespace: str, name: str):
        try:
            notebook = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            label_selector = f"notebook-name={notebook['metadata']['name']}"
            result = [
                {
                    "status": f"/cluster/namespaces/{namespace}/pods/?label_selector={label_selector}",
                    "overview": f"/crds/namespaces/{namespace}/notebooks/{name}/overview",
                    "logs": f"/cluster/namespaces/{namespace}/logs/?label_selector={label_selector}",
                    "yaml": yaml.dump(notebook).split('\n')
                }
            ]
            return response(result)
        except client.ApiException as e:
            return error_with_message(e)

    def get_notebook_overview(self, namespace: str, name: str):
        try:
            result = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return response(result, Render.to_notebook_overview)
        except client.ApiException as e:
            return error_with_message(e)

