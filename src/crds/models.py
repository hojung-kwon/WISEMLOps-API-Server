from pydantic import BaseModel

from src.cluster.models import Pod


class Notebook(BaseModel):
    name: str
    labels: dict = {
        "access-ml-pipeline": "true",
        "sidecar.istio.io/inject": "true"
    }
    annotations: dict = {
        "notebooks.kubeflow.org/server-type": "jupyter"
    }
    template_pod: Pod
