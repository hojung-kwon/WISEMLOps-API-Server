from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.workflow_pipeline_module.config import get_sqlalchemy_database_url
from src.workflow_pipeline_module.service import WorkflowPipelineService

engine = create_engine(
    get_sqlalchemy_database_url(), connect_args={"check_same_thread": False}
)
# connect_args={"check_same_thread": False} : SQLite에서만 필요함. 타 DB연동시 connect_args={"check_same_thread": False} 제거
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

workflow_pipeline_service = WorkflowPipelineService()
