import json

from kubernetes import client
from src.cluster.models import Metadata
from src.models import APIResponseModel


class Render:

    @staticmethod
    def _to_status_list(model, to_each_shape: callable):
        result = []
        for item in model.items:
            result.append(to_each_shape(item))
        return {"result": result}

    @staticmethod
    def to_name_list(model):
        return {"result": [item.metadata.name for item in model.items]}

    @staticmethod
    def to_no_content(model):
        return {"result": ['no content']}

    @staticmethod
    def metadata_of(item):
        # key-value 형태로 반환
        return Metadata(
            name=item.metadata.name,
            create_date=item.metadata.creation_timestamp,
            annotations=item.metadata.annotations,
            labels=item.metadata.labels,
            api_version=item.api_version,
        )

    @staticmethod
    def to_node_status_list(model):
        return Render._to_status_list(model, Render.to_node_status)

    @staticmethod
    def to_node_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "version": item.status.node_info.kubelet_version,
            "status": item.status.conditions[-1].type,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_volume_status_list(model):
        return Render._to_status_list(model, Render.to_volume_status)

    @staticmethod
    def to_volume_status(item):
        metadata = Render.metadata_of(item)
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

    @staticmethod
    def to_volume_claim_status_list(model):
        return Render._to_status_list(model, Render.to_volume_claim_status)

    @staticmethod
    def to_volume_claim_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "status": item.status.phase,
            "volume": item.spec.volume_name,
            "capacity": item.status.capacity['storage'],
            "access_mode": item.spec.access_modes[0],
            "storage_class": item.spec.storage_class_name,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_configmap_status_list(model):
        return Render._to_status_list(model, Render.to_configmap_status)

    @staticmethod
    def to_configmap_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "data": item.data,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_secret_status_list(model):
        return Render._to_status_list(model, Render.to_secret_status)

    @staticmethod
    def to_secret_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "type": item.type,
            "data": item.data,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_pod_status_list(model):
        return Render._to_status_list(model, Render.to_pod_status)

    @staticmethod
    def to_pod_status(item):
        metadata = Render.metadata_of(item)
        ready = sum(1 for status in item.status.container_statuses if status.ready)
        total = len(item.status.container_statuses)
        return {
            "name": metadata.name,
            # ready인 pod 수/total
            "ready": f"{ready}/{total}",
            "status": item.status.phase,
            "restarts": item.status.container_statuses[0].restart_count,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_deployment_status_list(model):
        return Render._to_status_list(model, Render.to_deployment_status)

    @staticmethod
    def to_deployment_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "ready": f"{item.status.ready_replicas}/{item.status.replicas}",
            "up_to_date": item.status.updated_replicas,
            "available": item.status.available_replicas,
            "create_date": metadata.create_date,
        }

    @staticmethod
    def to_service_status_list(model):
        return Render._to_status_list(model, Render.to_service_status)

    @staticmethod
    def to_service_status(item):
        metadata = Render.metadata_of(item)
        return {
            "name": metadata.name,
            "type": item.spec.type,
            "cluster_ip": item.spec.cluster_ip,
            "external_ip": item.spec.external_i_ps,
            "ports": [f"{port.port}:{port.node_port}/{port.protocol}" for port in item.spec.ports],
            "create_date": metadata.create_date,
        }


def encode_to_base64(dict_data: dict):
    import base64
    return {key: base64.b64encode(value.encode('utf-8')).decode('utf-8') for key, value in dict_data.items()}


def error_with_message(e: client.ApiException):
    body = json.loads(e.body)
    return APIResponseModel(code=e.status, result=body['message'], message=e.reason)


def response(model, shape_callable: callable = Render.to_name_list):
    return shape_callable(model)