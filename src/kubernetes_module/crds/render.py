from src.kubernetes_module.schemas import Metadata
from src.kubernetes_module.utils import to_yaml, get_status_uri, get_overview_uri, get_logs_uri, get_connect_uri, \
    get_delete_uri


class Render:
    @staticmethod
    def _to_status_list(model, to_each_shape: callable):
        result = []
        for item in model['items']:
            result.append(to_each_shape(item))
        return result

    @staticmethod
    def to_no_content(model):
        return None

    @staticmethod
    def metadata_of(item: dict):
        # key-value 형태로 반환
        return Metadata(
            name=item['metadata']['name'],
            labels=item['metadata']['labels'],
            annotations=item['metadata']['annotations'],
            create_date=item['metadata']['creationTimestamp'],
        )

    @staticmethod
    def to_notebook_status_list(model):
        return Render._to_status_list(model, Render.to_notebook_status)

    @staticmethod
    def to_notebook_status(item: dict):
        metadata = Render.metadata_of(item)
        namespace = item['metadata']['namespace']
        containers = item['spec']['template']['spec']['containers']
        notebook = containers[0]

        if 'nvidia.com/gpu' not in notebook['resources']['limits']:
            notebook['resources']['limits']['nvidia.com/gpu'] = 0

        return {
            "status": item['status']['containerState'] if 'status' in item else {},
            "name": metadata.name,
            "created_at": metadata.create_date,
            "image": notebook['image'],
            "gpus": notebook['resources']['limits']['nvidia.com/gpu'],
            "cpus": notebook['resources']['limits']['cpu'],
            "memory": notebook['resources']['limits']['memory'],
            "connect": get_connect_uri(namespace, metadata.name),
            "delete": get_delete_uri(namespace, metadata.name),
        }

    @staticmethod
    def to_notebook_details(model):
        label_selector = f"notebook-name={model['metadata']['name']}"
        namespace = model['metadata']['namespace']
        name = model['metadata']['name']
        return {
            "status": get_status_uri(namespace, label_selector),
            "overview": get_overview_uri(namespace, name),
            "logs": get_logs_uri(namespace, label_selector),
            "connect": get_connect_uri(namespace, name),
            "delete": get_delete_uri(namespace, name),
            "yaml": to_yaml(model),
        }

    @staticmethod
    def to_notebook_overview(item: dict):
        metadata = Render.metadata_of(item)
        _spec = item['spec']['template']['spec']
        _notebook = _spec['containers'][0]
        volumes = _spec['volumes']
        image = _notebook['image']
        conditions = item['status']['conditions']
        return {
            "name": metadata.name,
            "labels": metadata.labels,
            "annotations": metadata.annotations,
            "image": image,
            "min_cpu": _notebook['resources']['requests']['cpu'],
            "max_cpu": _notebook['resources']['limits']['cpu'],
            "min_memory": _notebook['resources']['requests']['memory'],
            "max_memory": _notebook['resources']['limits']['memory'],
            "min_gpu": _notebook['resources']['requests']['nvidia.com/gpu'],
            "max_gpu": _notebook['resources']['limits']['nvidia.com/gpu'],
            "create_date": metadata.create_date,
            "volumes": volumes,
            "conditions": conditions,
        }
