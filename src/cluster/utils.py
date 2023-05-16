import json

from src.cluster.exceptions import ClusterException
from src.models import APIResponseModel


def success_with_name_list(model):
    return {"result": [item.metadata.name for item in model.items]}


def success_with_no_content(items):
    return {"result": ['no content']}


def error_with_message(exception: ClusterException):
    body = json.loads(exception.body)
    return APIResponseModel(code=body['code'], result=body['status'], message=body['reason'])


def response(model, shape_callable: callable = success_with_name_list):
    return shape_callable(model)