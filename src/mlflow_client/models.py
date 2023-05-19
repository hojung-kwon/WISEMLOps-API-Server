from typing import Optional, Dict, Any

from pydantic import BaseModel


class Tag(BaseModel):
    key: str
    value: Any = None


class ExperimentInfo(BaseModel):
    name: str
    artifact_location: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None


class ExperimentOptions(BaseModel):
    name: str = ""
    tag: Optional[Tag] = None


class ModelVersionInfo(BaseModel):
    name: str
    source: str
    run_id: Optional[str] = None
    tags: Optional[Dict[str, Any]] = None
    run_link: Optional[str] = None
    description: Optional[str] = None
    await_creation_for: int = 300


class ModelVersionOptions(BaseModel):
    archive_existing_version: bool = False
    description: Optional[str] = None
    tag: Optional[Tag] = None


class RegisteredModelInfo(BaseModel):
    name: str
    tags: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class RegisteredModelOptions(BaseModel):
    name: str = ""
    alias: Optional[str] = None
    description: Optional[str] = None
    tag: Optional[Tag] = None


class RunInfo(BaseModel):
    experiment_id: str
    start_time: Optional[int] = None
    tags: Optional[Dict[str, Any]] = None
    run_name: Optional[str] = None


class RunOptions(BaseModel):
    name: str = ""
    tag: Optional[Tag] = None
    status: Optional[str] = None
    end_time: Optional[int] = None
