from typing import Optional, Dict, Any, List

from mlflow import MlflowClient

from src.mlflow_client_module.exceptions import MlflowException, MlflowApiError


class RunService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_run(self, experiment_id: str, start_time: Optional[int] = None, tags: Optional[Dict[str, Any]] = None,
                   run_name: Optional[str] = None):
        try:
            result = self._mlflow_client.create_run(experiment_id, start_time=start_time, tags=tags, run_name=run_name)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_run(self, run_id: str):
        try:
            self._mlflow_client.delete_run(run_id)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_tag(self, run_id: str, key: str):
        try:
            self._mlflow_client.delete_tag(run_id, key)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def get_metric_history(self, run_id: str, key: str):
        try:
            result = self._mlflow_client.get_metric_history(run_id, key)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def get_run(self, run_id: str):
        try:
            result = self._mlflow_client.get_run(run_id)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def list_artifacts(self, run_id: str, path: Optional[str] = None):
        try:
            result = self._mlflow_client.list_artifacts(run_id, path=path)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def restore_run(self, run_id: str):
        try:
            self._mlflow_client.restore_run(run_id)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def search_runs(self, experiment_ids: List[str], filter_string: str = '', run_view_type: int = 1,
                    max_results: int = 1000,
                    order_by: Optional[List[str]] = None, page_token: Optional[str] = None):
        try:
            result = self._mlflow_client.search_runs(experiment_ids, filter_string=filter_string,
                                                     run_view_type=run_view_type,
                                                     max_results=max_results, order_by=order_by, page_token=page_token)
            result_list = result.to_list()
            return result_list
        except MlflowException as e:
            raise MlflowApiError(e)

    def set_tag(self, run_id: str, key: str, value: Any):
        try:
            self._mlflow_client.set_tag(run_id, key, value)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def set_terminated(self, run_id: str, status: Optional[str] = None, end_time: Optional[int] = None):
        try:
            self._mlflow_client.set_terminated(run_id, status=status, end_time=end_time)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def update_run(self, run_id: str, status: Optional[str] = None, name: Optional[str] = None):
        try:
            self._mlflow_client.update_run(run_id, status=status, name=name)
            return run_id
        except MlflowException as e:
            raise MlflowApiError(e)
