import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "ml" / "data" / "processed" / "sales_processed.csv"
MODELS_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_PATH = MODELS_DIR / "sales_forecasting_model.pkl"


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():
    df = pd.read_csv(DATA_PATH)

    df["order_date"] = pd.to_datetime(df["order_date"])

    return df


# --------------------------------------------------
# Create daily sales dataset
# --------------------------------------------------

def create_daily_dataset(df):
    daily = (
        df.groupby("order_date")
        .agg(
            sales=("sales", "sum"),
            quantity=("quantity", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    daily = daily.sort_values("order_date")

    return daily


# --------------------------------------------------
# Create forecasting features
# --------------------------------------------------

def create_features(df):

    df = df.copy()

    # Calendar features
    df["year"] = df["order_date"].dt.year
    df["month"] = df["order_date"].dt.month
    df["day"] = df["order_date"].dt.day
    df["day_of_week"] = df["order_date"].dt.dayofweek
    df["day_of_year"] = df["order_date"].dt.dayofyear
    df["week_of_year"] = df["order_date"].dt.isocalendar().week.astype(int)
    df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

    # Historical sales features
    df["sales_lag_1"] = df["sales"].shift(1)

    df["sales_lag_7"] = df["sales"].shift(7)

    df["sales_lag_30"] = df["sales"].shift(30)

    # Rolling averages based ONLY on previous days
    df["sales_rolling_7"] = (
        df["sales"]
        .shift(1)
        .rolling(window=7)
        .mean()
    )

    df["sales_rolling_30"] = (
        df["sales"]
        .shift(1)
        .rolling(window=30)
        .mean()
    )

    return df


# --------------------------------------------------
# Prepare training data
# --------------------------------------------------

def prepare_data(df):

    df = create_features(df)

    feature_columns = [
        "year",
        "month",
        "day",
        "day_of_week",
        "day_of_year",
        "week_of_year",
        "is_weekend",
        "sales_lag_1",
        "sales_lag_7",
        "sales_lag_30",
        "sales_rolling_7",
        "sales_rolling_30",
    ]

    df = df.dropna()

    X = df[feature_columns]

    y = df["sales"]

    return X, y, df


# --------------------------------------------------
# Chronological train/test split
# --------------------------------------------------

def split_data(X, y):

    split_index = int(len(X) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]

    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    return X_train, X_test, y_train, y_test


# --------------------------------------------------
# Evaluate model
# --------------------------------------------------

def evaluate_model(model, X_test, y_test, model_name):

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = mean_squared_error(
        y_test,
        predictions
    ) ** 0.5

    r2 = r2_score(y_test, predictions)

    print(f"\n{model_name}")
    print("-" * 40)

    print(f"MAE : {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R²  : {r2:.4f}")

    return rmse


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Loading sales data...")

    df = load_data()

    print(f"Raw records: {len(df)}")

    # Create daily dataset
    daily_df = create_daily_dataset(df)

    print(f"Daily records: {len(daily_df)}")

    # Create features
    X, y, prepared_df = prepare_data(daily_df)

    print(f"Training records: {len(X)}")

    # Train/test split
    X_train, X_test, y_train, y_test = split_data(X, y)

    print(f"Training set: {len(X_train)}")
    print(f"Testing set : {len(X_test)}")

    # --------------------------------------------------
    # Linear Regression
    # --------------------------------------------------

    linear_model = LinearRegression()

    linear_model.fit(
        X_train,
        y_train
    )

    linear_rmse = evaluate_model(
        linear_model,
        X_test,
        y_test,
        "Linear Regression"
    )

    # --------------------------------------------------
    # Random Forest
    # --------------------------------------------------

    random_forest = RandomForestRegressor(
        n_estimators=200,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    random_forest.fit(
        X_train,
        y_train
    )

    rf_rmse = evaluate_model(
        random_forest,
        X_test,
        y_test,
        "Random Forest"
    )

    # --------------------------------------------------
    # Select best model
    # --------------------------------------------------

    if rf_rmse < linear_rmse:

        best_model = random_forest
        best_model_name = "Random Forest"

    else:

        best_model = linear_model
        best_model_name = "Linear Regression"

    # --------------------------------------------------
    # Save model
    # --------------------------------------------------

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    print("\n" + "=" * 50)
    print(f"Best model: {best_model_name}")
    print(f"Model saved to: {MODEL_PATH}")
    print("=" * 50)


if __name__ == "__main__":
    main()