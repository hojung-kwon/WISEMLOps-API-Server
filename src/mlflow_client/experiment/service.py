from typing import Optional, Dict, Any

from mlflow.exceptions import MlflowException

from src.mlflow_client import _mlflow_client
from src.mlflow_client.utils import response_success, response_error
from src.models import APIResponseModel


def create_experiment(name: str, artifact_location: Optional[str] = None,
                      tags: Optional[Dict[str, Any]] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_experiment(name, artifact_location=artifact_location, tags=tags)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def delete_experiment(experiment_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.delete_experiment(experiment_id)
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


def rename_experiment(experiment_id: str, new_name: str) -> APIResponseModel:
    try:
        result = _mlflow_client.rename_experiment(experiment_id, new_name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def restore_experiment(experiment_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.restore_experiment(experiment_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def list_experiments(view_type: int = 1, max_results: Optional[int] = 1000,
                     page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.list_experiments(view_type=view_type, max_results=max_results,
                                                 page_token=page_token)
        result_list = list(result)
    except MlflowException as me:
        return response_error(me)
    return response_success(result_list)


def set_experiment_tag(experiment_id: str, key: str, value: Any) -> APIResponseModel:
    try:
        result = _mlflow_client.set_experiment_tag(experiment_id, key, value)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)
