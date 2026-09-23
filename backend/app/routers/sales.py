from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Query

from backend.app.services.forecast_service import get_forecast

from backend.app.database import get_db
from backend.app.services.sales_service import (
    get_sales_summary,
    get_sales_trends,
    get_sales_by_category,
    get_sales_by_region,
)


router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"],
)


@router.get("/forecast")
def sales_forecast(
    days: int = Query(
        default=7,
        ge=1,
        le=30
    ),
    db: Session = Depends(get_db),
):
    return get_forecast(db, days)

@router.get("/summary")
def sales_summary(
    db: Session = Depends(get_db),
):
    return get_sales_summary(db)


@router.get("/trends")
def sales_trends(
    db: Session = Depends(get_db),
):
    return get_sales_trends(db)


@router.get("/categories")
def sales_categories(
    db: Session = Depends(get_db),
):
    return get_sales_by_category(db)


@router.get("/regions")
def sales_regions(
    db: Session = Depends(get_db),
):
    return get_sales_by_region(db)