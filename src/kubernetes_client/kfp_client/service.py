from typing import Optional

import kfp_server_api
from kfp import Client
from kubernetes.client import CoreV1Api, AuthenticationV1TokenRequest, V1ObjectMeta, V1TokenRequestSpec
from kubernetes.client.rest import ApiException

from src import app_config
from src.kubernetes_client.kfp_client.utils import Render
from src.kubernetes_client.models import Experiment, Pipeline, PipelineVersion, Run, RecurringRun
from src.kubernetes_client.utils import response, is_token_expired, error_with_message


class KfpService:
    def __init__(self, cluster_client: CoreV1Api):
        self.cluster_client = cluster_client
        self.sa_name = "default-editor"
        self.namespace = "kubeflow-user-example-com"
        self.token = None
        self.kfp_client = None
        self._connect_kfp_client()

    def _connect_kfp_client(self):
        if self.kfp_client is None or is_token_expired(self.token):
            self.token = \
                self.cluster_client.create_namespaced_service_account_token(name=self.sa_name,
                                                                            namespace=self.namespace,
                                                                            body=AuthenticationV1TokenRequest(
                                                                                api_version="authentication.k8s.io/v1",
                                                                                kind="TokenRequest",
                                                                                metadata=V1ObjectMeta(
                                                                                    name=self.sa_name,
                                                                                    namespace=self.namespace),
                                                                                spec=V1TokenRequestSpec(
                                                                                    audiences=[
                                                                                        "pipelines.kubeflow.org"],
                                                                                    expiration_seconds=7200))
                                                                            ).status.token
            self.kfp_client = Client(host=app_config.KUBEFLOW_PIPELINES_ENDPOINT,
                                     namespace=self.namespace,
                                     existing_token=self.token)

    def get_kfp_healthz(self):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_kfp_healthz()
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_user_namespace(self):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_user_namespace()
            return response(result, Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def list_experiments(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.list_experiments(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                      namespace=self.namespace)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def create_experiment(self, experiment: Experiment):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.create_experiment(name=experiment.name, description=experiment.description,
                                                       namespace=self.namespace)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_experiment(self, experiment_id: Optional[str] = None, experiment_name: Optional[str] = None):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_experiment(experiment_id=experiment_id, experiment_name=experiment_name,
                                                    namespace=self.namespace)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def archive_experiment(self, experiment_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.archive_experiment(experiment_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def delete_experiment(self, experiment_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.delete_experiment(experiment_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def list_pipelines(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.list_pipelines(page_token=page_token, page_size=page_size, sort_by=sort_by)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def upload_pipeline(self, pipeline: Pipeline):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.upload_pipeline(pipeline_package_path=pipeline.pipeline_package_path,
                                                     pipeline_name=pipeline.pipeline_name,
                                                     description=pipeline.description)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_pipeline(self, pipeline_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_pipeline(pipeline_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def delete_pipeline(self, pipeline_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.delete_pipeline(pipeline_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def list_pipeline_versions(self, pipeline_id: str, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.list_pipeline_versions(pipeline_id=pipeline_id, page_token=page_token,
                                                            page_size=page_size, sort_by=sort_by)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def upload_pipeline_version(self, pipeline_version: PipelineVersion):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.upload_pipeline_version(
                pipeline_package_path=pipeline_version.pipeline_package_path,
                pipeline_version_name=pipeline_version.pipeline_version_name,
                pipeline_id=pipeline_version.pipeline_id,
                pipeline_name=pipeline_version.pipeline_name,
                description=pipeline_version.description)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_pipeline_id(self, name: Optional[str]):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_pipeline_id(name)
            return response(result, Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def list_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                  experiment_id: Optional[str] = None):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.list_runs(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                               experiment_id=experiment_id,
                                               namespace=self.namespace)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def create_run_from_pipeline_package(self, run: Run):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.create_run_from_pipeline_package(pipeline_file=run.pipeline_file,
                                                                      arguments=run.arguments,
                                                                      run_name=run.run_name,
                                                                      experiment_name=run.experiment_name,
                                                                      namespace=self.namespace,
                                                                      pipeline_root=run.pipeline_root,
                                                                      enable_caching=run.enable_caching,
                                                                      service_account=self.sa_name)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_run(self, run_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_run(run_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def wait_for_run_completion(self, run_id: str, timeout: int):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.wait_for_run_completion(run_id, timeout=timeout)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def list_recurring_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                            experiment_id: Optional[str] = None):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.list_recurring_runs(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                         experiment_id=experiment_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def create_recurring_run(self, recurring_run: RecurringRun, ):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.create_recurring_run(experiment_id=recurring_run.experiment_id,
                                                          job_name=recurring_run.job_name,
                                                          description=recurring_run.description,
                                                          start_time=recurring_run.start_time,
                                                          end_time=recurring_run.end_time,
                                                          interval_second=recurring_run.interval_second,
                                                          cron_expression=recurring_run.cron_expression,
                                                          max_concurrency=recurring_run.max_concurrency,
                                                          no_catchup=recurring_run.no_catchup,
                                                          params=recurring_run.params,
                                                          pipeline_package_path=recurring_run.pipeline_package_path,
                                                          pipeline_id=recurring_run.pipeline_id,
                                                          version_id=recurring_run.version_id,
                                                          enabled=recurring_run.enabled,
                                                          enable_caching=recurring_run.enable_caching,
                                                          service_account=self.sa_name)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def get_recurring_run(self, job_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.get_recurring_run(job_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def delete_job(self, job_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.delete_job(job_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def disable_job(self, job_id: str):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.disable_job(job_id)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    def run_pipeline(self, experiment_id: str, job_name: str, pipeline_package_path: Optional[str] = None,
                     params: Optional[dict] = None, pipeline_id: Optional[str] = None,
                     version_id: Optional[str] = None, pipeline_root: Optional[str] = None,
                     enable_caching: Optional[str] = None, service_account: Optional[str] = None):
        try:
            self._connect_kfp_client()
            result = self.kfp_client.run_pipeline(experiment_id=experiment_id, job_name=job_name,
                                                  pipeline_package_path=pipeline_package_path,
                                                  params=params, pipeline_id=pipeline_id, version_id=version_id,
                                                  pipeline_root=pipeline_root, enable_caching=enable_caching,
                                                  service_account=service_account)
            return response(result.to_dict(), Render.to_raw_content)
        except ApiException or kfp_server_api.ApiException as e:
            return error_with_message(e)

    # def create_run_from_pipeline_func(self, pipeline_func: Callable, arguments: Mapping[str, str],
    #                                   run_name: Optional[str] = None, experiment_name: Optional[str] = None,
    #                                   pipeline_conf: Optional[dsl.PipelineConf] = None,
    #                                   mode: dsl.PipelineExecutionMode = dsl.PipelineExecutionMode.V1_LEGACY,
    #                                   launcher_image: Optional[str] = None, pipeline_root: Optional[str] = None,
    #                                   enable_caching: Optional[bool] = None):
    #     try:
    #         self._connect_kfp_client()
    #         result = self.kfp_client.create_run_from_pipeline_func(pipeline_func=pipeline_func, arguments=arguments,
    #                                                                run_name=run_name,
    #                                                                experiment_name=experiment_name,
    #                                                                pipeline_conf=pipeline_conf,
    #                                                                namespace=self.namespace,
    #                                                                mode=mode, launcher_image=launcher_image,
    #                                                                pipeline_root=pipeline_root,
    #                                                                enable_caching=enable_caching,
    #                                                                service_account=self.sa_name)
    #         return response(result.to_dict(), Render.to_raw_content)
    #     except ApiException or kfp_server_api.ApiException as e:
    #         return error_with_message(e)
