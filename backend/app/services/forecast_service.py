from pathlib import Path

import joblib
import pandas as pd
from sqlalchemy.orm import Session

from backend.app.models import Sale


PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "sales_forecasting_model.pkl"
)


FEATURES = [
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


def load_model():
    """
    Load the trained forecasting model.

    The model is loaded with joblib because the training
    pipeline uses sklearn/joblib-compatible serialization.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Forecasting model not found at: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    # Some training pipelines save a dictionary containing
    # the actual model.
    if isinstance(model, dict):
        if "model" in model:
            model = model["model"]
        elif "best_model" in model:
            model = model["best_model"]

    return model


def build_daily_sales(db: Session) -> pd.DataFrame:
    """
    Retrieve sales from PostgreSQL and aggregate them by day.
    """

    sales = (
        db.query(Sale.order_date, Sale.sales)
        .order_by(Sale.order_date)
        .all()
    )

    if not sales:
        raise ValueError("No sales data found in the database.")

    df = pd.DataFrame(
        sales,
        columns=["date", "sales"],
    )

    df["date"] = pd.to_datetime(df["date"])

    daily = (
        df.groupby("date", as_index=False)["sales"]
        .sum()
        .sort_values("date")
        .reset_index(drop=True)
    )

    return daily


def create_features(daily: pd.DataFrame) -> pd.DataFrame:
    """
    Create the same features used during model training.
    """

    daily = daily.copy()

    daily["year"] = daily["date"].dt.year
    daily["month"] = daily["date"].dt.month
    daily["day"] = daily["date"].dt.day
    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["day_of_year"] = daily["date"].dt.dayofyear

    daily["week_of_year"] = (
        daily["date"]
        .dt.isocalendar()
        .week
        .astype(int)
    )

    daily["is_weekend"] = (
        daily["day_of_week"] >= 5
    ).astype(int)

    # Historical features
    daily["sales_lag_1"] = daily["sales"].shift(1)
    daily["sales_lag_7"] = daily["sales"].shift(7)
    daily["sales_lag_30"] = daily["sales"].shift(30)

    # IMPORTANT:
    # Shift first so the current day's sales are not
    # accidentally included in the rolling calculation.
    daily["sales_rolling_7"] = (
        daily["sales"]
        .shift(1)
        .rolling(7)
        .mean()
    )

    daily["sales_rolling_30"] = (
        daily["sales"]
        .shift(1)
        .rolling(30)
        .mean()
    )

    return daily


def get_forecast(
    db: Session,
    days: int = 7,
):
    """
    Generate future sales predictions.

    Uses recursive forecasting:
    each prediction becomes part of the history
    used to generate the next prediction.
    """

    if days < 1:
        raise ValueError("days must be greater than 0.")

    if days > 30:
        raise ValueError("days cannot exceed 30.")

    # --------------------------------------------------
    # Load historical sales
    # --------------------------------------------------

    daily = build_daily_sales(db)

    # --------------------------------------------------
    # Build training-style features
    # --------------------------------------------------

    history = create_features(daily)

    history = history.dropna().reset_index(drop=True)

    if len(history) < 30:
        raise ValueError(
            "Not enough historical data to generate a forecast. "
            "At least 30 days of sales history are required."
        )

    # --------------------------------------------------
    # Load ML model
    # --------------------------------------------------

    model = load_model()

    # --------------------------------------------------
    # Generate recursive predictions
    # --------------------------------------------------

    forecasts = []

    for _ in range(days):

        next_date = (
            history["date"].max()
            + pd.Timedelta(days=1)
        )

        # Build features for the next day
        row = {
            "year": next_date.year,
            "month": next_date.month,
            "day": next_date.day,
            "day_of_week": next_date.dayofweek,
            "day_of_year": next_date.dayofyear,
            "week_of_year": int(
                next_date.isocalendar().week
            ),
            "is_weekend": int(
                next_date.dayofweek >= 5
            ),

            "sales_lag_1": history["sales"].iloc[-1],

            "sales_lag_7": history["sales"].iloc[-7],

            "sales_lag_30": history["sales"].iloc[-30],

            "sales_rolling_7": (
                history["sales"]
                .tail(7)
                .mean()
            ),

            "sales_rolling_30": (
                history["sales"]
                .tail(30)
                .mean()
            ),
        }

        input_data = pd.DataFrame(
            [row],
            columns=FEATURES,
        )

        prediction = model.predict(input_data)[0]

        # Sales cannot be negative
        prediction = max(float(prediction), 0.0)

        forecasts.append(
            {
                "date": next_date.date().isoformat(),
                "predicted_sales": round(
                    prediction,
                    2,
                ),
            }
        )

        # Add prediction to history so that it can
        # be used for the next recursive prediction.
        new_row = pd.DataFrame(
            [
                {
                    "date": next_date,
                    "sales": prediction,
                }
            ]
        )

        history = pd.concat(
            [
                history,
                new_row,
            ],
            ignore_index=True,
        )

    return forecasts