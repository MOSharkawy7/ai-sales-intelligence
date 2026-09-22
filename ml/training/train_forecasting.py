import joblib
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "sales_processed.csv"
)

MODELS_DIR = (
    PROJECT_ROOT
    / "ml"
    / "models"
)


def load_data() -> pd.DataFrame:
    """Load the processed sales data."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(
        DATA_PATH,
        parse_dates=["order_date"],
    )

    return df


def create_daily_dataset(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Aggregate individual orders into daily sales."""

    daily_sales = (
        df.groupby("order_date")
        .agg(
            sales=("sales", "sum"),
            quantity=("quantity", "sum"),
            orders=("order_id", "count"),
            average_discount=("discount", "mean"),
        )
        .reset_index()
    )

    return daily_sales


def create_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """Create time-based forecasting features."""

    df = df.copy()

    df["year"] = df["order_date"].dt.year

    df["month"] = df["order_date"].dt.month

    df["day"] = df["order_date"].dt.day

    df["day_of_week"] = (
        df["order_date"].dt.dayofweek
    )

    df["day_of_year"] = (
        df["order_date"].dt.dayofyear
    )

    df["week_of_year"] = (
        df["order_date"].dt.isocalendar().week
        .astype(int)
    )

    df["is_weekend"] = (
        df["day_of_week"] >= 5
    ).astype(int)

    # Historical sales features

    df["sales_lag_1"] = (
        df["sales"].shift(1)
    )

    df["sales_lag_7"] = (
        df["sales"].shift(7)
    )

    df["sales_lag_30"] = (
        df["sales"].shift(30)
    )

    # Rolling averages

    df["sales_rolling_7"] = (
        df["sales"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    df["sales_rolling_30"] = (
        df["sales"]
        .shift(1)
        .rolling(30)
        .mean()
    )

    return df


def prepare_data(
    df: pd.DataFrame,
):
    """Prepare features and target."""

    df = create_daily_dataset(df)

    df = create_features(df)

    df = df.dropna()

    feature_columns = [
        "year",
        "month",
        "day",
        "day_of_week",
        "day_of_year",
        "week_of_year",
        "is_weekend",
        "quantity",
        "orders",
        "average_discount",
        "sales_lag_1",
        "sales_lag_7",
        "sales_lag_30",
        "sales_rolling_7",
        "sales_rolling_30",
    ]

    target_column = "sales"

    X = df[feature_columns]

    y = df[target_column]

    return X, y, df


def split_data(
    X: pd.DataFrame,
    y: pd.Series,
):
    """Split data chronologically."""

    split_index = int(
        len(X) * 0.8
    )

    X_train = X.iloc[:split_index]

    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]

    y_test = y.iloc[split_index:]

    return (
        X_train,
        X_test,
        y_train,
        y_test,
    )


def evaluate_model(
    model,
    X_test,
    y_test,
    model_name: str,
):
    """Evaluate a regression model."""

    predictions = model.predict(
        X_test
    )

    mae = mean_absolute_error(
        y_test,
        predictions,
    )

    rmse = mean_squared_error(
        y_test,
        predictions,
    ) ** 0.5

    r2 = r2_score(
        y_test,
        predictions,
    )

    print(
        f"\n{model_name}"
    )

    print(
        f"MAE:  {mae:.2f}"
    )

    print(
        f"RMSE: {rmse:.2f}"
    )

    print(
        f"R²:   {r2:.4f}"
    )

    return {
        "model": model,
        "mae": mae,
        "rmse": rmse,
        "r2": r2,
    }


def main() -> None:

    print(
        "Loading processed dataset..."
    )

    df = load_data()

    print(
        f"Loaded {len(df)} rows."
    )

    print(
        "Preparing forecasting dataset..."
    )

    X, y, prepared_df = prepare_data(
        df
    )

    print(
        f"Prepared {len(X)} daily records."
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = split_data(
        X,
        y,
    )

    print(
        f"Training records: {len(X_train)}"
    )

    print(
        f"Testing records: {len(X_test)}"
    )

    # --------------------------------
    # Linear Regression
    # --------------------------------

    linear_model = LinearRegression()

    linear_model.fit(
        X_train,
        y_train,
    )

    linear_result = evaluate_model(
        linear_model,
        X_test,
        y_test,
        "Linear Regression",
    )

    # --------------------------------
    # Random Forest
    # --------------------------------

    random_forest = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1,
    )

    random_forest.fit(
        X_train,
        y_train,
    )

    random_forest_result = evaluate_model(
        random_forest,
        X_test,
        y_test,
        "Random Forest",
    )

    # --------------------------------
    # Select model
    # --------------------------------

    results = [
        linear_result,
        random_forest_result,
    ]

    best_result = min(
        results,
        key=lambda result: result["rmse"],
    )

    best_model = best_result["model"]

    print(
        "\nBest model:"
    )

    print(
        type(best_model).__name__
    )

    # --------------------------------
    # Save model
    # --------------------------------

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    model_path = (
        MODELS_DIR
        / "sales_forecasting_model.pkl"
    )

    joblib.dump(
        best_model,
        model_path,
    )

    print(
        f"\nModel saved to: {model_path}"
    )


if __name__ == "__main__":
    main()