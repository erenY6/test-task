from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        logger.warning(f"Validation error: {exc.errors()}")

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation error",
                "errors": exc.errors()
            }
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        logger.exception(exc)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error"
            }
        )