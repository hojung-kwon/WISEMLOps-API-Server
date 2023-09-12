from typing import Optional, Dict, Any, List

from mlflow import MlflowClient

from src.mlflow_client_module.exceptions import MlflowException, MlflowApiError


class RegisteredModelService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_registered_model(self, name: str, tags: Optional[Dict[str, Any]] = None,
                                description: Optional[str] = None):
        try:
            result = self._mlflow_client.create_registered_model(name, tags=tags, description=description)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_registered_model(self, name: str):
        try:
            result = self._mlflow_client.delete_registered_model(name)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_registered_model_alias(self, name: str, alias: str):
        try:
            self._mlflow_client.delete_registered_model_alias(name, alias)
            return name
        except MlflowException as e:
            raise MlflowApiError(e)

    def delete_registered_model_tag(self, name: str, key: str):
        try:
            self._mlflow_client.delete_registered_model_tag(name, key)
            return name
        except MlflowException as e:
            raise MlflowApiError(e)

    def get_registered_model(self, name: str):
        try:
            result = self._mlflow_client.get_registered_model(name)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def rename_registered_model(self, name: str, new_name: str):
        try:
            result = self._mlflow_client.rename_registered_model(name, new_name)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)

    def search_registered_models(self, filter_string: Optional[str] = None, max_results: int = 100,
                                 order_by: Optional[List[str]] = None,
                                 page_token: Optional[str] = None):
        try:
            result = self._mlflow_client.search_registered_models(filter_string=filter_string, max_results=max_results,
                                                                  order_by=order_by, page_token=page_token)
            result_list = result.to_list()
            return result_list
        except MlflowException as e:
            raise MlflowApiError(e)

    def set_registered_model_alias(self, name: str, alias: str, version: str):
        try:
            self._mlflow_client.set_registered_model_alias(name, alias, version)
            return name
        except MlflowException as e:
            raise MlflowApiError(e)

    def set_registered_model_tag(self, name: str, key: str, value: Any):
        try:
            self._mlflow_client.set_registered_model_tag(name, key, value)
            return name
        except MlflowException as e:
            raise MlflowApiError(e)

    def update_registered_model(self, name: str, description: Optional[str] = None):
        try:
            result = self._mlflow_client.update_registered_model(name, description=description)
            return result
        except MlflowException as e:
            raise MlflowApiError(e)
