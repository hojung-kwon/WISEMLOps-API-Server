from typing import List, Optional

from kserve import ApiException
from kserve import V1beta1InferenceServiceSpec, V1beta1PredictorSpec, V1beta1ModelSpec, V1beta1ModelFormat, \
    V1beta1InferenceService, constants, KServeClient
from kubernetes import client
from mlflow import MlflowException, MlflowClient

from src.kserve_module.exceptions import KServeApiError


class KServeService:
    def __init__(self, config_file):
        self.config_file = config_file

    @staticmethod
    def get_mlflow_client():
        return MlflowClient()

    def get_kserve_client(self):
        return KServeClient(config_file=self.config_file)

    def get_latest_versions_from_mlflow(self, model_name: str, stage: str = None) -> List:
        try:
            stages = None
            if stage:
                stages = stage.split(",")
            return self.get_mlflow_client().get_latest_versions(model_name, stages=stages)
        except MlflowException as e:
            raise KServeApiError(e)

    def get_latest_model_version_storage_uri(self, model_name: str, stage: str = None) -> Optional[str]:
        try:
            latest_model_versions = self.get_latest_versions_from_mlflow(model_name, stage=stage)
            if len(latest_model_versions) < 1:
                return None
            return latest_model_versions[-1].source
        except MlflowException as e:
            raise KServeApiError(e)

    def create_inference_service_info(self, name: str, namespace: str, storage_uri: Optional[str] = None,
                                      model_name: Optional[str] = None, service_account_name: str = 'minio30sa',
                                      model_format: str = 'mlflow',
                                      protocol_version: str = 'v1') -> Optional[V1beta1InferenceService]:
        try:
            if model_format != 'mlflow':
                return None
            protocol_version = 'v2'
            if storage_uri is None:
                if model_name is None:
                    return None
                storage_uri = self.get_latest_model_version_storage_uri(model_name)

            if storage_uri is None:
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
        except MlflowException as e:
            raise KServeApiError(e)

    def create_inference_service(self, name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                                 service_account_name: str = 'minio30sa',
                                 model_format: str = 'mlflow', protocol_version: str = 'v1'):
        try:
            i_svc_info = self.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                            model_name=model_name,
                                                            service_account_name=service_account_name,
                                                            model_format=model_format,
                                                            protocol_version=protocol_version)
            if i_svc_info is None:
                return False
            i_svc = self.get_kserve_client().create(i_svc_info)
            return i_svc
        except ApiException or MlflowException as e:
            raise KServeApiError(e)

    def get_inference_service(self, model_name: str, namespace: str):
        try:
            i_svc = self.get_kserve_client().get(model_name, namespace=namespace)
            return i_svc
        except ApiException or MlflowException as e:
            raise KServeApiError(e)

    def patch_inference_service(self, name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                                service_account_name: str = 'minio30sa',
                                model_format: str = 'mlflow', protocol_version: str = 'v1'):
        try:
            i_svc_info = self.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                            model_name=model_name,
                                                            service_account_name=service_account_name,
                                                            model_format=model_format,
                                                            protocol_version=protocol_version)
            if i_svc_info is None:
                return False
            i_svc = self.get_kserve_client().patch(name, i_svc_info)
            return i_svc
        except ApiException or MlflowException as e:
            raise KServeApiError(e)

    def replace_inference_service(self, name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                                  service_account_name: str = 'minio30sa',
                                  model_format: str = 'mlflow', protocol_version: str = 'v1'):
        try:
            i_svc_info = self.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                            model_name=model_name,
                                                            service_account_name=service_account_name,
                                                            model_format=model_format,
                                                            protocol_version=protocol_version)
            if i_svc_info is None:
                return False
            i_svc = self.get_kserve_client().replace(name, i_svc_info)
            return i_svc
        except ApiException or MlflowException as e:
            raise KServeApiError(e)

    def delete_inference_service(self, model_name: str, namespace: str):
        try:
            self.get_kserve_client().delete(model_name, namespace=namespace)
            return None
        except ApiException or MlflowException as e:
            raise KServeApiError(e)
