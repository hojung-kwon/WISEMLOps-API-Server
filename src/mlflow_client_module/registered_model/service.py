from typing import Optional, Dict, Any, List

from mlflow import MlflowClient


class RegisteredModelService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_registered_model(self, name: str, tags: Optional[Dict[str, Any]] = None,
                                description: Optional[str] = None):
        result = self._mlflow_client.create_registered_model(name, tags=tags, description=description)
        return result

    def delete_registered_model(self, name: str):
        result = self._mlflow_client.delete_registered_model(name)
        return result

    def delete_registered_model_alias(self, name: str, alias: str):
        result = self._mlflow_client.delete_registered_model_alias(name, alias)
        return result

    def delete_registered_model_tag(self, name: str, key: str):
        result = self._mlflow_client.delete_registered_model_tag(name, key)
        return result

    def get_registered_model(self, name: str):
        result = self._mlflow_client.get_registered_model(name)
        return result

    def rename_registered_model(self, name: str, new_name: str):
        result = self._mlflow_client.rename_registered_model(name, new_name)
        return result

    def search_registered_models(self, filter_string: Optional[str] = None, max_results: int = 100,
                                 order_by: Optional[List[str]] = None,
                                 page_token: Optional[str] = None):
        result = self._mlflow_client.search_registered_models(filter_string=filter_string, max_results=max_results,
                                                              order_by=order_by, page_token=page_token)
        result_list = result.to_list()
        return result_list

    def set_registered_model_alias(self, name: str, alias: str, version: str):
        result = self._mlflow_client.set_registered_model_alias(name, alias, version)
        return result

    def set_registered_model_tag(self, name: str, key: str, value: Any):
        result = self._mlflow_client.set_registered_model_tag(name, key, value)
        return result

    def update_registered_model(self, name: str, description: Optional[str] = None):
        result = self._mlflow_client.update_registered_model(name, description=description)
        return result
