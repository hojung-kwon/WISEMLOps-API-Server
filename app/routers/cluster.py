from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models import APIResponseModel
from app.client.kubernetes_client import k8s_client

router = APIRouter(
    prefix="/cluster",
    tags=["cluster"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)  # APIRouter 변수명은 원하는대로 설정 가능


@router.get("/{namespace}/pods", response_model=APIResponseModel)
async def get_list_namespaced_pod(namespace: str = 'default'):
    try:
        pods = k8s_client.list_namespaced_pod(namespace=namespace).items
        return {"result": [pod.metadata.name for pod in pods]}
    except Exception as e:
        return {"error": str(e)}


@router.get("/nodes", response_model=APIResponseModel)
async def get_list_node():
    try:
        nodes = k8s_client.list_node().items
        return {"result": [node.metadata.name for node in nodes]}
    except Exception as e:
        return {"error": str(e)}

