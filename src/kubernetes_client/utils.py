import base64
import json

import yaml
from kubernetes.client.rest import ApiException

from src.models import APIResponseModel


def error_with_message(e: ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable):
    return shape_callable(model)


def encode_to_base64(dict_data: dict):
    return {key: base64.b64encode(value.encode('utf-8')).decode('utf-8') for key, value in dict_data.items()}


def to_yaml(item: dict):
    return yaml.dump(item).split('\n')
