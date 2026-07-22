from fastapi import FastAPI

from app.core.logger import logger
import time
import logging
from fastapi import Request

from app.api import health
from app.api.contact import router as contact_router
from app.api.metrics import router as metrics_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

logger.info("Application started")
logger = logging.getLogger("portfolio-api")


@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):

    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} "
        f"{request.url.path} "
        f"{response.status_code} "
        f"{process_time:.3f}s"
    )

    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(
    contact_router,
    prefix="/api",
    tags=["Contact"]
)

app.include_router(
    health.router,
    prefix="/api"
)

app.include_router(
    metrics_router,
    prefix="/api"
)

@app.get("/")
async def root():
    return {
        "message": settings.APP_NAME
    }