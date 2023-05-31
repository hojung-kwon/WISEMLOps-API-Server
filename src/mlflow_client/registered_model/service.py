from typing import Optional, Dict, Any, List

from mlflow.exceptions import MlflowException

from src.mlflow_client import _mlflow_client
from src.mlflow_client.utils import response_success, response_error
from src.models import APIResponseModel


def create_registered_model(name: str, tags: Optional[Dict[str, Any]] = None,
                            description: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_registered_model(name, tags=tags, description=description)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_registered_model(name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_registered_model(name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_registered_model_alias(name: str, alias: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_registered_model_alias(name, alias)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_registered_model_tag(name: str, key: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_registered_model_tag(name, key)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_registered_model(name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_registered_model(name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def rename_registered_model(name: str, new_name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.rename_registered_model(name, new_name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_registered_models(filter_string: Optional[str] = None, max_results: int = 100,
                             order_by: Optional[List[str]] = None,
                             page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_registered_models(filter_string=filter_string, max_results=max_results,
                                                         order_by=order_by, page_token=page_token)
        result_list = list(result)
    except MlflowException as me:
        return response_error(me)
    return response_success(result_list)


def set_registered_model_alias(name: str, alias: str, version: str) -> APIResponseModel:
    try:
        result = _mlflow_client.set_registered_model_alias(name, alias, version)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def set_registered_model_tag(name: str, key: str, value: Any) -> APIResponseModel:
    try:
        result = _mlflow_client.set_registered_model_tag(name, key, value)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def update_registered_model(name: str, description: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.update_registered_model(name, description=description)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)
