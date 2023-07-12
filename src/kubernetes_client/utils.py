import json
import yaml
import base64
import time
from src.models import APIResponseModel
from kubernetes.client.rest import ApiException


def error_with_message(e: ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable):
    return shape_callable(model)


def encode_to_base64(dict_data: dict):
    return {key: base64.b64encode(value.encode('utf-8')).decode('utf-8') for key, value in dict_data.items()}


def to_yaml(item: dict):
    return yaml.dump(item).split('\n')


def is_token_expired(token: str):
    if token is None:
        return True
    payload = token.split(".")[1]
    payload = payload + '=' * (4 - len(payload) % 4)
    payload = base64.b64decode(payload).decode()
    payload = json.loads(payload)
    exp = payload['exp']
    now = time.time()
    if exp < now:
        return True
    return False
