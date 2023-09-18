from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.workflow_pipeline_module import models
from src.workflow_pipeline_module.config import get_sqlalchemy_database_url

engine = create_engine(
    get_sqlalchemy_database_url(), connect_args={"check_same_thread": False}
)
# connect_args={"check_same_thread": False} : SQLite에서만 필요함. 타 DB연동시 connect_args={"check_same_thread": False} 제거
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
