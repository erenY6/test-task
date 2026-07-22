from fastapi import APIRouter

from backend.app.services.metrics_service import metrics_service


router = APIRouter()


@router.get("/metrics")
async def metrics():

    return metrics_service.get()