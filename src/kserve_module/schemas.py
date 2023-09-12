from typing import Optional

from pydantic import BaseModel


class InferenceServiceInfo(BaseModel):
    name: str
    namespace: str
    storage_uri: Optional[str] = None
    model_name: Optional[str] = None
    service_account_name: str = 'minio30sa'
    model_format: str = 'mlflow'
    protocol_version: str = 'v1'
