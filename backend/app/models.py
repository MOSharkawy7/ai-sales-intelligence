from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    String,
)


from .database import Base


class Sale(Base):

    __tablename__ = "sales"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        String,
        unique=True,
        index=True,
    )

    order_date = Column(
        Date,
        index=True,
    )

    customer_id = Column(
        String,
        index=True,
    )

    product = Column(
        String,
    )

    category = Column(
        String,
    )

    region = Column(
        String,
    )

    quantity = Column(
        Integer,
    )

    unit_price = Column(
        Float,
    )

    discount = Column(
        Float,
    )

    sales = Column(
        Float,
    )


class CustomerSegment(Base):

    __tablename__ = "customer_segments"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    customer_id = Column(
        String,
        unique=True,
        index=True,
    )

    total_spend = Column(
        Float,
    )

    total_orders = Column(
        Integer,
    )

    total_quantity = Column(
        Integer,
    )

    average_order_value = Column(
        Float,
    )

    average_discount = Column(
        Float,
    )

    unique_products = Column(
        Integer,
    )

    unique_categories = Column(
        Integer,
    )

    segment = Column(
        Integer,
    )


class SalesAnomaly(Base):

    __tablename__ = "sales_anomalies"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    order_id = Column(
        String,
        unique=True,
        index=True,
    )

    order_date = Column(
        Date,
        index=True,
    )

    customer_id = Column(
        String,
    )

    product = Column(
        String,
    )

    quantity = Column(
        Integer,
    )

    unit_price = Column(
        Float,
    )

    discount = Column(
        Float,
    )

    sales = Column(
        Float,
    )

    anomaly_score = Column(
        Float,
    )