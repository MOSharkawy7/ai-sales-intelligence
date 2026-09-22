from fastapi import APIRouter

from ..services.anomaly_service import (
    get_anomalies,
    get_anomaly_summary,
)


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomalies"],
)


@router.get("/")
def anomalies():

    return get_anomalies()


@router.get("/summary")
def anomaly_summary():

    return get_anomaly_summary()