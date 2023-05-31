from typing import Optional, Dict, Any, List

from mlflow.exceptions import MlflowException

from src.mlflow_client import _mlflow_client
from src.mlflow_client.utils import response_success, response_error
from src.models import APIResponseModel


def create_run(experiment_id: str, start_time: Optional[int] = None, tags: Optional[Dict[str, Any]] = None,
               run_name: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.create_run(experiment_id, start_time=start_time, tags=tags, run_name=run_name)
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


def get_metric_history(run_id: str, key: str) -> APIResponseModel:
    try:
        result = _mlflow_client.get_metric_history(run_id, key)
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


def restore_run(run_id: str) -> APIResponseModel:
    try:
        result = _mlflow_client.restore_run(run_id)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)


def search_runs(experiment_ids: List[str], filter_string: str = '', run_view_type: int = 1, max_results: int = 1000,
                order_by: Optional[List[str]] = None, page_token: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.search_runs(experiment_ids, filter_string=filter_string, run_view_type=run_view_type,
                                            max_results=max_results, order_by=order_by, page_token=page_token)
        result_list = list(result)
    except MlflowException as me:
        return response_error(me)
    return response_success(result_list)


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


def update_run(run_id: str, status: Optional[str] = None, name: Optional[str] = None) -> APIResponseModel:
    try:
        result = _mlflow_client.update_run(run_id, status=status, name=name)
    except MlflowException as me:
        return response_error(me)
    return response_success(result)
