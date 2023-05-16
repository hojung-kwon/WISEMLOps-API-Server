from kubernetes import client


def create_client(_config):
    return client.CoreV1Api(api_client=client.ApiClient(_config))


def create_custom_api(_config):
    return client.CustomObjectsApi(api_client=client.ApiClient(_config))
