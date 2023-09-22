import json

from jinja2 import TemplateError
from kfp_server_api import ApiException as KFPApiException
from kubernetes.client import ApiException as KubernetesApiException
from pydantic.json import pydantic_encoder
from sqlalchemy.orm import Session

from src.kfp_module import kfp_service
from src.kfp_module.exceptions import KFPApiError
from src.workflow_generator_module import pipeline_gen_service
from src.workflow_generator_module.exceptions import WorkflowTemplateError
from src.workflow_generator_module.schemas import PipelineInfo
from src.workflow_pipeline_module import workflow_pipeline_service
from src.workflow_pipeline_module.exceptions import PipelineCreateError
from src.workflow_pipeline_module.schemas import PipelineDto


class WorkflowPipelineService:
    def __init__(self):
        pass

    @staticmethod
    def make_pipeline(pipeline_info: PipelineInfo, db: Session):
        try:
            # workflow/kfp 호출, pipeline tar.gz 생성
            pipeline = pipeline_gen_service.make_kfp_pipeline_tar_gz(pipeline_info)

            if pipeline is None:
                raise PipelineCreateError(pipeline, 'cannot create pipeline')
        except TemplateError as te:
            raise WorkflowTemplateError(te)

        try:
            # pipeline upload
            result = kfp_service.upload_pipeline(pipeline)
        except KFPApiException or KubernetesApiException as e:
            raise KFPApiError(e)

        try:
            # db save
            pipeline_id = str(result.get('id'))
            pipeline_name = result.get('name')
            pipeline_description = result.get('description')
            version_info = json.loads(json.dumps(result.get('default_version'), default=pydantic_encoder))

            nodes = json.loads(json.dumps(pipeline_info.nodes, default=pydantic_encoder))
            edges = json.loads(json.dumps(pipeline_info.edges, default=pydantic_encoder))
            position = pipeline_info.position
            zoom = pipeline_info.zoom

            db_pipeline = PipelineDto(pipeline_id=pipeline_id,
                                      pipeline_name=pipeline_name,
                                      pipeline_description=pipeline_description,
                                      version_info=version_info,
                                      nodes=nodes,
                                      edges=edges,
                                      position=position,
                                      zoom=zoom)

            result = workflow_pipeline_service.create_pipeline(db=db, pipeline=db_pipeline)
        except PipelineCreateError as pe:
            raise PipelineCreateError(pipeline, pe.message)
        return result
