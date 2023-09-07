from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.models import APIResponseModel
from src.workflow_pipeline import SessionLocal, engine
from . import service, models, schemas
from .utils import response_success, response_error

router = APIRouter(
    prefix="/pipeline",
    tags=["pipeline"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=APIResponseModel)
def create_pipeline(pipeline: schemas.Pipeline, db: Session = Depends(get_db)):
    try:
        result = service.create_pipeline(db=db, pipeline=pipeline)
        return response_success(result)
    except Exception as e:
        return response_error(e)


@router.get("", response_model=APIResponseModel)
def get_pipelines(pipeline_name: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        pipelines = service.get_pipelines(db, pipeline_name=pipeline_name, skip=skip, limit=limit)
        return response_success(pipelines)
    except Exception as e:
        return response_error(e)



@router.get("/{pipeline_id}", response_model=APIResponseModel)
def get_pipeline(pipeline_id: str, db: Session = Depends(get_db)):
    try:
        pipelines = service.get_pipeline_by_id(db, pipeline_id)
        return response_success(pipelines)
    except Exception as e:
        return response_error(e)
