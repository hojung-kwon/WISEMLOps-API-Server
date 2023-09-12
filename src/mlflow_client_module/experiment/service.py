from typing import Optional, Dict, Any, List

from mlflow import MlflowClient


class ExperimentService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_experiment(self, name: str, artifact_location: Optional[str] = None,
                          tags: Optional[Dict[str, Any]] = None):
        result = self._mlflow_client.create_experiment(name, artifact_location=artifact_location, tags=tags)
        return result

    def delete_experiment(self, experiment_id: str):
        result = self._mlflow_client.delete_experiment(experiment_id)
        return result

    def get_experiment(self, experiment_id: str):
        result = self._mlflow_client.get_experiment(experiment_id)
        return result

    def get_experiment_by_name(self, name: str):
        result = self._mlflow_client.get_experiment_by_name(name)
        return result

    def rename_experiment(self, experiment_id: str, new_name: str):
        result = self._mlflow_client.rename_experiment(experiment_id, new_name)
        return result

    def restore_experiment(self, experiment_id: str):
        result = self._mlflow_client.restore_experiment(experiment_id)
        return result

    def search_experiments(self, view_type: int = 1, max_results: Optional[int] = 1000,
                           filter_string: Optional[str] = None,
                           order_by: Optional[List[str]] = None, page_token: Optional[str] = None):
        result = self._mlflow_client.search_experiments(view_type=view_type, max_results=max_results,
                                                        filter_string=filter_string, order_by=order_by,
                                                        page_token=page_token)
        result_list = result.to_list()
        return result_list

    def set_experiment_tag(self, experiment_id: str, key: str, value: Any):
        result = self._mlflow_client.set_experiment_tag(experiment_id, key, value)
        return result
