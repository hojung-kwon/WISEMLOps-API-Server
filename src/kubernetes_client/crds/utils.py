import json

from kubernetes import client

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
        containers = item['spec']['template']['spec']['containers']
        notebook = containers[0]

        if 'nvidia.com/gpu' not in notebook['resources']['limits']:
            notebook['resources']['limits']['nvidia.com/gpu'] = 0

        return {
            "status": item['status']['conditions'][0]['type'],
            "name": metadata.name,
            "created_at": metadata.create_date,
            "image": notebook['image'],
            "gpus": notebook['resources']['limits']['nvidia.com/gpu'],
            "cpus": notebook['resources']['limits']['cpu'],
            "memory": notebook['resources']['limits']['memory'],
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


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = None):
    if shape_callable is None:
        return {"result": model}
    return shape_callable(model)
