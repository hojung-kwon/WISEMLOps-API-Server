import logging
import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette import status
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from uvicorn import Config, Server

from src import app_config
from src.common_module import router as common_router
from src.exceptions import MLOpsAPIException
from src.kfp_module import router as kfp_router
from src.kfp_module.exceptions import KFPException
from src.kserve_module import router as kserve_router
from src.kserve_module.exceptions import KServeException
from src.kubernetes_module.cluster import router as cluster_router
from src.kubernetes_module.crds import router as crd_router
from src.kubernetes_module.exceptions import KubernetesException
from src.minio_module import router as minio_router
from src.minio_module.exceptions import MinIOException
from src.mlflow_module import router as mlflow_router
from src.mlflow_module.exceptions import MlflowException
from src.version import get_version_info, write_version_py
from src.workflow_generator_module import router as gen_pipeline_router
from src.workflow_generator_module.exceptions import WorkflowGeneratorException
from src.workflow_pipeline_module import router as pipeline_router
from src.workflow_pipeline_module.exceptions import WorkflowPipelineException

LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "DEBUG"))
JSON_LOGS = True if os.environ.get("JSON_LOGS", "0") == "1" else False


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # remove every other logger's handlers
    # and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # configure loguru
    logger.configure(handlers=[{"sink": sys.stdout, "serialize": JSON_LOGS}])


def check_env_exist() -> None:
    """
    설정이 필요한 환경변수가 세팅되어있는지 체크
    TODO: 필요한 환경변수가 없을 경우, 프로그램 종료

    Returns: None

    """
    env_list = ['CHECK_ENV']  # TODO: 확인할 환경변수 설정
    for env in env_list:
        if env not in os.environ.keys():
            logging.warning(f"set {repr(env)} environment variable.")


@asynccontextmanager
async def lifespan(lifespan_app: FastAPI):
    # startup event
    logging.info("Start Python FastAPI Template")
    # logging.info("Check env exist ...")
    # check_env_exist()
    write_version_py()
    yield
    # shutdown event
    logging.info("Shut down Python FastAPI Template")


app = FastAPI(
    lifespan=lifespan,
    title="Python FastAPI Template",
    description="ML Ops Python FastAPI Template",
    version="0.0.1",
    # dependencies=[Depends(get_query_token)]
)

app.include_router(cluster_router.router)
app.include_router(crd_router.router)
app.include_router(minio_router.router)
app.include_router(mlflow_router.router)
app.include_router(kserve_router.router)
app.include_router(kfp_router.router)
app.include_router(gen_pipeline_router.router)
app.include_router(pipeline_router.router)
app.include_router(common_router.router)


@app.exception_handler(ValueError)
async def http_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(app_config.SERVICE_CODE) + str(status.HTTP_400_BAD_REQUEST)),
            "message": f"Invalid Request: Value Error.",
            "result": exc.args
        }
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(app_config.SERVICE_CODE) + str(exc.status_code)),
            "message": f"{exc.detail}",
            "result": {
                "headers": exc.headers
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(f"{app_config.SERVICE_CODE}{status.HTTP_422_UNPROCESSABLE_ENTITY}"),
            "message": f"Invalid Request: {exc.errors()[0]['msg']} (type: {exc.errors()[0]['type']}), "
                       f"Check {(exc.errors()[0]['loc'])}",
            "result": {
                "body": exc.body
            }
        }
    )


@app.exception_handler(ValidationError)
async def request_validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=200,
        content={
            "code": int(str(app_config.SERVICE_CODE) + str(status.HTTP_422_UNPROCESSABLE_ENTITY)),
            "message": "pydantic model ValidationError 발생",
            "result": {
                "body": exc.errors()
            }
        }
    )


@app.exception_handler(MLOpsAPIException)
async def mlops_api_exception_handler(request: Request, exc: MLOpsAPIException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(WorkflowGeneratorException)
async def workflow_generator_exception_handler(request: Request, exc: WorkflowGeneratorException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(WorkflowPipelineException)
async def workflow_pipeline_exception_handler(request: Request, exc: WorkflowPipelineException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(MinIOException)
async def minio_exception_handler(request: Request, exc: MinIOException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(KFPException)
async def kfp_exception_handler(request: Request, exc: KFPException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(KubernetesException)
async def kubernetes_exception_handler(request: Request, exc: KubernetesException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(KServeException)
async def kserve_exception_handler(request: Request, exc: KServeException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.exception_handler(MlflowException)
async def mlflow_exception_handler(request: Request, exc: MlflowException):
    return JSONResponse(status_code=200,
                        content={"code": exc.code, "message": exc.message, "result": exc.result})


@app.get("/")
async def root():
    return {"title": app.title, "description": app.description, "version": app.version, "docs_url": app.docs_url}


@app.get("/health")
async def health():
    return {"status": "UP"}


@app.get("/info")
async def info():
    VERSION, GIT_REVISION, GIT_SHORT_REVISION, GIT_BRANCH, BUILD_DATE = get_version_info()
    return {
        "version": VERSION,
        "git_branch": GIT_BRANCH,
        "git_revision": GIT_REVISION,
        "git_short_revision": GIT_SHORT_REVISION,
        "build_date": BUILD_DATE
    }


origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    server = Server(
        Config(
            "main:app",
            host="0.0.0.0",
            port=8000,
            log_level=LOG_LEVEL,
        ),
    )

    # setup logging last, to make sure no library overwrites it
    # (they shouldn't, but it happens)
    setup_logging()
    # uvicorn.run(app=app, host="0.0.0.0", port=8000, log_level=LOG_LEVEL)
    server.run()
