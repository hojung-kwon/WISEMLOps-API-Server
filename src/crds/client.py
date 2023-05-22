from kubernetes import client

from src.cluster.client import ClientTemplateFactory
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
    def build_namespace(namespace: str, labels=None):
        return client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=namespace,
                labels=labels
            )
        )

    @staticmethod
    def build_notebook(notebook: Notebook):
        template_pod = ClientTemplateFactory.build_pod(notebook.template_pod).spec
        return {
            "apiVersion": "kubeflow.org/v1alpha1",
            "kind": "Notebook",
            "metadata": {
                "name": notebook.name,
                "labels": notebook.labels
            },
            "spec": {
                "template": {
                    "spec": template_pod
                },
            }
        }



