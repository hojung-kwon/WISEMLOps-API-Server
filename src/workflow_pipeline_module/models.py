from sqlalchemy import Column, String, DateTime, Integer, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Pipeline(Base):
    __tablename__ = "pipeline"
    pipeline_id = Column(String, primary_key=True, index=True)
    pipeline_name = Column(String, index=True)
    pipeline_description = Column(String)
    version_name = Column(String)
    version_description = Column(String)
    nodes = Column(JSON)
    edges = Column(JSON)
    position = Column(JSON)
    zoom = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

