from sqlalchemy import Column, String, DateTime

from .database_config import Base


class Pipeline(Base):
    __tablename__ = "pipeline"
    pipeline_name = Column(String, primary_key=True, index=True)
    nodes = Column(String)
    edges = Column(String)
    position = Column(String)
    zoom = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)