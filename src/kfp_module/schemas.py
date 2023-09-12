from typing import Optional, Mapping

from pydantic import BaseModel


class Experiment(BaseModel):
    name: str
    description: Optional[str] = None


class Pipeline(BaseModel):
    pipeline_name: str
    pipeline_package_path: str
    description: Optional[str] = None


class PipelineVersion(BaseModel):
    pipeline_version_name: str
    pipeline_package_path: str
    pipeline_id: Optional[str] = None
    pipeline_name: Optional[str] = None
    description: Optional[str] = None


class Run(BaseModel):
    pipeline_file: str
    arguments: Mapping[str, str]
    run_name: Optional[str] = None
    experiment_name: Optional[str] = None
    pipeline_root: Optional[str] = None
    enable_caching: Optional[bool] = None


class RecurringRun(BaseModel):
    experiment_id: str
    job_name: str
    description: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    interval_second: Optional[int] = None
    cron_expression: Optional[str] = None
    max_concurrency: Optional[int] = 1
    no_catchup: Optional[bool] = None
    params: Optional[dict] = None
    pipeline_package_path: Optional[str] = None
    pipeline_id: Optional[str] = None
    version_id: Optional[str] = None
    enabled: bool = True
    enable_caching: Optional[bool] = None
