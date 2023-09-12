from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kubernetes_module import crd_service
from src.kubernetes_module.schemas import Notebook
from src.response import Response

router = APIRouter(
    prefix="/crds",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("/namespaces/{namespace}/notebooks", tags=["notebook"], response_model=Response)
async def get_notebooks(namespace: str):
    return Response.from_result(crd_service.get_notebooks(namespace))


@router.post("/namespaces/{namespace}/notebooks", tags=["notebook"], response_model=Response)
async def create_notebook(namespace: str, notebook: Notebook = None):
    return Response.from_result(crd_service.create_notebook(namespace, notebook))


@router.delete("/namespaces/{namespace}/notebooks/{name}", tags=["notebook"], response_model=Response)
async def delete_notebook(namespace: str, name: str = ''):
    return Response.from_result(crd_service.delete_notebook(namespace, name))


@router.get("/namespaces/{namespace}/notebooks/{name}", tags=["notebook"], response_model=Response)
async def get_notebook(namespace: str, name: str):
    return Response.from_result(crd_service.get_notebook(namespace, name))


@router.get("/namespaces/{namespace}/notebooks/{name}/overview", tags=["notebook"], response_model=Response)
async def get_notebook_overview(namespace: str, name: str):
    return Response.from_result(crd_service.get_notebook_overview(namespace, name))
