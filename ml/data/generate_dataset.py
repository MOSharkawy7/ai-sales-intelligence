import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "raw"
    / "sales.csv"
)


random.seed(42)


PRODUCTS = {
    "Laptop": {
        "category": "Electronics",
        "price": 850,
    },
    "Monitor": {
        "category": "Electronics",
        "price": 400,
    },
    "Keyboard": {
        "category": "Electronics",
        "price": 70,
    },
    "Mouse": {
        "category": "Electronics",
        "price": 25,
    },
    "Desk": {
        "category": "Furniture",
        "price": 300,
    },
    "Chair": {
        "category": "Furniture",
        "price": 120,
    },
}


REGIONS = [
    "Cairo",
    "Giza",
    "Alexandria",
    "Mansoura",
]


CUSTOMERS = [
    f"C{number:03d}"
    for number in range(1, 101)
]


def generate_sales_data(
    number_of_orders: int = 5000,
) -> pd.DataFrame:

    start_date = datetime(2023, 1, 1)

    rows = []

    for order_id in range(
        1,
        number_of_orders + 1,
    ):

        random_days = random.randint(
            0,
            729,
        )

        order_date = (
            start_date
            + timedelta(days=random_days)
        )

        product = random.choice(
            list(PRODUCTS.keys())
        )

        product_info = PRODUCTS[product]

        category = product_info["category"]

        base_price = product_info["price"]

        # Add small price variation
        unit_price = round(
            base_price
            * random.uniform(0.9, 1.1),
            2,
        )

        # Weekend purchases are slightly higher
        weekend_multiplier = (
            1.25
            if order_date.weekday() >= 5
            else 1.0
        )

        quantity = max(
            1,
            int(
                random.randint(1, 5)
                * weekend_multiplier
            ),
        )

        discount = round(
            random.choice(
                [
                    0,
                    0,
                    0.05,
                    0.05,
                    0.10,
                    0.15,
                ]
            ),
            2,
        )

        customer_id = random.choice(
            CUSTOMERS
        )

        region = random.choice(
            REGIONS
        )

        rows.append(
            {
                "order_id": order_id,
                "order_date": order_date.date(),
                "customer_id": customer_id,
                "product": product,
                "category": category,
                "region": region,
                "quantity": quantity,
                "unit_price": unit_price,
                "discount": discount,
            }
        )

    return pd.DataFrame(rows)


def main() -> None:

    print("Generating sales dataset...")

    df = generate_sales_data()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        f"Generated {len(df)} sales records."
    )

    print(
        f"Dataset saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()