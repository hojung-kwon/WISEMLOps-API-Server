import json

from kubernetes import client
from src.models import APIResponseModel, Metadata


class Render:

    @staticmethod
    def _to_status_list(model, to_each_shape: callable):
        result = []
        for item in model['items']:
            result.append(to_each_shape(item))
        return {"result": result}

    @staticmethod
    def to_name_list(model):
        return {"result": [item['metadata']['name'] for item in model['items']]}

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
        return {
            "name": metadata.name,
            "create_date": metadata.create_date,
        }


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable):
    return shape_callable(model)