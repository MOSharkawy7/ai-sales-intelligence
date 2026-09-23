from sqlalchemy.orm import Session

from backend.app.models import SalesAnomaly


def get_anomalies(db: Session):
    anomalies = (
        db.query(SalesAnomaly)
        .order_by(SalesAnomaly.anomaly_score.asc())
        .all()
    )

    return [
        {
            "order_id": anomaly.order_id,
            "order_date": anomaly.order_date,
            "customer_id": anomaly.customer_id,
            "product": anomaly.product,
            "quantity": anomaly.quantity,
            "unit_price": float(anomaly.unit_price),
            "discount": float(anomaly.discount),
            "sales": float(anomaly.sales),
            "anomaly_score": float(anomaly.anomaly_score),
        }
        for anomaly in anomalies
    ]


def get_anomaly_summary(db: Session):
    total_anomalies = (
        db.query(SalesAnomaly)
        .count()
    )

    return {
        "total_anomalies": total_anomalies,
    }