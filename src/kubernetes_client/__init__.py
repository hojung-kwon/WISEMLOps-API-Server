from src.kubernetes_client.client import ClientFactory
from src.kubernetes_client.cluster.service import ClusterService
from src.kubernetes_client.crds.service import CrdService

cluster_service = ClusterService(
    cluster_client=ClientFactory.create_core_client(),
    deployment_client=ClientFactory.create_deployment_client(),
    network_client=ClientFactory.create_networking_client()
)

crd_service = CrdService(
    api_client=ClientFactory.create_api_client(),
    crd_client=ClientFactory.create_crd_client()
)

