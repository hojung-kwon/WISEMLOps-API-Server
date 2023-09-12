from typing import Optional, Dict, Any, List

from mlflow import MlflowClient


class ModelVersionService:
    def __init__(self, _mlflow_client=MlflowClient()):
        self._mlflow_client = MlflowClient()

    def create_model_version(self, name: str, source: str, run_id: Optional[str] = None,
                             tags: Optional[Dict[str, Any]] = None,
                             run_link: Optional[str] = None, description: Optional[str] = None,
                             await_creation_for: int = 300):
        result = self._mlflow_client.create_model_version(name, source, run_id=run_id, tags=tags, run_link=run_link,
                                                          description=description,
                                                          await_creation_for=await_creation_for)
        return result

    def delete_model_version(self, name: str, version: str):
        result = self._mlflow_client.delete_model_version(name, version)
        return result

    def delete_model_version_tag(self, name: str, version: Optional[str] = None, key: Optional[str] = None,
                                 stage: Optional[str] = None):
        result = self._mlflow_client.delete_model_version_tag(name, version=version, key=key, stage=stage)
        return result

    def get_latest_versions(self, name: str, stages: Optional[List[str]] = None):
        result = self._mlflow_client.get_latest_versions(name, stages=stages)
        return result

    def get_model_version(self, name: str, version: str):
        result = self._mlflow_client.get_model_version(name, version)
        return result

    def get_model_version_by_alias(self, name: str, alias: str):
        result = self._mlflow_client.get_model_version_by_alias(name, alias)
        return result

    def get_model_version_download_uri(self, name: str, version: str):
        result = self._mlflow_client.get_model_version_download_uri(name, version)
        return result

    def get_model_version_stages(self, name: str, version: str):
        result = self._mlflow_client.get_model_version_stages(name, version)
        return result

    def search_model_versions(self, filter_string: Optional[str] = None, max_results: int = 10000,
                              order_by: Optional[List[str]] = None,
                              page_token: Optional[str] = None):
        result = self._mlflow_client.search_model_versions(filter_string=filter_string, max_results=max_results,
                                                           order_by=order_by, page_token=page_token)
        result_list = result.to_list()
        return result_list

    def set_model_version_tag(self, name: str, version: Optional[str] = None, key: Optional[str] = None,
                              value: Optional[Any] = None, stage: Optional[str] = None):
        result = self._mlflow_client.set_model_version_tag(name, version=version, key=key, value=value, stage=stage)
        return result

    def transition_model_version_stage(self, name: str, version: str, stage: str,
                                       archive_existing_versions: bool = False):
        result = self._mlflow_client.transition_model_version_stage(name, version, stage,
                                                                    archive_existing_versions=archive_existing_versions)
        return result

    def update_model_version(self, name: str, version: str, description: Optional[str] = None):
        result = self._mlflow_client.update_model_version(name, version, description=description)
        return result
