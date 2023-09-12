from typing import Optional, Dict, Any, List

from mlflow import MlflowClient


class RunService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_run(self, experiment_id: str, start_time: Optional[int] = None, tags: Optional[Dict[str, Any]] = None,
                   run_name: Optional[str] = None):
        result = self._mlflow_client.create_run(experiment_id, start_time=start_time, tags=tags, run_name=run_name)
        return result

    def delete_run(self, run_id: str):
        result = self._mlflow_client.delete_run(run_id)
        return result

    def delete_tag(self, run_id: str, key: str):
        result = self._mlflow_client.delete_tag(run_id, key)
        return result

    def get_metric_history(self, run_id: str, key: str):
        result = self._mlflow_client.get_metric_history(run_id, key)
        return result

    def get_run(self, run_id: str):
        result = self._mlflow_client.get_run(run_id)
        return result

    def list_artifacts(self, run_id: str, path: Optional[str] = None):
        result = self._mlflow_client.list_artifacts(run_id, path=path)
        return result

    def restore_run(self, run_id: str):
        result = self._mlflow_client.restore_run(run_id)
        return result

    def search_runs(self, experiment_ids: List[str], filter_string: str = '', run_view_type: int = 1,
                    max_results: int = 1000,
                    order_by: Optional[List[str]] = None, page_token: Optional[str] = None):
        result = self._mlflow_client.search_runs(experiment_ids, filter_string=filter_string,
                                                 run_view_type=run_view_type,
                                                 max_results=max_results, order_by=order_by, page_token=page_token)
        result_list = result.to_list()
        return result_list

    def set_tag(self, run_id: str, key: str, value: Any):
        result = self._mlflow_client.set_tag(run_id, key, value)
        return result

    def set_terminated(self, run_id: str, status: Optional[str] = None, end_time: Optional[int] = None):
        result = self._mlflow_client.set_terminated(run_id, status=status, end_time=end_time)
        return result

    def update_run(self, run_id: str, status: Optional[str] = None, name: Optional[str] = None):
        result = self._mlflow_client.update_run(run_id, status=status, name=name)
        return result
