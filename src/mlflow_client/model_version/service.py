from typing import Optional, Dict, Any, List

from mlflow import MlflowException

from src.mlflow_client import _mlflow_client
from src.mlflow_client.utils import response_success, response_error
from src.models import APIResponseModel


def create_model_version(name: str, source: str, run_id: Optional[str] = None, tags: Optional[Dict[str, Any]] = None,
                         run_link: Optional[str] = None, description: Optional[str] = None,
                         await_creation_for: int = 300) -> APIResponseModel:
    try:
        result = _mlflow_client.create_model_version(name, source, run_id=run_id, tags=tags, run_link=run_link,
                                                     description=description, await_creation_for=await_creation_for)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_model_version(name: str, version: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_model_version(name, version)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_model_version_tag(name: str, version: Optional[str] = None, key: Optional[str] = None,
                             stage: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_model_version_tag(name, version=version, key=key, stage=stage)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_latest_versions(name: str, stages: Optional[List[str]] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.get_latest_versions(name, stages=stages)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_model_version(name: str, version: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_model_version(name, version)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_model_version_by_alias(name: str, alias: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_model_version_by_alias(name, alias)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_model_version_download_uri(name: str, version: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_model_version_download_uri(name, version)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_model_version_stages(name: str, version: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_model_version_stages(name, version)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_model_versions(filter_string: Optional[str] = None, max_results: int = 10000,
                          order_by: Optional[List[str]] = None, page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_model_versions(filter_string=filter_string, max_results=max_results,
                                                      order_by=order_by, page_token=page_token)
        result_list = result.to_list()
    except MlflowException as me:
        return response_error(me)
    return response_success(result_list)


def set_model_version_tag(name: str, version: Optional[str] = None, key: Optional[str] = None,
                          value: Optional[Any] = None, stage: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.set_model_version_tag(name, version=version, key=key, value=value, stage=stage)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def transition_model_version_stage(name: str, version: str, stage: str,
                                   archive_existing_versions: bool = False) -> APIResponseModel:
    try:
        result = _mlflow_client.transition_model_version_stage(name, version, stage,
                                                               archive_existing_versions=archive_existing_versions)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def update_model_version(name: str, version: str, description: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.update_model_version(name, version, description=description)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)
