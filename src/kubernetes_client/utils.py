import json
import yaml
import base64
import requests
from src import app_config
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


def get_session_cookie():
    session = requests.Session()
    to_redirect = session.get(app_config.CLUSTER_HOST, verify=False)

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"login": app_config.KUBEFLOW_USERNAME, "password": app_config.KUBEFLOW_PASSWORD}
    session.post(to_redirect.url, headers=headers, data=data, verify=False)

    session_cookie = session.cookies.get_dict()["authservice_session"]
    return f"authservice_session={session_cookie}"