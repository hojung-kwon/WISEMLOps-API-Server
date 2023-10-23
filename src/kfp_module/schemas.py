import re
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, validator

from src.kfp_module.exceptions import RequestValidationError


class Experiment(BaseModel):
    name: str = Field(title="Experiment 명칭", description="The name of the experiment.")
    description: Optional[str] = Field(title="Experiment 설명", description="Description of the experiment.",
                                       default=None)

    @classmethod
    @validator('name')
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v


class Pipeline(BaseModel):
    pipeline_package_path: str = Field(title="Pipeline 패키지 파일 경로", description="Local path to the pipeline package.")
    pipeline_name: Optional[str] = Field(title="Pipeline 명칭",
                                         description="Optional. Name of the pipeline to be shown in the UI.",
                                         default=None)
    description: Optional[str] = Field(title="Pipeline 설명",
                                       description="Optional. Description of the pipeline to be shown in the UI.",
                                       default=None)

    @classmethod
    @validator('pipeline_name')
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v


class PipelineVersion(BaseModel):
    pipeline_package_path: str = Field(title="Pipeline 패키지 파일 경로", description="Local path to the pipeline package.")
    pipeline_version_name: str = Field(title="Pipeline 버전 명칭",
                                       description="Name of the pipeline version to be shown in the UI.")
    pipeline_id: Optional[str] = Field(title="Pipeline 아이디", description="Optional. Id of the pipeline.", default=None)
    pipeline_name: Optional[str] = Field(title="Pipeline 명칭", description="Optional. Name of the pipeline.",
                                         default=None)
    description: Optional[str] = Field(title="Pipeline 버전 설명",
                                       description="Optional."
                                                   " Description of the pipeline version to be shown in the UI.",
                                       default=None)

    @classmethod
    @validator('pipeline_name')
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v


class Run(BaseModel):
    experiment_id: str = Field(title="Experiment ID",
                               description="ID of an experiment.")
    job_name: str = Field(title="Job 명칭", description="Name of the job.")
    pipeline_package_path: Optional[str] = Field(title="Pipeline 패키지 파일 경로",
                                                 description="Local path of the pipeline package"
                                                             " (the filename should end with one of the following"
                                                             " .tar.gz, .tgz, .zip, .json).",
                                                 default=None)
    params: Optional[Dict[str, Any]] = Field(title="매개 변수",
                                             description="Arguments to the pipeline function provided as a dict.",
                                             default=None)
    pipeline_id: Optional[str] = Field(title="Pipeline 아이디", description="ID of a pipeline.",
                                       default=None)
    version_id: Optional[str] = Field(title="Pipeline 버전 아이디",
                                      description="ID of the pipeline version to run."
                                                  " If both pipeline_id and version_id are specified, version_id"
                                                  " will take precendence."
                                                  " If only pipeline_id is specified, the default version of this"
                                                  " pipeline is used to create the run.",
                                      default=None)
    pipeline_root: Optional[str] = Field(title="Pipeline 결과 출력 경로",
                                         description="Root path of the pipeline outputs.",
                                         default=None)
    enable_caching: Optional[bool] = Field(title="Caching 활성화 여부",
                                           description="Whether or not to enable caching for the run."
                                                       " If not set, defaults to the compile time settings,"
                                                       " which is ``True`` for all tasks by default,"
                                                       " while users may specify different caching options"
                                                       " for individual tasks."
                                                       " If set, the setting applies to all tasks in the pipeline"
                                                       " (overrides the compile time settings)",
                                           default=None)

    @classmethod
    @validator('job_name', allow_reuse=True)
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v


class RunPipelineBase(BaseModel):
    arguments: Optional[Dict[str, Any]] = Field(title="실행 인자",
                                                description="Arguments to the pipeline function provided as a dict.",
                                                default=None)
    run_name: Optional[str] = Field(title="Run 명칭", description="Name of the run to be shown in the UI.",
                                    default=None)
    experiment_name: Optional[str] = Field(title="Experiment 명칭",
                                           description="Name of the experiment to add the run to."
                                                       " You cannot specify both experiment_name and experiment_id.",
                                           default=None)
    pipeline_root: Optional[str] = Field(title="Pipeline 결과 출력 경로",
                                         description="Root path of the pipeline outputs.",
                                         default=None)
    enable_caching: Optional[bool] = Field(title="Caching 활성화 여부",
                                           description="Whether or not to enable caching for the run."
                                                       " If not set, defaults to the compile time settings,"
                                                       " which is ``True`` for all tasks by default,"
                                                       " while users may specify different caching options"
                                                       " for individual tasks."
                                                       " If set, the setting applies to all tasks in the pipeline"
                                                       " (overrides the compile time settings)",
                                           default=None)
    experiment_id: Optional[str] = Field(title="Experiment ID",
                                         description="ID of the experiment to add the run to."
                                                     " You cannot specify both experiment_id and experiment_name.",
                                         default=None)

    @classmethod
    @validator('run_name', allow_reuse=True)
    @validator('experiment_name', allow_reuse=True)
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v


