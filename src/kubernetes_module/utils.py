import base64

import yaml

from src.kubernetes_module.config import get_cluster_host


def render(model, shape_callable: callable):
    return shape_callable(model)


def encode_to_base64(dict_data: dict):
    return {key: base64.b64encode(value.encode('utf-8')).decode('utf-8') for key, value in dict_data.items()}


def to_yaml(item: dict):
    return yaml.dump(item).split('\n')


def get_connect_uri(namespace: str, name: str):
    return f"{get_cluster_host()}/notebook/{namespace}/{name}/lab"


def get_delete_uri(namespace: str, name: str):
    return f"/crds/namespaces/{namespace}/notebooks/{name}"


def get_status_uri(namespace: str, label_selector: str):
    return f"/cluster/namespaces/{namespace}/pods/?label_selector={label_selector}"


def get_overview_uri(namespace: str, name: str):
    return f"/crds/namespaces/{namespace}/notebooks/{name}/overview"


def get_logs_uri(namespace: str, label_selector: str):
    return f"/cluster/namespaces/{namespace}/logs/?label_selector={label_selector}"
