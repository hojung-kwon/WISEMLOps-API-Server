import json

from kubernetes import client
from src.models import APIResponseModel, Metadata


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
            create_date=item['metadata']['creationTimestamp'],
            annotations=item['metadata']['annotations'],
            labels=item['metadata']['labels'],
            api_version=item['apiVersion'],
        )

    @staticmethod
    def to_notebook_status_list(model):
        return Render._to_status_list(model, Render.to_notebook_status)

    @staticmethod
    def to_notebook_status(item: dict):
        metadata = Render.metadata_of(item)
        containers = item['spec']['template']['spec']['containers']
        containers_spec = []
        for container in containers:
            if 'nvidia.com/gpu' not in container['resources']['limits']:
                container['resources']['limits']['nvidia.com/gpu'] = 0
            containers_spec.append({
                "status": item['status']['conditions'][0]['type'],
                "name": metadata.name,
                "created_at": metadata.create_date,
                "image": container['image'],
                "gpus": container['resources']['limits']['nvidia.com/gpu'],
                "cpus": container['resources']['limits']['cpu'],
                "memory": container['resources']['limits']['memory'],
            })
        return containers_spec


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable):
    return shape_callable(model)