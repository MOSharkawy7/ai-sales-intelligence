import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DATA_PATH = PROJECT_ROOT / "ml" / "data" / "raw" / "sales.csv"
PROCESSED_DATA_DIR = PROJECT_ROOT / "ml" / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DATA_DIR / "sales_processed.csv"


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product",
    "category",
    "region",
    "quantity",
    "unit_price",
    "discount",
]


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw sales dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def validate_columns(df: pd.DataFrame) -> None:
    """Make sure all required columns exist."""

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare the raw sales data."""

    df = df.copy()

    # Convert date column
    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    # Remove rows with invalid dates
    df = df.dropna(subset=["order_date"])

    # Remove duplicate orders
    df = df.drop_duplicates(subset=["order_id"])

    # Remove invalid numerical values
    df = df[df["quantity"] > 0]
    df = df[df["unit_price"] >= 0]

    # Keep discount between 0 and 1
    df["discount"] = df["discount"].clip(0, 1)

    # Fill missing categorical values
    categorical_columns = [
        "customer_id",
        "product",
        "category",
        "region",
    ]

    for column in categorical_columns:
        df[column] = df[column].fillna("Unknown")

    return df


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create features used by analytics and ML models."""

    df = df.copy()

    # Calculate revenue before discount
    df["gross_sales"] = (
        df["quantity"] * df["unit_price"]
    )

    # Calculate discount amount
    df["discount_amount"] = (
        df["gross_sales"] * df["discount"]
    )

    # Calculate final sales amount
    df["sales"] = (
        df["gross_sales"] - df["discount_amount"]
    )

    # Extract useful date features
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["day"] = df["order_date"].dt.day
    df["day_of_week"] = df["order_date"].dt.dayofweek

    # Weekday/weekend indicator
    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    return df


def save_processed_data(df: pd.DataFrame) -> None:
    """Save the processed dataset."""

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )


def main() -> None:
    """Run the complete preprocessing pipeline."""

    print("Loading dataset...")

    df = load_data(RAW_DATA_PATH)

    print(f"Loaded {len(df)} rows.")

    print("Validating dataset...")

    validate_columns(df)

    print("Cleaning dataset...")

    df = clean_data(df)

    print("Creating features...")

    df = create_features(df)

    print("Saving processed dataset...")

    save_processed_data(df)

    print(
        f"Processed dataset saved to: "
        f"{PROCESSED_DATA_PATH}"
    )

    print(f"Final dataset contains {len(df)} rows.")
    print("\nColumns:")
    print(df.columns.tolist())


if __name__ == "__main__":
    main()