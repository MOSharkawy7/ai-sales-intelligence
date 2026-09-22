from ..data_loader import load_anomalies


def get_anomalies():

    df = load_anomalies()

    return [
        {
            "order_id": row["order_id"],
            "order_date": row["order_date"].strftime(
                "%Y-%m-%d"
            ),
            "customer_id": row["customer_id"],
            "product": row["product"],
            "quantity": int(row["quantity"]),
            "unit_price": round(
                float(row["unit_price"]),
                2
            ),
            "discount": round(
                float(row["discount"]),
                2
            ),
            "sales": round(
                float(row["sales"]),
                2
            ),
            "anomaly_score": round(
                float(row["anomaly_score"]),
                4
            ),
        }
        for _, row in df.iterrows()
    ]


def get_anomaly_summary():

    df = load_anomalies()

    return {
        "total_anomalies": len(df),
        "average_anomaly_sales": round(
            float(df["sales"].mean()),
            2
        ),
        "highest_anomaly_sales": round(
            float(df["sales"].max()),
            2
        ),
    }