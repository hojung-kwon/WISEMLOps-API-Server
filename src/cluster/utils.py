import json
from kubernetes import client
from src.models import APIResponseModel


def success_with_name_list(model):
    return {"result": [item.metadata.name for item in model.items]}


def success_with_no_content(model):
    return {"result": ['no content']}


def success_with_node_status(model):
    result = []
    for item in model.items:
        name, age, _, _ = metadata_of(item)
        version = item.status.node_info.kubelet_version
        status = item.status.conditions[-1].type
        result.append({"name": name, "create_date": age, "version": version, "status": status})
    return {"result": result}


def metadata_of(item):
    # key-value 형태로 반환
    return {
        "name": item.metadata.name,
        "create_date": item.metadata.creation_timestamp,
        "api_version": item.api_version,
        "labels": item.metadata.labels
    }


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = success_with_name_list):
    return shape_callable(model)