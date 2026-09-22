from ..data_loader import load_sales_data


def get_sales_summary():

    df = load_sales_data()

    total_sales = float(
        df["sales"].sum()
    )

    total_orders = int(
        df["order_id"].nunique()
    )

    total_quantity = int(
        df["quantity"].sum()
    )

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    return {
        "total_sales": round(
            total_sales,
            2
        ),
        "total_orders": total_orders,
        "total_quantity": total_quantity,
        "average_order_value": round(
            average_order_value,
            2
        ),
    }


def get_sales_trends():

    df = load_sales_data()

    trends = (
        df.groupby("order_date")
        .agg(
            sales=("sales", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values("order_date")
    )

    return [
        {
            "date": row["order_date"].strftime(
                "%Y-%m-%d"
            ),
            "sales": round(
                float(row["sales"]),
                2
            ),
            "orders": int(
                row["orders"]
            ),
        }
        for _, row in trends.iterrows()
    ]


def get_sales_by_category():

    df = load_sales_data()

    result = (
        df.groupby("category")
        .agg(
            sales=("sales", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values(
            "sales",
            ascending=False
        )
    )

    return [
        {
            "category": row["category"],
            "sales": round(
                float(row["sales"]),
                2
            ),
            "orders": int(
                row["orders"]
            ),
        }
        for _, row in result.iterrows()
    ]


def get_sales_by_region():

    df = load_sales_data()

    result = (
        df.groupby("region")
        .agg(
            sales=("sales", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
        .sort_values(
            "sales",
            ascending=False
        )
    )

    return [
        {
            "region": row["region"],
            "sales": round(
                float(row["sales"]),
                2
            ),
            "orders": int(
                row["orders"]
            ),
        }
        for _, row in result.iterrows()
    ]