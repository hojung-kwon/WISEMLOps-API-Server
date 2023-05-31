from kserve import ApiException
from mlflow.exceptions import MlflowException

import src.kserve_client.v1.utils as utils
from src.kserve_client import kserve_client
from src.kserve_client.utils import response
from src.models import APIResponseModel


def create_inference_service(name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                             service_account_name: str = 'minio30sa',
                             model_format: str = 'mlflow', protocol_version: str = 'v1') -> APIResponseModel:
    try:
        i_svc_info = utils.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                         model_name=model_name,
                                                         service_account_name=service_account_name,
                                                         model_format=model_format, protocol_version=protocol_version)
        if i_svc_info is None:
            response(False)
        i_svc = kserve_client.create(i_svc_info)
    except ApiException or MlflowException as e:
        return response(e)
    return response(i_svc)


def get_inference_service(model_name: str, namespace: str) -> APIResponseModel:
    try:
        i_svc = kserve_client.get(model_name, namespace=namespace)
    except ApiException or MlflowException as e:
        return response(e)
    return response(i_svc)


def patch_inference_service(name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                            service_account_name: str = 'minio30sa',
                            model_format: str = 'mlflow', protocol_version: str = 'v1') -> APIResponseModel:
    try:
        i_svc_info = utils.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                         model_name=model_name,
                                                         service_account_name=service_account_name,
                                                         model_format=model_format, protocol_version=protocol_version)
        if i_svc_info is None:
            response(False)
        i_svc = kserve_client.patch(i_svc_info)
    except ApiException or MlflowException as e:
        return response(e)
    return response(i_svc)


def replace_inference_service(name: str, namespace: str, storage_uri: str = None, model_name: str = None,
                              service_account_name: str = 'minio30sa',
                              model_format: str = 'mlflow', protocol_version: str = 'v1') -> APIResponseModel:
    try:
        i_svc_info = utils.create_inference_service_info(name, namespace, storage_uri=storage_uri,
                                                         model_name=model_name,
                                                         service_account_name=service_account_name,
                                                         model_format=model_format, protocol_version=protocol_version)
        if i_svc_info is None:
            response(False)
        i_svc = kserve_client.replace(i_svc_info)
    except ApiException or MlflowException as e:
        return response(e)
    return response(i_svc)


def delete_inference_service(model_name: str, namespace: str) -> APIResponseModel:
    try:
        kserve_client.delete(model_name, namespace=namespace)
    except ApiException or MlflowException as e:
        return response(e)
    return response(None)
