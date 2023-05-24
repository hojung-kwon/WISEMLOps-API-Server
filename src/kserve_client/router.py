from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.kserve_client.v1.router import router as v1_router

router = APIRouter(
    prefix="/kserve",
    tags=["kserve"],
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)

router.include_router(v1_router)
