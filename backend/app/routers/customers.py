from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.services.customer_service import (
    get_customers,
    get_customer_segments,
)


router = APIRouter(
    prefix="/api/customers",
    tags=["Customers"],
)


@router.get("/")
def customers(
    db: Session = Depends(get_db),
):
    return get_customers(db)


@router.get("/segments")
def customer_segments(
    db: Session = Depends(get_db),
):
    return get_customer_segments(db)