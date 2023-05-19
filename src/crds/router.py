from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.models import APIResponseModel
from src.crds import crd_service

router = APIRouter(
    prefix="/crds",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)


@router.get("/{namespaces/{namespace}/notebooks", tags=["notebook"], response_model=APIResponseModel)
async def get_notebooks(namespace: str = 'default'):
    return crd_service.get_notebooks(namespace)

