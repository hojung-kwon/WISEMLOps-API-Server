from typing import List, Optional

from kserve import V1beta1InferenceServiceSpec, V1beta1PredictorSpec, V1beta1ModelSpec, V1beta1ModelFormat, \
    V1beta1InferenceService, constants
from kubernetes import client
from mlflow import MlflowException

from src.mlflow_client_module import _mlflow_client


def create_inference_service_info(name: str, namespace: str, storage_uri: Optional[str] = None,
                                  model_name: Optional[str] = None, service_account_name: str = 'minio30sa',
                                  model_format: str = 'mlflow',
                                  protocol_version: str = 'v1') -> Optional[V1beta1InferenceService]:
    if model_format == 'mlflow':
        protocol_version = 'v2'
        if storage_uri is None:
            if model_name is None:
                return None
            try:
                storage_uri = get_latest_model_version_storage_uri(model_name)
            except MlflowException as e:
                raise MlflowException(message=e.message, error_code=e.error_code)

    if storage_uri in None:
        return None

    default_model_spec = V1beta1InferenceServiceSpec(
        predictor=V1beta1PredictorSpec(
            service_account_name=service_account_name,
            model=V1beta1ModelSpec(
                model_format=V1beta1ModelFormat(name=model_format),
                protocol_version=protocol_version,
                storage_uri=storage_uri)
        )
    )

    i_svc = V1beta1InferenceService(api_version=constants.KSERVE_V1BETA1,
                                    kind=constants.KSERVE_KIND,
                                    metadata=client.V1ObjectMeta(name=name, namespace=namespace),
                                    spec=default_model_spec)

    return i_svc


def get_latest_versions(model_name: str, stage: str = None) -> List:
    try:
        stages = None
        if stage:
            stages = stage.split(",")
        latest_model_versions = _mlflow_client.get_latest_versions(model_name, stages=stages)
    except MlflowException as e:
        raise MlflowException(message=e.message, error_code=e.error_code)
    return latest_model_versions


def get_latest_model_version_storage_uri(model_name: str, stage: str = None) -> Optional[str]:
    try:
        latest_model_versions = get_latest_versions(model_name, stage=stage)
    except MlflowException as e:
        raise MlflowException(message=e.message, error_code=e.error_code)
    if len(latest_model_versions) < 1:
        return None
    return latest_model_versions[-1].source
