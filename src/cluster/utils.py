import json

from kubernetes import client

from src.cluster.models import Metadata
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
    metadata = metadata_of(item)
    return {
        "name": metadata.name,
        "version": item.status.node_info.kubelet_version,
        "status": item.status.conditions[-1].type,
        "create_date": metadata.create_date,
    }


def success_with_volume_status(model):
    return _success_with_status(model, to_volume_status)


def to_volume_status(item):
    metadata = metadata_of(item)
    return {
        "name": metadata.name,
        "capacity": item.spec.capacity['storage'],
        "access_mode": item.spec.access_modes[0],
        "reclaim_policy": item.spec.persistent_volume_reclaim_policy,
        "status": item.status.phase,
        "claim": item.spec.claim_ref.name if item.spec.claim_ref else 'none',
        "storage_class": item.spec.storage_class_name,
        "reason": item.status.reason,
        "create_date": metadata.create_date,
    }


def success_with_volume_claim_status(model):
    return _success_with_status(model, to_volume_claim_status)


def to_volume_claim_status(item):
    metadata = metadata_of(item)
    return {
        "name": metadata.name,
        "status": item.status.phase,
        "volume": item.spec.volume_name,
        "capacity": item.status.capacity['storage'],
        "access_mode": item.spec.access_modes[0],
        "storage_class": item.spec.storage_class_name,
        "create_date": metadata.create_date,
    }

def success_with_config_map_status(model):
    return _success_with_status(model, to_config_map_status)


def to_config_map_status(item):
    metadata = metadata_of(item)
    return {
        "name": metadata.name,
        "data": item.data,
        "create_date": metadata.create_date,
    }


def metadata_of(item):
    # key-value 형태로 반환
    return Metadata(
        name=item.metadata.name,
        create_date=item.metadata.creation_timestamp,
        annotations=item.metadata.annotations,
        labels=item.metadata.labels,
        api_version=item.api_version,
    )


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = success_with_name_list):
    return shape_callable(model)