from pydantic import BaseModel

from src.kubernetes_client.models import Pod, Metadata


class Notebook(BaseModel):
    metadata: Metadata
    template_pod: Pod
