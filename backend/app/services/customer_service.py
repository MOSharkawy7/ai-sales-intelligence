from ..data_loader import load_customer_segments


def get_customer_segments():

    df = load_customer_segments()

    summary = (
        df.groupby("segment")
        .agg(
            customers=("customer_id", "count"),
            average_spend=("total_spend", "mean"),
            average_orders=("total_orders", "mean"),
            average_order_value=(
                "average_order_value",
                "mean",
            ),
        )
        .reset_index()
    )

    return [
        {
            "segment": int(row["segment"]),
            "customers": int(row["customers"]),
            "average_spend": round(
                float(row["average_spend"]),
                2
            ),
            "average_orders": round(
                float(row["average_orders"]),
                2
            ),
            "average_order_value": round(
                float(row["average_order_value"]),
                2
            ),
        }
        for _, row in summary.iterrows()
    ]


def get_customers():

    df = load_customer_segments()

    return [
        {
            "customer_id": row["customer_id"],
            "segment": int(row["segment"]),
            "total_spend": round(
                float(row["total_spend"]),
                2
            ),
            "total_orders": int(
                row["total_orders"]
            ),
            "average_order_value": round(
                float(row["average_order_value"]),
                2
            ),
        }
        for _, row in df.iterrows()
    ]