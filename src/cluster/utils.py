import json

from kubernetes import client
from src.models import APIResponseModel


def success_with_name_list(model):
    return {"result": [item.metadata.name for item in model.items]}


def success_with_no_content(model):
    return {"result": ['no content']}


def _success_with_status(model, to_shape: callable):
    result = []
    for item in model.items:
        result.append(to_shape(item))
    return {"result": result}


def success_with_node_status(model):
    return _success_with_status(model, to_node_status)


def to_node_status(item):
    name, create_date, _, _ = metadata_of(item)
    return {
        "name": name,
        "create_date": create_date,
        "version": item.status.node_info.kubelet_version,
        "status": item.status.conditions[-1].type
    }


def success_with_volume_status(model):
    return _success_with_status(model, to_volume_status)


def to_volume_status(item):
    name, create_date, _, _ = metadata_of(item)
    return {
        "name": name,
        "capacity": item.spec.capacity['storage'],
        "access_mode": item.spec.access_modes[0],
        "reclaim_policy": item.spec.persistent_volume_reclaim_policy,
        "status": item.status.phase,
        "claim": item.spec.claim_ref.name if item.spec.claim_ref else 'none',
        "storage_class": item.spec.storage_class_name,
        "reason": item.status.reason,
    }


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