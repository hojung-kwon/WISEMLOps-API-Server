from src.kubernetes_module.client import ClientFactory
from src.kubernetes_module.cluster.service import ClusterService
from src.kubernetes_module.config import load_cluster_config
from src.kubernetes_module.crds.service import CrdService

load_cluster_config()

cluster_service = ClusterService(
    cluster_client=ClientFactory.get_core_client(),
    deployment_client=ClientFactory.get_deployment_client(),
    network_client=ClientFactory.get_networking_client()
)

crd_service = CrdService(
    api_client=ClientFactory.get_api_client(),
    crd_client=ClientFactory.create_crd_client()
)
