from kubernetes import client


class ClientFactory:
    @staticmethod
    def get_core_client():
        return client.CoreV1Api()

    @staticmethod
    def get_deployment_client():
        return client.AppsV1Api()

    @staticmethod
    def get_networking_client():
        return client.NetworkingV1Api()

    @staticmethod
    def get_api_client():
        return client.ApiClient()

    @staticmethod
    def create_crd_client():
        return client.CustomObjectsApi()
