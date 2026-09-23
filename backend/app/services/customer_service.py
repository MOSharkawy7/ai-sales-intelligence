from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models import CustomerSegment


def get_customers(db: Session):
    customers = (
        db.query(CustomerSegment)
        .order_by(CustomerSegment.total_spend.desc())
        .all()
    )

    return [
        {
            "customer_id": customer.customer_id,
            "total_spend": float(customer.total_spend),
            "total_orders": customer.total_orders,
            "total_quantity": customer.total_quantity,
            "average_order_value": float(customer.average_order_value),
            "average_discount": float(customer.average_discount),
            "unique_products": customer.unique_products,
            "unique_categories": customer.unique_categories,
            "segment": customer.segment,
        }
        for customer in customers
    ]


def get_customer_segments(db: Session):
    results = (
        db.query(
            CustomerSegment.segment,
            func.count(CustomerSegment.id).label("customer_count"),
            func.sum(CustomerSegment.total_spend).label("total_spend"),
            func.avg(CustomerSegment.average_order_value).label(
                "average_order_value"
            ),
        )
        .group_by(CustomerSegment.segment)
        .order_by(CustomerSegment.segment)
        .all()
    )

    return [
        {
            "segment": segment,
            "customer_count": customer_count,
            "total_spend": round(float(total_spend), 2),
            "average_order_value": round(
                float(average_order_value), 2
            ),
        }
        for (
            segment,
            customer_count,
            total_spend,
            average_order_value,
        ) in results
    ]