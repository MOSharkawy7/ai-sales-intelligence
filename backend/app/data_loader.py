import pandas as pd

from functools import lru_cache

from .config import (
    PROCESSED_DATA_PATH,
    CUSTOMER_SEGMENTS_PATH,
    ANOMALIES_PATH,
)


@lru_cache
def load_sales_data():

    df = pd.read_csv(
        PROCESSED_DATA_PATH
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    return df


@lru_cache
def load_customer_segments():

    df = pd.read_csv(
        CUSTOMER_SEGMENTS_PATH
    )

    return df


@lru_cache
def load_anomalies():

    df = pd.read_csv(
        ANOMALIES_PATH
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    return df