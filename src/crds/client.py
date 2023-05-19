from kubernetes import client


class ClientFactory:

    @staticmethod
    def create_api_client():
        return client.ApiClient()

    @staticmethod
    def create_crd_client():
        return client.CustomObjectsApi()


class ClientTemplateFactory:

    @staticmethod
    def build_namespace(namespace: str, labels=None):
        return client.V1Namespace(
            metadata=client.V1ObjectMeta(
                name=namespace,
                labels=labels
            )
        )