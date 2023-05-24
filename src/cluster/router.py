from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models import APIResponseModel
from src.cluster import cluster_service
from src.cluster.models import \
    Volume, VolumeClaim, \
    ConfigMap, Secret, \
    Pod, Deployment, \
    Service, Ingress, Metadata

router = APIRouter(
    prefix="/cluster",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("/nodes", tags=["node"], response_model=APIResponseModel)
async def get_nodes():
    return cluster_service.get_nodes()


@router.get("/namespaces", tags=["namespace"], response_model=APIResponseModel)
async def get_namespaces():
    return cluster_service.get_namespaces()


@router.post("/namespaces/", tags=["namespace"], response_model=APIResponseModel)
async def create_namespace(metadata: Metadata):
    return cluster_service.create_namespace(metadata)


@router.delete("/namespaces/{namespace}", tags=["namespace"], response_model=APIResponseModel)
async def delete_namespace(namespace: str):
    return cluster_service.delete_namespace(namespace)


@router.patch("/namespaces/{namespace}", tags=["namespace"], response_model=APIResponseModel)
async def update_namespace(namespace: str, labels: dict = None, istio: bool = False):
    return cluster_service.update_namespace(namespace, labels, istio)


@router.get("/volumes", tags=["volume"], response_model=APIResponseModel)
async def get_volumes():
    return cluster_service.get_volumes()


@router.post("/volumes", tags=["volume"], response_model=APIResponseModel)
async def create_volume(pv: Volume):
    return cluster_service.create_volume(pv)


@router.delete("/volumes/{name}", tags=["volume"], response_model=APIResponseModel)
async def delete_volume(name: str):
    return cluster_service.delete_volume(name)


@router.get("/namespaces/{namespace}/volumeclaims", tags=["volumeclaim"], response_model=APIResponseModel)
async def get_volume_claims(namespace: str = 'default'):
    return cluster_service.get_volume_claims(namespace)


@router.post("/namespaces/{namespace}/volumeclaims", tags=["volumeclaim"], response_model=APIResponseModel)
async def create_volume_claim(namespace: str, pvc: VolumeClaim):
    return cluster_service.create_volume_claim(namespace, pvc)


@router.delete("/namespaces/{namespace}/volumeclaims/{name}", tags=["volumeclaim"], response_model=APIResponseModel)
async def delete_volume_claim(namespace: str, name: str):
    return cluster_service.delete_volume_claim(namespace, name)


@router.get("/namespaces/{namespace}/configmaps", tags=["configmap"], response_model=APIResponseModel)
async def get_config_maps(namespace: str = 'default'):
    return cluster_service.get_config_maps(namespace)


@router.post("/namespaces/{namespace}/configmaps", tags=["configmap"], response_model=APIResponseModel)
async def create_config_map(namespace: str, config_map: ConfigMap):
    return cluster_service.create_config_map(namespace, config_map)


@router.delete("/namespaces/{namespace}/configmaps/{name}", tags=["configmap"], response_model=APIResponseModel)
async def delete_config_map(namespace: str, name: str):
    return cluster_service.delete_config_map(namespace, name)


@router.get("/namespaces/{namespace}/secrets", tags=["secret"], response_model=APIResponseModel)
async def get_secrets(namespace: str = 'default'):
    return cluster_service.get_secrets(namespace)


@router.post("/namespaces/{namespace}/secrets", tags=["secret"], response_model=APIResponseModel)
async def create_secret(namespace: str, secret: Secret):
    return cluster_service.create_secret(namespace, secret)


@router.delete("/namespaces/{namespace}/secrets/{name}", tags=["secret"], response_model=APIResponseModel)
async def delete_secret(namespace: str, name: str):
    return cluster_service.delete_secret(namespace, name)


@router.get("/namespaces/{namespace}/pods", tags=["pod"], response_model=APIResponseModel)
async def get_pods(namespace: str = 'default'):
    return cluster_service.get_pods(namespace)


@router.get("/namespaces/{namespace}/pods/{name}/logs", tags=["pod"], response_model=APIResponseModel)
async def get_pod_logs(namespace: str, name: str,):
    return cluster_service.get_pod_logs(namespace, name)


@router.get("/namespaces/{namespace}/pods/{name}/logs/{container}", tags=["pod"], response_model=APIResponseModel)
async def get_container_logs(namespace: str, name: str, container: str):
    return cluster_service.get_container_logs(namespace, name, container)


@router.post("/namespaces/{namespace}/pods", tags=["pod"], response_model=APIResponseModel)
async def create_namespaced_pod(namespace: str, pod: Pod):
    return cluster_service.create_pod(namespace, pod)


@router.delete("/namespaces/{namespace}/pods/{name}", tags=["pod"], response_model=APIResponseModel)
async def delete_namespaced_pod(namespace: str, name: str):
    return cluster_service.delete_pod(namespace, name)


@router.get("/namespaces/{namespace}/deployments", tags=["deployment"], response_model=APIResponseModel)
async def get_deployments(namespace: str = 'default'):
    return cluster_service.get_deployments(namespace)


@router.post("/namespaces/{namespace}/deployments", tags=["deployment"], response_model=APIResponseModel)
async def create_deployment(namespace: str, deployment: Deployment):
    return cluster_service.create_deployment(namespace, deployment)


@router.delete("/namespaces/{namespace}/deployments/{name}", tags=["deployment"], response_model=APIResponseModel)
async def delete_deployment(namespace: str, name: str):
    return cluster_service.delete_deployment(namespace, name)


@router.get("/namespaces/{namespace}/services", tags=["service"], response_model=APIResponseModel)
async def get_services(namespace: str = 'default'):
    return cluster_service.get_services(namespace)


@router.post("/namespaces/{namespace}/services", tags=["service"], response_model=APIResponseModel)
async def create_service(namespace: str, service: Service):
    return cluster_service.create_service(namespace, service)


@router.delete("/namespaces/{namespace}/services/{name}", tags=["service"], response_model=APIResponseModel)
async def delete_service(namespace: str, name: str):
    return cluster_service.delete_service(namespace, name)


@router.get("/namespaces/{namespace}/ingresses", tags=["ingress"], response_model=APIResponseModel)
async def get_ingresses(namespace: str = 'default'):
    return cluster_service.get_ingresses(namespace)


@router.post("/namespaces/{namespace}/ingresses", tags=["ingress"], response_model=APIResponseModel)
async def create_ingress(namespace: str, ingress: Ingress):
    return cluster_service.create_ingress(namespace, ingress)


@router.delete("/namespaces/{namespace}/ingresses/{name}", tags=["ingress"], response_model=APIResponseModel)
async def delete_ingress(namespace: str, name: str):
    return cluster_service.delete_ingress(namespace, name)