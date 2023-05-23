from pydantic import BaseModel

from src.cluster.models import Pod, Metadata


class Notebook(BaseModel):
    metadata: Metadata
    template_pod: Pod
