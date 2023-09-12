from kubernetes.client import ApiClient, CustomObjectsApi
from kubernetes.client.rest import ApiException

from src.kubernetes_module.crds.render import Render
from src.kubernetes_module.exceptions import KubernetesApiError
from src.kubernetes_module.resource import ResourceFactory
from src.kubernetes_module.schemas import Notebook
from src.kubernetes_module.utils import render


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
            return render(result, Render.to_notebook_status_list)
        except ApiException as e:
            raise KubernetesApiError(e)

    def create_notebook(self, namespace: str, notebook: Notebook):
        try:
            body = ResourceFactory.build_notebook(notebook)
            result = self.crd_client.create_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                body=body
            )
            return render(result, Render.to_no_content)
        except ApiException as e:
            raise KubernetesApiError(e)

    def delete_notebook(self, namespace: str, name: str):
        try:
            result = self.crd_client.delete_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return render(result, Render.to_no_content)
        except ApiException as e:
            raise KubernetesApiError(e)

    def get_notebook(self, namespace: str, name: str):
        try:
            result = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return render(result, Render.to_notebook_details)
        except ApiException as e:
            raise KubernetesApiError(e)

    def get_notebook_overview(self, namespace: str, name: str):
        try:
            result = self.crd_client.get_namespaced_custom_object(
                group="kubeflow.org", version="v1alpha1",
                plural="notebooks",
                namespace=namespace,
                name=name
            )
            return render(result, Render.to_notebook_overview)
        except ApiException as e:
            raise KubernetesApiError(e)
