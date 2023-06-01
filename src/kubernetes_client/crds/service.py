from kubernetes.client import ApiClient, CustomObjectsApi
from kubernetes.client.rest import ApiException

from src.kubernetes_client.client import ResourceFactory
from src.kubernetes_client.crds.utils import Render
from src.kubernetes_client.models import Notebook
from src.kubernetes_client.utils import response, error_with_message


class CrdService:
    def __init__(self, api_client: ApiClient, crd_client: CustomObjectsApi):
        self.api_client = api_client
        self.crd_client = crd_client
        pass

    def get_notebooks(self, namespace: str):
        try:
            result = self.crd_client.list_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace
            )
            return response(result, Render.to_notebook_status_list)
        except ApiException as e:
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
        except ApiException as e:
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
        except ApiException as e:
            return error_with_message(e)

    def get_notebook(self, namespace: str, name: str):
        try:
            result = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return response(result, Render.to_notebook_details)
        except ApiException as e:
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
        except ApiException as e:
            return error_with_message(e)

