from typing import Optional, Dict, Any, List

from mlflow import MlflowClient

from src.mlflow_module.exceptions import MlflowApiError, MlflowException


class ExperimentService:
    def __init__(self):
        pass

    @staticmethod
    def get_mlflow_client():
        return MlflowClient()

    def create_experiment(self, name: str, artifact_location: Optional[str] = None,
                          tags: Optional[Dict[str, Any]] = None):
        try:
            result = self.get_mlflow_client().create_experiment(name, artifact_location=artifact_location, tags=tags)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_experiment(self, experiment_id: str):
        try:
            self.get_mlflow_client().delete_experiment(experiment_id)
            return experiment_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def get_experiment(self, experiment_id: str):
        try:
            result = self.get_mlflow_client().get_experiment(experiment_id)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def get_experiment_by_name(self, name: str):
        try:
            result = self.get_mlflow_client().get_experiment_by_name(name)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def rename_experiment(self, experiment_id: str, new_name: str):
        try:
            self.get_mlflow_client().rename_experiment(experiment_id, new_name)
            return experiment_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def restore_experiment(self, experiment_id: str):
        try:
            self.get_mlflow_client().restore_experiment(experiment_id)
            return experiment_id
        except MlflowException as e:
            raise MlflowApiError(e)

    def search_experiments(self, view_type: int = 1, max_results: Optional[int] = 1000,
                           filter_string: Optional[str] = None,
                           order_by: Optional[List[str]] = None, page_token: Optional[str] = None):
        try:
            result = self.get_mlflow_client().search_experiments(view_type=view_type, max_results=max_results,
                                                                 filter_string=filter_string, order_by=order_by,
                                                                 page_token=page_token)
            result_list = result.to_list()
            return result_list
        except MlflowException as e:
            raise MlflowApiError(e)

    def set_experiment_tag(self, experiment_id: str, key: str, value: Any):
        try:
            self.get_mlflow_client().set_experiment_tag(experiment_id, key, value)
            return experiment_id
        except MlflowException as e:
            raise MlflowApiError(e)
