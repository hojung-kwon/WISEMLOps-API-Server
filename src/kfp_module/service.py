import base64
import json
import time
from typing import Optional

from kfp import Client
from kfp_server_api import RunServiceApi, ExperimentServiceApi, PipelineServiceApi, PipelineUploadServiceApi, \
    HealthzServiceApi
from kfp_server_api.api import JobServiceApi
from kfp_server_api.api_client import ApiClient
from kfp_server_api.configuration import Configuration
from kubernetes.client import CoreV1Api, AuthenticationV1TokenRequest, V1ObjectMeta, V1TokenRequestSpec

from src.kfp_module.schemas import Experiment, Pipeline, PipelineVersion, Run, RecurringRun


class KfpService:
    def __init__(self, host, cluster_client: CoreV1Api, sa_name: str = 'default-editor',
                 namespace: str = 'kubeflow-user-example-com'):
        self.host = host
        self.cluster_client = cluster_client
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

    def get_token(self):
        if self.is_token_expired():
            self.token = self.cluster_client.create_namespaced_service_account_token(name=self.sa_name,
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

    def get_kfp_client(self):
        return Client(host=self.host, namespace=self.namespace, existing_token=self.get_token())

    def get_api_client(self):
        config = Configuration()
        config.host = self.host
        config.api_key['authorization'] = self.get_token()
        config.api_key_prefix['authorization'] = 'Bearer'
        return ApiClient(config)

    def get_job_api(self):
        return JobServiceApi(self.get_api_client())

    def get_run_api(self):
        return RunServiceApi(self.get_api_client())

    def get_experiment_api(self):
        return ExperimentServiceApi(self.get_api_client())

    def get_pipelines_api(self):
        return PipelineServiceApi(self.get_api_client())

    def get_upload_api(self):
        return PipelineUploadServiceApi(self.get_api_client())

    def get_healthz_api(self):
        return HealthzServiceApi(self.get_api_client())

    def get_kfp_healthz(self):
        return self.get_kfp_client().get_kfp_healthz().to_dict()

    def get_user_namespace(self):
        return self.get_kfp_client().get_user_namespace()

    def list_experiments(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        return self.get_kfp_client().list_experiments(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                      namespace=self.namespace).to_dict()

    def create_experiment(self, experiment: Experiment):
        return self.get_kfp_client().create_experiment(name=experiment.name, description=experiment.description,
                                                       namespace=self.namespace).to_dict()

    def get_experiment(self, experiment_id: Optional[str] = None, experiment_name: Optional[str] = None):
        return self.get_kfp_client().get_experiment(experiment_id=experiment_id, experiment_name=experiment_name,
                                                    namespace=self.namespace).to_dict()

    def archive_experiment(self, experiment_id: str):
        return self.get_kfp_client().archive_experiment(experiment_id)

    def delete_experiment(self, experiment_id: str):
        return self.get_kfp_client().delete_experiment(experiment_id)

    def list_pipelines(self, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        return self.get_kfp_client().list_pipelines(page_token=page_token, page_size=page_size,
                                                    sort_by=sort_by).to_dict()

    def upload_pipeline(self, pipeline: Pipeline):
        return self.get_kfp_client().upload_pipeline(pipeline_package_path=pipeline.pipeline_package_path,
                                                     pipeline_name=pipeline.pipeline_name,
                                                     description=pipeline.description).to_dict()

    def get_pipeline(self, pipeline_id: str):
        return self.get_kfp_client().get_pipeline(pipeline_id).to_dict()

    def list_pipeline_versions(self, pipeline_id: str, page_token: str = '', page_size: int = 10, sort_by: str = ''):
        return self.get_kfp_client().list_pipeline_versions(pipeline_id=pipeline_id, page_token=page_token,
                                                            page_size=page_size, sort_by=sort_by).to_dict()

    def delete_pipeline(self, pipeline_id: str):
        return self.get_kfp_client().delete_pipeline(pipeline_id)

    def get_pipeline_id(self, name: Optional[str]):
        return self.get_kfp_client().get_pipeline_id(name)

    def upload_pipeline_version(self, pipeline_version: PipelineVersion):
        return self.get_kfp_client().upload_pipeline_version(
            pipeline_package_path=pipeline_version.pipeline_package_path,
            pipeline_version_name=pipeline_version.pipeline_version_name,
            pipeline_id=pipeline_version.pipeline_id,
            pipeline_name=pipeline_version.pipeline_name,
            description=pipeline_version.description).to_dict()

    def delete_pipeline_version(self, version_id: str):
        return self.get_kfp_client().delete_pipeline_version(version_id)

    def get_pipeline_template(self, pipeline_id: str):
        return self.get_pipelines_api().get_template(id=pipeline_id)

    def get_pipeline_version(self, version_id: str):
        return self.get_pipelines_api().get_pipeline_version(version_id=version_id)

    def get_pipeline_version_template(self, pipeline_id: str):
        return self.get_pipelines_api().get_pipeline_version_template(version_id=pipeline_id)

    def list_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                  experiment_id: Optional[str] = None):
        return self.get_kfp_client().list_runs(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                               experiment_id=experiment_id,
                                               namespace=self.namespace).to_dict()

    def create_run_from_pipeline_package(self, run: Run):
        return self.get_kfp_client().create_run_from_pipeline_package(pipeline_file=run.pipeline_file,
                                                                      arguments=run.arguments,
                                                                      run_name=run.run_name,
                                                                      experiment_name=run.experiment_name,
                                                                      namespace=self.namespace,
                                                                      pipeline_root=run.pipeline_root,
                                                                      enable_caching=run.enable_caching,
                                                                      service_account=self.sa_name)

    def get_run(self, run_id: str):
        return self.get_kfp_client().get_run(run_id).to_dict()

    def wait_for_run_completion(self, run_id: str, timeout: int):
        return self.get_kfp_client().wait_for_run_completion(run_id, timeout=timeout)

    def list_recurring_runs(self, page_token: str = '', page_size: int = 10, sort_by: str = '',
                            experiment_id: Optional[str] = None):
        return self.get_kfp_client().list_recurring_runs(page_token=page_token, page_size=page_size, sort_by=sort_by,
                                                         experiment_id=experiment_id).to_dict()

    def create_recurring_run(self, recurring_run: RecurringRun):
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

    def get_recurring_run(self, job_id: str):
        return self.get_kfp_client().get_recurring_run(job_id).to_dict()

    def delete_job(self, job_id: str):
        return self.get_kfp_client().delete_job(job_id)

    def disable_job(self, job_id: str):
        return self.get_kfp_client().disable_job(job_id)

    def run_pipeline(self, experiment_id: str, job_name: str, pipeline_package_path: Optional[str] = None,
                     params: Optional[dict] = None, pipeline_id: Optional[str] = None,
                     version_id: Optional[str] = None, pipeline_root: Optional[str] = None,
                     enable_caching: Optional[str] = None):
        return self.get_kfp_client().run_pipeline(experiment_id=experiment_id, job_name=job_name,
                                                  pipeline_package_path=pipeline_package_path,
                                                  params=params, pipeline_id=pipeline_id, version_id=version_id,
                                                  pipeline_root=pipeline_root, enable_caching=enable_caching,
                                                  service_account=self.sa_name).to_dict()

    # def create_run_from_pipeline_func(self, pipeline_func: Callable, arguments: Mapping[str, str],
    #                                   run_name: Optional[str] = None, experiment_name: Optional[str] = None,
    #                                   pipeline_conf: Optional[dsl.PipelineConf] = None,
    #                                   mode: dsl.PipelineExecutionMode = dsl.PipelineExecutionMode.V1_LEGACY,
    #                                   launcher_image: Optional[str] = None, pipeline_root: Optional[str] = None,
    #                                   enable_caching: Optional[bool] = None):
    #     return self.get_kfp_client().create_run_from_pipeline_func(pipeline_func=pipeline_func, arguments=arguments,
    #                                                                run_name=run_name,
    #                                                                experiment_name=experiment_name,
    #                                                                pipeline_conf=pipeline_conf,
    #                                                                namespace=self.namespace,
    #                                                                mode=mode, launcher_image=launcher_image,
    #                                                                pipeline_root=pipeline_root,
    #                                                                enable_caching=enable_caching,
    #                                                                service_account=self.sa_name)

    def get_run_detail(self, run_id: str):
        return self.get_run_api().get_run(run_id)

    def read_artifact(self, run_id: str, node_id: str, artifact_name: str):
        return self.get_run_api().read_artifact(run_id, node_id, artifact_name)
