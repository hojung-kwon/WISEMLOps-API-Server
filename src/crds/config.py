from kubernetes import client


class ClusterClientFactory:

    @staticmethod
    def create_client():
        return client.CoreV1Api()

    @staticmethod
    def create_deployment_client():
        return client.AppsV1Api()

    @staticmethod
    def create_networking_api():
        return client.NetworkingV1Api()