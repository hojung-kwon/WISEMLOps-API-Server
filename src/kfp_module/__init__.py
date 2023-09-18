from src.kfp_module.config import get_kube_config_path, get_kubeflow_pipelines_endpoint
from src.kfp_module.service import KfpService

kfp_service = KfpService(
    host=get_kubeflow_pipelines_endpoint(),
    config_file=get_kube_config_path()
)
