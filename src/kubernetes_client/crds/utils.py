import json
import yaml

from kubernetes.client.rest import ApiException

from src.kubernetes_client.models import Metadata
from src.models import APIResponseModel


class Render:

    @staticmethod
    def _to_status_list(model, to_each_shape: callable):
        result = []
        if 'items' not in model:
            return {"result": [to_each_shape(model)]}
        for item in model['items']:
            result.append(to_each_shape(item))
        return {"result": result}

    @staticmethod
    def to_no_content(model):
        return {"result": ['no content']}

    @staticmethod
    def metadata_of(item: dict):
        # key-value 형태로 반환
        return Metadata(
            name=item['metadata']['name'],
            labels=item['metadata']['labels'],
            annotations=item['metadata']['annotations'],
            create_date=item['metadata']['creationTimestamp'],
        )

    @staticmethod
    def to_notebook_status_list(model):
        return Render._to_status_list(model, Render.to_notebook_status)

    @staticmethod
    def to_notebook_status(item: dict):
        metadata = Render.metadata_of(item)
        namespace = item['metadata']['namespace']
        containers = item['spec']['template']['spec']['containers']
        notebook = containers[0]

        if 'nvidia.com/gpu' not in notebook['resources']['limits']:
            notebook['resources']['limits']['nvidia.com/gpu'] = 0

        return {
            "status": item['status']['containerState'],
            "name": metadata.name,
            "created_at": metadata.create_date,
            "image": notebook['image'],
            "gpus": notebook['resources']['limits']['nvidia.com/gpu'],
            "cpus": notebook['resources']['limits']['cpu'],
            "memory": notebook['resources']['limits']['memory'],
            "connect": get_connect_uri(namespace, metadata.name),
            "delete": get_delete_uri(namespace, metadata.name),
        }

    @staticmethod
    def to_notebook_details(model):
        label_selector = f"notebook-name={model['metadata']['name']}"
        namespace = model['metadata']['namespace']
        name = model['metadata']['name']
        return {
            "result": {
                "status": get_status_uri(namespace, label_selector),
                "overview": get_overview_uri(namespace, name),
                "logs": get_logs_uri(namespace, label_selector),
                "connect": get_connect_uri(namespace, name),
                "delete": get_delete_uri(namespace, name),
                "yaml": to_yaml(model),
            }
        }

    @staticmethod
    def to_notebook_overview(item: dict):
        metadata = Render.metadata_of(item)
        _spec = item['spec']['template']['spec']
        _notebook = _spec['containers'][0]
        volumes = _spec['volumes']
        image = _notebook['image']
        conditions = item['status']['conditions']
        return {
            "result": {
                "name": metadata.name,
                "labels": metadata.labels,
                "annotations": metadata.annotations,
                "image": image,
                "min_cpu": _notebook['resources']['requests']['cpu'],
                "max_cpu": _notebook['resources']['limits']['cpu'],
                "min_memory": _notebook['resources']['requests']['memory'],
                "max_memory": _notebook['resources']['limits']['memory'],
                "min_gpu": _notebook['resources']['requests']['nvidia.com/gpu'],
                "max_gpu": _notebook['resources']['limits']['nvidia.com/gpu'],
                "create_date": metadata.create_date,
                "volumes": volumes,
                "conditions": conditions,
            }
        }


def get_connect_uri(namespace: str, name: str):
    from src import app_config
    return f"{app_config.NOTEBOOK_HOST}/notebook/{namespace}/{name}/lab"


def get_delete_uri(namespace: str, name: str):
    return f"/crds/namespaces/{namespace}/notebooks/{name}"


def get_status_uri(namespace: str, label_selector: str):
    return f"/cluster/namespaces/{namespace}/pods/?label_selector={label_selector}"


def get_overview_uri(namespace: str, name: str):
    return f"/crds/namespaces/{namespace}/notebooks/{name}/overview"


def get_logs_uri(namespace: str, label_selector: str):
    return f"/cluster/namespaces/{namespace}/logs/?label_selector={label_selector}"


def to_yaml(notebook: dict):
    return yaml.dump(notebook).split('\n')


def error_with_message(e: ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = None):
    if shape_callable is None:
        return {"result": model}
    return shape_callable(model)


