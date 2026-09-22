import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "sales_processed.csv"
)

REPORTS_DIR = (
    PROJECT_ROOT
    / "ml"
    / "reports"
)

CHARTS_DIR = REPORTS_DIR / "charts"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the processed sales dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    return df


def dataset_overview(df: pd.DataFrame) -> None:
    """Display basic information about the dataset."""

    print("\n" + "=" * 60)
    print("DATASET OVERVIEW")
    print("=" * 60)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nData types:")
    print(df.dtypes)


def summary_statistics(df: pd.DataFrame) -> None:
    """Display summary statistics for numerical columns."""

    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)

    numerical_columns = [
        "quantity",
        "unit_price",
        "discount",
        "gross_sales",
        "discount_amount",
        "sales",
    ]

    print(
        df[numerical_columns].describe()
    )


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate total sales for each month."""

    monthly_sales = (
        df.groupby(
            ["year", "month"],
            as_index=False
        )["sales"]
        .sum()
    )

    monthly_sales["period"] = (
        monthly_sales["year"].astype(str)
        + "-"
        + monthly_sales["month"].astype(str).str.zfill(2)
    )

    return monthly_sales


def analyze_products(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales by product."""

    product_sales = (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY PRODUCT")
    print("=" * 60)

    print(product_sales)

    return product_sales


def analyze_categories(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales by category."""

    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY CATEGORY")
    print("=" * 60)

    print(category_sales)

    return category_sales


def analyze_regions(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales by region."""

    region_sales = (
        df.groupby("region")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 60)
    print("SALES BY REGION")
    print("=" * 60)

    print(region_sales)

    return region_sales


def create_monthly_sales_chart(
    monthly_sales: pd.DataFrame
) -> None:
    """Create monthly sales line chart."""

    plt.figure(figsize=(10, 6))

    sns.lineplot(
        data=monthly_sales,
        x="period",
        y="sales",
        marker="o"
    )

    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)

    plt.tight_layout()

    output_path = (
        CHARTS_DIR
        / "monthly_sales.png"
    )

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()

    print(
        f"Saved chart: {output_path}"
    )


def create_product_chart(
    product_sales: pd.DataFrame
) -> None:
    """Create product sales bar chart."""

    plt.figure(figsize=(10, 6))

    product_sales.sort_values().plot(
        kind="barh"
    )

    plt.title("Sales by Product")
    plt.xlabel("Sales")
    plt.ylabel("Product")

    plt.tight_layout()

    output_path = (
        CHARTS_DIR
        / "sales_by_product.png"
    )

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()

    print(
        f"Saved chart: {output_path}"
    )


def create_category_chart(
    category_sales: pd.DataFrame
) -> None:
    """Create category sales chart."""

    plt.figure(figsize=(8, 6))

    category_sales.plot(
        kind="bar"
    )

    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")

    plt.xticks(rotation=0)

    plt.tight_layout()

    output_path = (
        CHARTS_DIR
        / "sales_by_category.png"
    )

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()

    print(
        f"Saved chart: {output_path}"
    )


def create_region_chart(
    region_sales: pd.DataFrame
) -> None:
    """Create region sales chart."""

    plt.figure(figsize=(8, 6))

    region_sales.plot(
        kind="bar"
    )

    plt.title("Sales by Region")
    plt.xlabel("Region")
    plt.ylabel("Sales")

    plt.xticks(rotation=0)

    plt.tight_layout()

    output_path = (
        CHARTS_DIR
        / "sales_by_region.png"
    )

    plt.savefig(
        output_path,
        dpi=150
    )

    plt.close()

    print(
        f"Saved chart: {output_path}"
    )


def generate_insights(
    df: pd.DataFrame,
    product_sales: pd.DataFrame,
    category_sales: pd.DataFrame,
    region_sales: pd.DataFrame,
) -> None:
    """Print high-level business insights."""

    total_sales = df["sales"].sum()

    total_orders = df["order_id"].nunique()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    best_product = product_sales.index[0]
    best_product_sales = product_sales.iloc[0]

    best_category = category_sales.index[0]

    best_region = region_sales.index[0]

    print("\n" + "=" * 60)
    print("BUSINESS INSIGHTS")
    print("=" * 60)

    print(
        f"Total sales: ${total_sales:,.2f}"
    )

    print(
        f"Total orders: {total_orders}"
    )

    print(
        f"Average order value: "
        f"${average_order_value:,.2f}"
    )

    print(
        f"Best-selling product: "
        f"{best_product} "
        f"(${best_product_sales:,.2f})"
    )

    print(
        f"Best category: {best_category}"
    )

    print(
        f"Best-performing region: "
        f"{best_region}"
    )


def main() -> None:
    """Run the complete EDA process."""

    print("Loading processed dataset...")

    df = load_data(
        PROCESSED_DATA_PATH
    )

    CHARTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    dataset_overview(df)

    summary_statistics(df)

    monthly_sales = sales_by_month(df)

    product_sales = analyze_products(df)

    category_sales = analyze_categories(df)

    region_sales = analyze_regions(df)

    create_monthly_sales_chart(
        monthly_sales
    )

    create_product_chart(
        product_sales
    )

    create_category_chart(
        category_sales
    )

    create_region_chart(
        region_sales
    )

    generate_insights(
        df,
        product_sales,
        category_sales,
        region_sales,
    )

    print("\nEDA completed successfully.")


if __name__ == "__main__":
    main()