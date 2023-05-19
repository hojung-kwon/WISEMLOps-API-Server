from typing import Optional

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_client import service
from src.mlflow_client.models import ExperimentInfo, ModelVersionInfo, ModelVersionOptions, RegisteredModelInfo, \
    RegisteredModelOptions, ExperimentOptions, RunInfo, RunOptions
from src.models import APIResponseModel

router = APIRouter(
    prefix="/mlflow",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.post("/experiment", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def create_experiment(experiment_info: ExperimentInfo):
    return service.create_experiment(experiment_info.name, artifact_location=experiment_info.artifact_location,
                                     tags=experiment_info.tags)


@router.get("/experiment", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def search_experiments(view_type: int = 1, max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                             order_by: Optional[str] = None, page_token=None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_experiments(view_type=view_type, max_results=max_results, filter_string=filter_string,
                                      order_by=order_by_list, page_token=page_token)


@router.get("/experiment/{experiment_id}", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def get_experiment(experiment_id: int):
    return service.get_experiment(str(experiment_id))


@router.delete("/experiment/{experiment_id}", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def delete_experiment(experiment_id: int):
    return service.delete_experiment(str(experiment_id))


@router.post("/experiment/{experiment_id}/restore", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def restore_experiment(experiment_id: int):
    return service.restore_experiment(str(experiment_id))


@router.put("/experiment/{experiment_id}/name", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def rename_experiment(experiment_id: int, experiment_options: ExperimentOptions):
    return service.rename_experiment(str(experiment_id), experiment_options.name)


@router.put("/experiment/{experiment_id}/tag", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def set_experiment_tag(experiment_id: int, experiment_options: ExperimentOptions):
    tag = experiment_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    return service.set_experiment_tag(str(experiment_id), key, value)


@router.get("/experiment/name/{experiment_name}", tags=["mlflow / experiment"], response_model=APIResponseModel)
async def get_experiment_by_name(experiment_name: str):
    return service.get_experiment_by_name(experiment_name)


@router.post("/model-version", tags=["mlflow / model-version"], response_model=APIResponseModel)
async def create_model_version(model_version_info: ModelVersionInfo):
    return service.create_model_version(model_version_info.name, model_version_info.source,
                                        run_id=model_version_info.run_id, tags=model_version_info.tags,
                                        run_link=model_version_info.run_link,
                                        description=model_version_info.description,
                                        await_creation_for=model_version_info.await_creation_for)


@router.get("/model-version", tags=["mlflow / model-version"], response_model=APIResponseModel)
async def search_model_versions(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                order_by: Optional[str] = None, page_token=None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_model_versions(max_results=max_results, filter_string=filter_string, order_by=order_by_list,
                                         page_token=page_token)


@router.get("/model-version/{model_name}/latest", tags=["mlflow / model-version"], response_model=APIResponseModel)
async def get_latest_versions(model_name: str, stage: str = None):
    stages = None
    if stage:
        stages = [stage]
    return service.get_latest_versions(model_name, stages)


@router.get("/model-version/{model_name}/{version}", tags=["mlflow / model-version"], response_model=APIResponseModel)
async def get_model_version(model_name: str, version: int):
    return service.get_model_version(model_name, str(version))


@router.delete("/model-version/{model_name}/{version}", tags=["mlflow / model-version"],
               response_model=APIResponseModel)
async def delete_model_version(model_name: str, version: int):
    return service.delete_model_version(model_name, str(version))


@router.put("/model-version/{model_name}/{version}/description", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def update_model_version(model_name: str, version: int, model_version_options: ModelVersionOptions):
    return service.update_model_version(model_name, str(version), model_version_options.description)


@router.get("/model-version/{model_name}/{version}/uri", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def get_model_version_download_uri(model_name: str, version: int):
    return service.get_model_version_download_uri(model_name, str(version))


@router.get("/model-version/{model_name}/{version}/stages", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def get_model_version_stages(model_name: str, version: int):
    return service.get_model_version_stages(model_name, str(version))


@router.put("/model-version/{model_name}/{version}/{stage}", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def transition_model_version_stage(model_name: str, version: int, stage: str,
                                         model_version_options: ModelVersionOptions):
    return service.transition_model_version_stage(model_name, str(version), stage,
                                                  archive_existing_versions=model_version_options.archive_existing_version)


@router.put("/model-version/{model_name}/{version_or_stage}/tag", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def set_model_version_tag(model_name: str, version_or_stage: str, model_version_options: ModelVersionOptions):
    tag = model_version_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    version = None
    stage = None
    if version_or_stage.isdigit():
        version = version_or_stage
    else:
        stage = version_or_stage
    return service.set_model_version_tag(model_name, version=version, stage=stage, key=key, value=value)


@router.delete("/model-version/{model_name}/{version_or_stage}/tag/{tag_key}", tags=["mlflow / model-version"],
               response_model=APIResponseModel)
async def delete_model_version_tag(model_name: str, version_or_stage: str, tag_key: str):
    version = None
    stage = None
    if version_or_stage.isdigit():
        version = version_or_stage
    else:
        stage = version_or_stage
    return service.delete_model_version_tag(model_name, version=version, stage=stage, key=tag_key)


@router.get("/model-version/{model_name}/alias/{alias}", tags=["mlflow / model-version"],
            response_model=APIResponseModel)
async def get_model_version_by_alias(model_name: str, alias: str):
    return service.get_model_version_by_alias(model_name, alias)


@router.post("/registered-model", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def create_registered_model(registered_model_info: RegisteredModelInfo):
    return service.create_registered_model(registered_model_info.name, tags=registered_model_info.tags,
                                           description=registered_model_info.description)


@router.get("/registered-model", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def search_registered_models(max_results: Optional[int] = 1000, filter_string: Optional[str] = None,
                                   order_by: Optional[str] = None, page_token=None):
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_registered_models(max_results=max_results, filter_string=filter_string,
                                            order_by=order_by_list, page_token=page_token)


@router.get("/registered-model/{model_name}", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def get_registered_model(model_name: str):
    return service.get_registered_model(model_name)


@router.delete("/registered-model/{model_name}", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def delete_registered_model(model_name: str):
    return service.delete_registered_model(model_name)


@router.put("/registered-model/{model_name}/name", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def rename_registered_model(model_name: str, registered_model_options: RegisteredModelOptions):
    return service.rename_registered_model(model_name, registered_model_options.name)


@router.put("/registered-model/{model_name}/description", tags=["mlflow / registered-model"],
            response_model=APIResponseModel)
async def update_registered_model(model_name: str, registered_model_options: RegisteredModelOptions):
    return service.update_registered_model(model_name, registered_model_options.description)


@router.put("/registered-model/{model_name}/alias/{version}", tags=["mlflow / registered-model"],
            response_model=APIResponseModel)
async def set_registered_model_alias(model_name: str, version: int, registered_model_options: RegisteredModelOptions):
    return service.set_registered_model_alias(model_name, registered_model_options.alias, str(version))


@router.delete("/registered-model/{model_name}/alias/{alias}", tags=["mlflow / registered-model"],
               response_model=APIResponseModel)
async def delete_registered_model_alias(model_name: str, alias: str):
    return service.delete_registered_model_alias(model_name, alias)


@router.put("/registered-model/{model_name}/tag", tags=["mlflow / registered-model"], response_model=APIResponseModel)
async def set_registered_model_tag(model_name: str, registered_model_options: RegisteredModelOptions):
    tag = registered_model_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    return service.set_registered_model_tag(model_name, key, value)


@router.delete("/registered-model/{model_name}/tag/{tag_key}", tags=["mlflow / registered-model"],
               response_model=APIResponseModel)
async def delete_registered_model_tag(model_name: str, tag_key: str):
    return service.delete_registered_model_tag(model_name, tag_key)


@router.post("/run", tags=["mlflow / run"], response_model=APIResponseModel)
async def create_run(run_info: RunInfo):
    return service.create_run(run_info.experiment_id, start_time=run_info.start_time, tags=run_info.tags,
                              run_name=run_info.run_name)


@router.get("/run", tags=["mlflow / run"], response_model=APIResponseModel)
async def search_runs(experiment_id: int, filter_string: str = '', run_view_type: int = 1,
                      max_results: int = 1000, order_by: Optional[str] = None, page_token: Optional[str] = None):
    experiment_ids = [str(experiment_id)]
    order_by_list = None
    if order_by:
        order_by_list = order_by.split(",")
    return service.search_runs(experiment_ids, filter_string=filter_string, run_view_type=run_view_type,
                               max_results=max_results, order_by=order_by_list, page_token=page_token)


@router.get("/run/{run_id}", tags=["mlflow / run"], response_model=APIResponseModel)
async def get_run(run_id: str):
    return service.get_run(run_id)


@router.put("/run/{run_id}", tags=["mlflow / run"], response_model=APIResponseModel)
async def update_run(run_id: str, run_options: RunOptions):
    return service.update_run(run_id, status=run_options.status, name=run_options.name)


@router.delete("/run/{run_id}", tags=["mlflow / run"], response_model=APIResponseModel)
async def delete_run(run_id: str):
    return service.delete_run(run_id)


@router.get("/run/{run_id}/artifacts", tags=["mlflow / run"], response_model=APIResponseModel)
async def list_artifacts(run_id: str):
    return service.list_artifacts(run_id)


@router.post("/run/{run_id}/restore", tags=["mlflow / run"], response_model=APIResponseModel)
async def restore_run(run_id: str):
    return service.restore_run(run_id)


@router.post("/run/{run_id}/terminated", tags=["mlflow / run"], response_model=APIResponseModel)
async def set_terminated(run_id: str, run_options: RunOptions):
    return service.set_terminated(run_id, run_options.status, run_options.end_time)


@router.put("/run/{run_id}/tag", tags=["mlflow / run"], response_model=APIResponseModel)
async def set_tag(run_id: str, run_options: RunOptions):
    tag = run_options.tag
    key = None
    value = None
    if tag and tag.value:
        key = tag.key
        value = tag.value
    return service.set_tag(run_id, key, value)


@router.delete("/run/{run_id}/tag/{tag_key}", tags=["mlflow / run"], response_model=APIResponseModel)
async def delete_tag(run_id: str, tag_key: str):
    return service.delete_tag(run_id, tag_key)


@router.get("/run/{run_id}/metric/{metric_name}", tags=["mlflow / run"], response_model=APIResponseModel)
async def get_metric_history(run_id: str, metric_name: str):
    return service.get_metric_history(run_id, key=metric_name)
