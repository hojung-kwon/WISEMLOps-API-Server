from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src import app_config
from src.workflow_pipeline.service import WorkflowPipelineService

SQLALCHEMY_DATABASE_URL = app_config.SQLALCHEMY_DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# connect_args={"check_same_thread": False} : SQLite에서만 필요함. 타 DB연동시 connect_args={"check_same_thread": False} 제거
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


workflow_pipeline_service = WorkflowPipelineService()