from fastapi import APIRouter

from ..services.sales_service import (
    get_sales_summary,
    get_sales_trends,
    get_sales_by_category,
    get_sales_by_region,
)


router = APIRouter(
    prefix="/api/sales",
    tags=["Sales"],
)


@router.get("/summary")
def sales_summary():

    return get_sales_summary()


@router.get("/trends")
def sales_trends():

    return get_sales_trends()


@router.get("/categories")
def sales_categories():

    return get_sales_by_category()


@router.get("/regions")
def sales_regions():

    return get_sales_by_region()