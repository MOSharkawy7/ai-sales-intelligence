from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.anomaly_service import (
    get_anomalies,
    get_anomaly_summary,
)


router = APIRouter(
    prefix="/api/anomalies",
    tags=["Anomalies"],
)


@router.get("/")
def anomalies(
    db: Session = Depends(get_db),
):
    return get_anomalies(db)


@router.get("/summary")
def anomaly_summary(
    db: Session = Depends(get_db),
):
    return get_anomaly_summary(db)