from fastapi import APIRouter

from ..services.customer_service import (
    get_customer_segments,
    get_customers,
)


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],
)


@router.get("/segments")
def customer_segments():

    return get_customer_segments()


@router.get("/")
def customers():

    return get_customers()