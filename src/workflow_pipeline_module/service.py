from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from src.workflow_pipeline_module import models
from src.workflow_pipeline_module.exceptions import PipelineCreateError
from src.workflow_pipeline_module.pipeline_dto import PipelineDto


class WorkflowPipelineService:
    def __init__(self):
        pass

    def get_pipeline_by_id(self, db: Session, pipeline_id: str):
        pipeline_result = db.query(models.Pipeline).filter(models.Pipeline.pipeline_id == pipeline_id).one_or_none()
        return pipeline_result

    def get_pipelines(self, db: Session, pipeline_name: Optional[str] = None, skip: int = 0, limit: int = 100):
        if pipeline_name is None or pipeline_name.strip() == "":
            return db.query(models.Pipeline).offset(skip).limit(limit).all()
        pipeline_result = db.query(models.Pipeline) \
            .filter(models.Pipeline.pipeline_name == pipeline_name).offset(skip).limit(limit).all()
        return pipeline_result

    def create_pipeline(self, db: Session, pipeline: PipelineDto):
        # db_pipeline = self.get_pipelines(db, pipeline_name=pipeline.pipeline_name)
        # if db_pipeline:
        #     raise PipelineAlreadyExistsError(pipeline)
        try:
            # TODO : pipeline upload 후, pipeline_id 얻고 넣기
            import uuid
            pipeline_id = uuid.uuid4()

            created_at = datetime.now()
            updated_at = datetime.now()

            db_pipeline = models.Pipeline(pipeline_id=pipeline_id, pipeline_name=pipeline.pipeline_name,
                                          pipeline_description=pipeline.pipeline_description, nodes=pipeline.nodes,
                                          edges=pipeline.edges, position=pipeline.position, zoom=pipeline.zoom,
                                          created_at=created_at, updated_at=updated_at)
            db.add(db_pipeline)
            db.commit()
            db.refresh(db_pipeline)
        except PipelineCreateError as pe:
            raise PipelineCreateError(pipeline, pe.message)
        return db_pipeline