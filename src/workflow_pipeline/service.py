from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


def get_pipeline_by_name(db: Session, pipeline_name: str):
    return db.query(models.Pipeline).filter(models.Pipeline.pipeline_name == pipeline_name).first()


def get_pipelines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pipeline).offset(skip).limit(limit).all()


def create_pipeline(db: Session, pipeline: schemas.Pipeline):
    db_pipeline = get_pipeline_by_name(db, pipeline_name=pipeline.pipeline_name)
    if db_pipeline:
        raise HTTPException(status_code=400, detail="already registered")

    if pipeline.created_at is None:
        pipeline.created_at = datetime.now()

    if pipeline.updated_at is None:
        pipeline.updated_at = datetime.now()

    db_pipeline = models.Pipeline(pipeline_name=pipeline.pipeline_name, nodes=pipeline.nodes, edges=pipeline.edges,
                                  position=pipeline.position, zoom=pipeline.zoom, created_at=pipeline.created_at,
                                  updated_at=pipeline.updated_at)
    db.add(db_pipeline)
    db.commit()
    db.refresh(db_pipeline)
    return db_pipeline
