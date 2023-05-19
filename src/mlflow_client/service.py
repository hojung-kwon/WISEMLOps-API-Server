import os
from typing import Optional, Dict, Any, List

from mlflow import MlflowClient, MlflowException

from src.mlflow_client.config import MLFLOW_S3_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, \
    MLFLOW_TRACKING_URI
from src.mlflow_client.utils import response_error, response_success
from src.models import APIResponseModel

os.environ["MLFLOW_S3_ENDPOINT_URL"] = MLFLOW_S3_ENDPOINT_URL
os.environ["AWS_ACCESS_KEY_ID"] = AWS_ACCESS_KEY_ID
os.environ["AWS_SECRET_ACCESS_KEY"] = AWS_SECRET_ACCESS_KEY
os.environ["MLFLOW_TRACKING_URI"] = MLFLOW_TRACKING_URI

_mlflow_client = MlflowClient()


def create_experiment(name: str, artifact_location: Optional[str] = None,
                      tags: Optional[Dict[str, Any]] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_experiment(name, artifact_location=artifact_location, tags=tags)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def create_model_version(name: str, source: str, run_id: Optional[str] = None, tags: Optional[Dict[str, Any]] = None,
                         run_link: Optional[str] = None, description: Optional[str] = None,
                         await_creation_for: int = 300) -> APIResponseModel:
    try:
        result = _mlflow_client.create_model_version(name, source, run_id=run_id, tags=tags, run_link=run_link,
                                                     description=description, await_creation_for=await_creation_for)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def create_registered_model(name: str, tags: Optional[Dict[str, Any]] = None,
                            description: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_registered_model(name, tags=tags, description=description)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def create_run(experiment_id: str, start_time: Optional[int] = None, tags: Optional[Dict[str, Any]] = None,
               run_name: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_run(experiment_id, start_time=start_time, tags=tags, run_name=run_name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_experiment(experiment_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_experiment(experiment_id)
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


def delete_run(run_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_run(run_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_tag(run_id: str, key: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_tag(run_id, key)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_experiment(experiment_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_experiment(experiment_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_experiment_by_name(name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_experiment_by_name(name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_latest_versions(name: str, stages: Optional[List[str]] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.get_latest_versions(name, stages=stages)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_metric_history(run_id: str, key: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_metric_history(run_id, key)
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


def get_registered_model(name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_registered_model(name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def get_run(run_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_run(run_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def list_artifacts(run_id: str, path: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.list_artifacts(run_id, path=path)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def rename_experiment(experiment_id: str, new_name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.rename_experiment(experiment_id, new_name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def rename_registered_model(name: str, new_name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.rename_registered_model(name, new_name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def restore_experiment(experiment_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.restore_experiment(experiment_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def restore_run(run_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.restore_run(run_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_experiments(view_type: int = 1, max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                       order_by: Optional[List[str]] = None, page_token=None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_experiments(view_type=view_type, max_results=max_results,
                                                   filter_string=filter_string, order_by=order_by,
                                                   page_token=page_token)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_model_versions(filter_string: Optional[str] = None, max_results: int = 10000,
                          order_by: Optional[List[str]] = None, page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_model_versions(filter_string=filter_string, max_results=max_results,
                                                      order_by=order_by, page_token=page_token)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_registered_models(filter_string: Optional[str] = None, max_results: int = 100,
                             order_by: Optional[List[str]] = None,
                             page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_registered_models(filter_string=filter_string, max_results=max_results,
                                                         order_by=order_by, page_token=page_token)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_runs(experiment_ids: List[str], filter_string: str = '', run_view_type: int = 1, max_results: int = 1000,
                order_by: Optional[List[str]] = None, page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_runs(experiment_ids, filter_string=filter_string, run_view_type=run_view_type,
                                            max_results=max_results, order_by=order_by, page_token=page_token)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def set_experiment_tag(experiment_id: str, key: str, value: Any) -> APIResponseModel:
    try:
        result = _mlflow_client.set_experiment_tag(experiment_id, key, value)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def set_model_version_tag(name: str, version: Optional[str] = None, key: Optional[str] = None,
                          value: Optional[Any] = None, stage: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.set_model_version_tag(name, version=version, key=key, value=value, stage=stage)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


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


def set_tag(run_id: str, key: str, value: Any) -> APIResponseModel:
    try:
        result = _mlflow_client.set_tag(run_id, key, value)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def set_terminated(run_id: str, status: Optional[str] = None, end_time: Optional[int] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.set_terminated(run_id, status=status, end_time=end_time)
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


def update_registered_model(name: str, description: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.update_registered_model(name, description=description)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def update_run(run_id: str, status: Optional[str] = None, name: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.update_run(run_id, status=status, name=name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)
