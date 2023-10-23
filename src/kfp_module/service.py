import base64
import json
import time
from typing import Optional

from kfp import Client
from kfp.dsl import base_component
from kfp_server_api import ApiException as KFPApiException
# from kfp_server_api.api import RunServiceApi, ExperimentServiceApi, PipelineServiceApi, \
#     PipelineUploadServiceApi, HealthzServiceApi
# from kfp_server_api.api_client import ApiClient
# from kfp_server_api.configuration import Configuration
from kubernetes import config, client
from kubernetes.client import ApiException as KubernetesApiException
from kubernetes.client import AuthenticationV1TokenRequest, V1ObjectMeta, V1TokenRequestSpec

from src.kfp_module.exceptions import KFPApiError
from src.kfp_module.schemas import Experiment, Pipeline, PipelineVersion, Run, RecurringRun, RunPipelinePackage, \
    RunPipelineBase


class KfpService:
    def __init__(self, host, config_file, sa_name: str = 'default-editor',
                 namespace: str = 'kubeflow-user-example-com'):
        config.load_kube_config(config_file=config_file)
        self.host = host
        self.sa_name = sa_name
        self.namespace = namespace
        self.token = None

    def is_token_expired(self):
        if self.token is None:
            return True
        payload = self.token.split(".")[1]
        payload = payload + '=' * (4 - len(payload) % 4)
        payload = base64.b64decode(payload).decode()
        payload = json.loads(payload)
        exp = payload['exp']
        now = time.time()
        if exp < now:
            return True
        return False

    @staticmethod
    def get_cluster_client():
        return client.CoreV1Api()

    def get_token(self):
        try:
            if self.is_token_expired():
                self.token = self.get_cluster_client(). \
                    create_namespaced_service_account_token(name=self.sa_name,
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
            return self.token
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_kfp_client(self):
        try:
            return Client(host=self.host, namespace=self.namespace, existing_token=self.get_token())
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    # def get_api_client(self):
    #     try:
    #         kfp_config = Configuration()
    #         kfp_config.host = self.host
    #         kfp_config.api_key['authorization'] = self.get_token()
    #         kfp_config.api_key_prefix['authorization'] = 'Bearer'
    #         return ApiClient(kfp_config)
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
    #
    # def get_run_api(self):
    #     try:
    #         return RunServiceApi(self.get_api_client())
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
    #
    # def get_experiment_api(self):
    #     try:
    #         return ExperimentServiceApi(self.get_api_client())
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
    #
    # def get_pipelines_api(self):
    #     try:
    #         return PipelineServiceApi(self.get_api_client())
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
    #
    # def get_upload_api(self):
    #     try:
    #         return PipelineUploadServiceApi(self.get_api_client())
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
    #
    # def get_healthz_api(self):
    #     try:
    #         return HealthzServiceApi(self.get_api_client())
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)

    def get_kfp_healthz(self):
        try:
            return self.get_kfp_client().get_kfp_healthz().to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_user_namespace(self):
        try:
            return self.get_kfp_client().get_user_namespace()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_experiments(self, filter_option: Optional[str] = None, page_token: str = '', page_size: int = 10,
                         sort_by: str = ''):
        try:
            return self.get_kfp_client().list_experiments(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                          filter=filter_option,
                                                          namespace=self.namespace).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_archive_experiments(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            return self.list_experiments(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                         filter_option=json.dumps({
                                             "predicates": [{
                                                 "operation": "EQUALS",
                                                 "key": "storage_state",
                                                 "stringValue": "ARCHIVED",
                                             }]
                                         }))
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_unarchive_experiments(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            return self.list_experiments(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                         filter_option=json.dumps({
                                             "predicates": [{
                                                 "operation": "EQUALS",
                                                 "key": "storage_state",
                                                 "stringValue": "AVAILABLE",
                                             }]
                                         }))
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def create_experiment(self, experiment: Experiment):
        try:
            return self.get_kfp_client().create_experiment(name=experiment.name, description=experiment.description,
                                                           namespace=self.namespace).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_experiment(self, experiment_id: Optional[str] = None, experiment_name: Optional[str] = None):
        try:
            return self.get_kfp_client().get_experiment(experiment_id=experiment_id, experiment_name=experiment_name,
                                                        namespace=self.namespace).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def archive_experiment(self, experiment_id: str):
        try:
            return self.get_kfp_client().archive_experiment(experiment_id=experiment_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def unarchive_experiment(self, experiment_id: str):
        try:
            return self.get_kfp_client().unarchive_experiment(experiment_id=experiment_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def delete_experiment(self, experiment_id: str):
        try:
            return self.get_kfp_client().delete_experiment(experiment_id=experiment_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_pipelines(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        try:
            return self.get_kfp_client().list_pipelines(page_token=page_token, page_size=page_size,
                                                        sort_by=sort_by).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def upload_pipeline(self, pipeline: Pipeline):
        try:
            return self.get_kfp_client().upload_pipeline(pipeline_package_path=pipeline.pipeline_package_path,
                                                         pipeline_name=pipeline.pipeline_name,
                                                         description=pipeline.description).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_pipeline(self, pipeline_id: str):
        try:
            return self.get_kfp_client().get_pipeline(pipeline_id=pipeline_id).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def delete_pipeline(self, pipeline_id: str):
        try:
            return self.get_kfp_client().delete_pipeline(pipeline_id=pipeline_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_pipeline_id(self, name: Optional[str]):
        try:
            return self.get_kfp_client().get_pipeline_id(name)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_pipeline_versions(self, pipeline_id: str, page_token: str = '', page_size: int = 10,
                               sort_by: str = ''):
        try:
            return self.get_kfp_client().list_pipeline_versions(pipeline_id=pipeline_id, page_token=page_token,
                                                                page_size=page_size, sort_by=sort_by).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def upload_pipeline_version(self, pipeline_version: PipelineVersion):
        try:
            return self.get_kfp_client().upload_pipeline_version(
                pipeline_package_path=pipeline_version.pipeline_package_path,
                pipeline_version_name=pipeline_version.pipeline_version_name,
                pipeline_id=pipeline_version.pipeline_id,
                pipeline_name=pipeline_version.pipeline_name,
                description=pipeline_version.description).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def delete_pipeline_version(self, pipeline_id: str, version_id: str):
        try:
            return self.get_kfp_client().delete_pipeline_version(pipeline_id=pipeline_id,
                                                                 pipeline_version_id=version_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_pipeline_version(self, pipeline_id: str, version_id: str):
        try:
            return self.get_kfp_client().get_pipeline_version(pipeline_id=pipeline_id,
                                                              pipeline_version_id=version_id).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                  experiment_id: Optional[str] = None):
        try:
            return self.get_kfp_client().list_runs(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                   experiment_id=experiment_id,
                                                   namespace=self.namespace).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def run_pipeline(self, run: Run):
        try:
            return self.get_kfp_client().run_pipeline(experiment_id=run.experiment_id,
                                                      job_name=run.job_name,
                                                      pipeline_package_path=run.pipeline_package_path,
                                                      params=run.params,
                                                      pipeline_id=run.pipeline_id,
                                                      version_id=run.version_id,
                                                      pipeline_root=run.pipeline_root,
                                                      enable_caching=run.enable_caching,
                                                      service_account=self.sa_name)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def create_run_from_pipeline_package(self, run: RunPipelinePackage):
        try:
            return self.get_kfp_client().create_run_from_pipeline_package(pipeline_file=run.pipeline_file,
                                                                          arguments=run.arguments,
                                                                          run_name=run.run_name,
                                                                          experiment_name=run.experiment_name,
                                                                          namespace=self.namespace,
                                                                          pipeline_root=run.pipeline_root,
                                                                          enable_caching=run.enable_caching,
                                                                          service_account=self.sa_name,
                                                                          experiment_id=run.experiment_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def create_run_from_pipeline_func(self, pipeline_func: base_component.BaseComponent, run: RunPipelineBase):
        try:
            return self.get_kfp_client().create_run_from_pipeline_func(pipeline_func=pipeline_func,
                                                                       arguments=run.arguments,
                                                                       run_name=run.run_name,
                                                                       experiment_name=run.experiment_name,
                                                                       namespace=self.namespace,
                                                                       pipeline_root=run.pipeline_root,
                                                                       enable_caching=run.enable_caching,
                                                                       service_account=self.sa_name,
                                                                       experiment_id=run.experiment_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_run(self, run_id: str):
        try:
            return self.get_kfp_client().get_run(run_id).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def wait_for_run_completion(self, run_id: str, timeout: int):
        try:
            return self.get_kfp_client().wait_for_run_completion(run_id, timeout=timeout).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def list_recurring_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                            experiment_id: Optional[str] = None):
        try:
            return self.get_kfp_client().list_recurring_runs(page_token=page_token, page_size=page_size,
                                                             sort_by=sort_by,
                                                             experiment_id=experiment_id,
                                                             namespace=self.namespace).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def create_recurring_run(self, recurring_run: RecurringRun):
        try:
            return self.get_kfp_client().create_recurring_run(experiment_id=recurring_run.experiment_id,
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
                                                              service_account=self.sa_name).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def get_recurring_run(self, recurring_run_id: str):
        try:
            return self.get_kfp_client().get_recurring_run(recurring_run_id=recurring_run_id).to_dict()
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def delete_recurring_run(self, recurring_run_id: str):
        try:
            return self.get_kfp_client().delete_recurring_run(recurring_run_id=recurring_run_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def disable_recurring_run(self, recurring_run_id: str):
        try:
            return self.get_kfp_client().disable_recurring_run(recurring_run_id=recurring_run_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    def enable_recurring_run(self, recurring_run_id: str):
        try:
            return self.get_kfp_client().enable_recurring_run(recurring_run_id=recurring_run_id)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

    # def read_artifact(self, run_id: str, node_id: str, artifact_name: str):
    #     try:
    #         return self.get_run_api().read_artifact(run_id, node_id, artifact_name)
    #     except KFPApiException or KubernetesApiException as e:
    #         raise KFPApiError(e)