class RunPipelinePackage(RunPipelineBase):
    pipeline_file: str = Field(title="Pipeline 패키지 파일 경로", description="A compiled pipeline package file.")


class RecurringRun(BaseModel):
    experiment_id: str = Field(title="Experiment 아이디", description="The string id of an experiment.")
    job_name: str = Field(title="Job 명칭", description="Name of the job.")
    description: Optional[str] = Field(title="Job 설명", description="An optional job description.", default=None)
    start_time: Optional[str] = Field(title="시작 시간",
                                      description="RFC3339 time string of the time when to start the job.",
                                      default=None)
    end_time: Optional[str] = Field(title="종료 시간",
                                    description="RFC3339 time string of the time when to end the job.",
                                    default=None)
    interval_second: Optional[int] = Field(title="시간 간격",
                                           description="Integer indicating the seconds"
                                                       " between two recurring runs in for a periodic schedule.",
                                           default=None)
    cron_expression: Optional[str] = Field(title="Cron식 표현",
                                           description="A cron expression representing a set of times,"
                                                       " using 6 space-separated fields,"
                                                       " e.g. '0 0 9 ? * 2-6'.",
                                           default=None)
    max_concurrency: Optional[int] = Field(title="최대 동시성",
                                           description="Integer indicating how many jobs can be run in parallel.",
                                           default=1)
    no_catchup: Optional[bool] = Field(title="Catch Up 비활성화 여부",
                                       description="Whether the recurring run should catch up if behind schedule."
                                                   " For example,"
                                                   " if the recurring run is paused for a while"
                                                   " and re-enabled afterwards."
                                                   " If no_catchup=False,"
                                                   " the scheduler will catch up on (back fill) each missed interval."
                                                   " Otherwise,"
                                                   " it only schedules the latest interval if more than one interval"
                                                   " is ready to be scheduled."
                                                   " Usually, if your pipeline handles back fill internally,"
                                                   " you should turn catchup off to avoid duplicate back fill."
                                                   " (default: {False})",
                                       default=None)
    pipeline_package_path: Optional[str] = Field(title="Pipeline 패키지 파일 경로",
                                                 description="Local path of the pipeline package"
                                                             " (the filename should end with one of the following"
                                                             " .tar.gz, .tgz, .zip, .json).",
                                                 default=None)
    params: Optional[dict] = Field(title="매개 변수",
                                   description="Arguments to the pipeline function provided as a dict.",
                                   default=None)
    pipeline_id: Optional[str] = Field(title="Pipeline 아이디", description="ID of a pipeline.",
                                       default=None)
    version_id: Optional[str] = Field(title="Pipeline 버전 아이디",
                                      description="ID of a pipeline version."
                                                  " If both ``pipeline_id`` and ``version_id`` are specified,"
                                                  " ``version_id`` will take precedence."
                                                  " If only ``pipeline_id`` is specified,"
                                                  " the default version of this pipeline is used to create the run.",
                                      default=None)
    enabled: bool = Field(title="반복 실행 활성화 여부",
                          description="Whether to enable or disable the recurring run.",
                          default=True)
    pipeline_root: Optional[str] = Field(title="Pipeline 결과 출력 경로",
                                         description="Root path of the pipeline outputs.",
                                         default=None)
    enable_caching: Optional[bool] = Field(title="Caching 활성화 여부",
                                           description="Whether or not to enable caching for the run."
                                                       " If not set, defaults to the compile time settings,"
                                                       " which is ``True`` for all tasks by default,"
                                                       " while users may specify different caching options"
                                                       " for individual tasks."
                                                       " If set, the setting applies to all tasks in the pipeline"
                                                       " (overrides the compile time settings)",
                                           default=None)

    @classmethod
    @validator('job_name', allow_reuse=True)
    def validate_name(cls, v):
        reg = re.compile(r'\W')
        if reg.match(v):
            raise RequestValidationError(
                message="Only alphabetic characters, numbers, and underscores are allowed in the name.",
                result={"current_name": v}
            )
        return v
