from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_pipeline_by_id(db: Session, pipeline_id: str):
    return db.query(models.Pipeline).filter(models.Pipeline.pipeline_id == pipeline_id).one_or_none()


def get_pipelines(db: Session, pipeline_name: Optional[str] = None, skip: int = 0, limit: int = 100):
    if pipeline_name is None or pipeline_name.strip() == "":
        return db.query(models.Pipeline).offset(skip).limit(limit).all()
    return db.query(models.Pipeline).filter(models.Pipeline.pipeline_name == pipeline_name).offset(skip).limit(
        limit).all()


def create_pipeline(db: Session, pipeline: schemas.Pipeline):
    db_pipeline = get_pipeline_by_id(db, pipeline_id=pipeline.pipeline_id)
    if db_pipeline:
        raise HTTPException(status_code=400, detail="already registered")

    if pipeline.created_at is None:
        pipeline.created_at = datetime.now()

    if pipeline.updated_at is None:
        pipeline.updated_at = datetime.now()

    db_pipeline = models.Pipeline(pipeline_id=pipeline.pipeline_id, pipeline_name=pipeline.pipeline_name,
                                  pipeline_description=pipeline.pipeline_description, nodes=pipeline.nodes,
                                  edges=pipeline.edges, position=pipeline.position, zoom=pipeline.zoom,
                                  created_at=pipeline.created_at, updated_at=pipeline.updated_at)

    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline
