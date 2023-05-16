import json
from kubernetes import client
from src.models import APIResponseModel


def success_with_name_list(model):
    return {"result": [item.metadata.name for item in model.items]}


def success_with_no_content(items):
    return {"result": ['no content']}


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = success_with_name_list):
    return shape_callable(model)