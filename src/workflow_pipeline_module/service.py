from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.workflow_pipeline_module.exceptions import PipelineCreateError
from src.workflow_pipeline_module.models import Pipeline
from src.workflow_pipeline_module.schemas import PipelineDto


class WorkflowPipelineService:
    def __init__(self):
        pass

    @staticmethod
    def get_pipeline_by_id(db: Session, pipeline_id: str):
        pipeline_result = db.query(Pipeline).filter(Pipeline.pipeline_id == pipeline_id).one_or_none()
        return pipeline_result

    @staticmethod
    def get_pipelines(db: Session, pipeline_name: Optional[str] = None, skip: int = 0, limit: int = 100):
        if pipeline_name is None or pipeline_name.strip() == "":
            return db.query(Pipeline).offset(skip).limit(limit).all()
        pipeline_result = db.query(Pipeline) \
            .filter(Pipeline.pipeline_name == pipeline_name).offset(skip).limit(limit).all()
        return pipeline_result

    @staticmethod
    def create_pipeline(db: Session, pipeline: PipelineDto):
        # db_pipeline = self.get_pipelines(db, pipeline_name=pipeline.pipeline_name)
        # if db_pipeline:
        #     raise PipelineAlreadyExistsError(pipeline)
        try:
            created_at = datetime.now()
            updated_at = datetime.now()

            db_pipeline = Pipeline(pipeline_id=pipeline.pipeline_id, pipeline_name=pipeline.pipeline_name,
                                   pipeline_description=pipeline.pipeline_description, nodes=pipeline.nodes,
                                   version_info=pipeline.version_info,
                                   edges=pipeline.edges, position=pipeline.position, zoom=pipeline.zoom,
                                   created_at=created_at, updated_at=updated_at)
            db.add(db_pipeline)
            db.commit()
            db.refresh(db_pipeline)
        except PipelineCreateError as pe:
            raise PipelineCreateError(pipeline, pe.message)
        return db_pipeline
