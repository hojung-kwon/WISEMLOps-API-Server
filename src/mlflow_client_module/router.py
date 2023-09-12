from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.mlflow_client_module.experiment.router import router as experiment_router
from src.mlflow_client_module.model_version.router import router as model_version_router
from src.mlflow_client_module.registered_model.router import router as registered_model_router
from src.mlflow_client_module.run.router import router as run_router

router = APIRouter(
    prefix="/mlflow",
    responses={404: {"description": "Not found"}},
    default_response_class=JSONResponse,
)

router.include_router(experiment_router)
router.include_router(model_version_router)
router.include_router(registered_model_router)
router.include_router(run_router)
