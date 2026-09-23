import sys

from pathlib import Path

import pandas as pd

from sqlalchemy.orm import Session


# Allow running this file directly
PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)


from backend.app.database import (
    Base,
    SessionLocal,
    engine,
)

from backend.app.models import (
    Sale,
    CustomerSegment,
    SalesAnomaly,
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

SALES_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "sales_processed.csv"
)

SEGMENTS_PATH = (
    PROJECT_ROOT
    / "ml"
    / "reports"
    / "customer_segments.csv"
)

ANOMALIES_PATH = (
    PROJECT_ROOT
    / "ml"
    / "reports"
    / "sales_anomalies.csv"
)


# --------------------------------------------------
# Create tables
# --------------------------------------------------

def create_tables():

    Base.metadata.create_all(
        bind=engine
    )

    print("Database tables created.")


# --------------------------------------------------
# Seed sales
# --------------------------------------------------

def seed_sales(db: Session):

    print("Loading sales data...")

    df = pd.read_csv(
        SALES_PATH
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    records = []

    for _, row in df.iterrows():

        record = Sale(
            order_id=str(
                row["order_id"]
            ),
            order_date=row["order_date"].date(),
            customer_id=str(
                row["customer_id"]
            ),
            product=str(
                row["product"]
            ),
            category=str(
                row["category"]
            ),
            region=str(
                row["region"]
            ),
            quantity=int(
                row["quantity"]
            ),
            unit_price=float(
                row["unit_price"]
            ),
            discount=float(
                row["discount"]
            ),
            sales=float(
                row["sales"]
            ),
        )

        records.append(record)

    db.bulk_save_objects(
        records
    )

    db.commit()

    print(
        f"Inserted {len(records)} sales records."
    )


# --------------------------------------------------
# Seed customer segments
# --------------------------------------------------

def seed_customer_segments(db: Session):

    print(
        "Loading customer segments..."
    )

    df = pd.read_csv(
        SEGMENTS_PATH
    )

    records = []

    for _, row in df.iterrows():

        record = CustomerSegment(
            customer_id=str(
                row["customer_id"]
            ),
            total_spend=float(
                row["total_spend"]
            ),
            total_orders=int(
                row["total_orders"]
            ),
            total_quantity=int(
                row["total_quantity"]
            ),
            average_order_value=float(
                row["average_order_value"]
            ),
            average_discount=float(
                row["average_discount"]
            ),
            unique_products=int(
                row["unique_products"]
            ),
            unique_categories=int(
                row["unique_categories"]
            ),
            segment=int(
                row["segment"]
            ),
        )

        records.append(record)

    db.bulk_save_objects(
        records
    )

    db.commit()

    print(
        f"Inserted {len(records)} customer segments."
    )


# --------------------------------------------------
# Seed anomalies
# --------------------------------------------------

def seed_anomalies(db: Session):

    print(
        "Loading anomaly data..."
    )

    df = pd.read_csv(
        ANOMALIES_PATH
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    records = []

    for _, row in df.iterrows():

        record = SalesAnomaly(
            order_id=str(
                row["order_id"]
            ),
            order_date=row["order_date"].date(),
            customer_id=str(
                row["customer_id"]
            ),
            product=str(
                row["product"]
            ),
            quantity=int(
                row["quantity"]
            ),
            unit_price=float(
                row["unit_price"]
            ),
            discount=float(
                row["discount"]
            ),
            sales=float(
                row["sales"]
            ),
            anomaly_score=float(
                row["anomaly_score"]
            ),
        )

        records.append(record)

    db.bulk_save_objects(
        records
    )

    db.commit()

    print(
        f"Inserted {len(records)} anomalies."
    )


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    create_tables()

    db = SessionLocal()

    try:

        seed_sales(db)

        seed_customer_segments(db)

        seed_anomalies(db)

    finally:

        db.close()

    print(
        "\nDatabase seeding completed."
    )


if __name__ == "__main__":
    main()