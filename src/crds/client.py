from kubernetes import client

from src.kubernetes_client.client import ResourceFactory
from src.crds.models import Notebook


class ClientFactory:

    @staticmethod
    def create_api_client():
        return client.ApiClient()

    @staticmethod
    def create_crd_client():
        return client.CustomObjectsApi()


class CrdTemplateFactory:

    @staticmethod
    def build_notebook(notebook: Notebook):
        notebook.metadata.labels.update({
            "access-ml-pipeline": "true",
            "sidecar.istio.io/inject": "true"
        })
        notebook.metadata.annotations.update({
            "notebooks.kubeflow.org/server-type": "jupyter"
        })
        return {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "Notebook",
            "metadata": ResourceFactory.build_metadata(notebook.metadata),
            "spec": {
                "template": ResourceFactory.build_pod(notebook.template_pod)
            }
        }



