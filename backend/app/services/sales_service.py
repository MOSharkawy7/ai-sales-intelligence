from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models import Sale


def get_sales_summary(db: Session):
    total_sales = db.query(
        func.sum(Sale.sales)
    ).scalar() or 0

    total_orders = db.query(
        func.count(Sale.id)
    ).scalar() or 0

    total_quantity = db.query(
        func.sum(Sale.quantity)
    ).scalar() or 0

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_sales": round(float(total_sales), 2),
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "average_order_value": round(
            float(average_order_value),
            2
        ),
    }


def get_sales_trends(db: Session):
    results = (
        db.query(
            Sale.order_date,
            func.sum(Sale.sales).label("sales"),
        )
        .group_by(Sale.order_date)
        .order_by(Sale.order_date)
        .all()
    )

    return [
        {
            "date": order_date,
            "sales": round(float(sales), 2),
        }
        for order_date, sales in results
    ]


def get_sales_by_category(db: Session):
    results = (
        db.query(
            Sale.category,
            func.sum(Sale.sales).label("sales"),
        )
        .group_by(Sale.category)
        .order_by(func.sum(Sale.sales).desc())
        .all()
    )

    return [
        {
            "category": category,
            "sales": round(float(sales), 2),
        }
        for category, sales in results
    ]


def get_sales_by_region(db: Session):
    results = (
        db.query(
            Sale.region,
            func.sum(Sale.sales).label("sales"),
        )
        .group_by(Sale.region)
        .order_by(func.sum(Sale.sales).desc())
        .all()
    )

    return [
        {
            "region": region,
            "sales": round(float(sales), 2),
        }
        for region, sales in results
    ]