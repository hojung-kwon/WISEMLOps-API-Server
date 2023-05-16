from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.models import APIResponseModel
from src.cluster.service import cluster_service

router = APIRouter(
    prefix="/cluster",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)  # APIRouter 변수명은 원하는대로 설정 가능


@router.get("/nodes", tags=["node"], response_model=APIResponseModel)
async def get_nodes():
    return cluster_service.get_nodes()


@router.get("/namespaces", tags=["namespace"], response_model=APIResponseModel)
async def get_namespaces():
    return cluster_service.get_namespaces()


@router.post("/namespaces/{namespace}", tags=["namespace"], response_model=APIResponseModel)
async def create_namespace(namespace: str, labels: dict = None, istio: bool = False):
    return cluster_service.create_namespace(namespace, labels, istio)


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
async def create_volume(
        name: str,
        size: str = '3Gi',
        volume_mode: str = 'Filesystem',
        access_mode: str = 'ReadWriteOnce',
        storage_class: str = 'default-storage-class',
        policy: str = 'Delete',
        volume_type: str = 'nfs'):
    return cluster_service.create_volume(name, size, volume_mode, access_mode, storage_class, policy, volume_type)


@router.delete("/volumes/{name}", tags=["volume"], response_model=APIResponseModel)
async def delete_volume(name: str):
    return cluster_service.delete_volume(name)


@router.get("/namespaces/{namespace}/services", tags=["service"], response_model=APIResponseModel)
async def get_services(namespace: str = 'default'):
    return cluster_service.get_services(namespace)


@router.get("/namespaces/{namespace}/secrets", tags=["secret"], response_model=APIResponseModel)
async def get_secrets(namespace: str = 'default'):
    return cluster_service.get_secrets(namespace)


@router.get("/namespaces/{namespace}/pods", tags=["pod"], response_model=APIResponseModel)
async def get_list_namespaced_pod(namespace: str = 'default'):
    return cluster_service.get_pods(namespace)


@router.get("/namespaces/{namespace}/volumeclaims", tags=["volumeclaim"], response_model=APIResponseModel)
async def get_volume_claims(namespace: str = 'default'):
    return cluster_service.get_volume_claims(namespace)


@router.get("/namespaces/{namespace}/configmaps", tags=["configmap"], response_model=APIResponseModel)
async def get_config_maps(namespace: str = 'default'):
    return cluster_service.get_config_maps(namespace)


