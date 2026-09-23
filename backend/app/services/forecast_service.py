from pathlib import Path
import pickle

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


def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


def get_forecast(db: Session, days: int = 7):

    sales = (
        db.query(
            Sale.order_date,
            Sale.sales,
        )
        .order_by(Sale.order_date)
        .all()
    )

    df = pd.DataFrame(
        sales,
        columns=["date", "sales"]
    )

    daily = (
        df.groupby("date")["sales"]
        .sum()
        .reset_index()
    )

    daily["date"] = pd.to_datetime(daily["date"])

    daily = daily.sort_values("date")

    daily["year"] = daily["date"].dt.year
    daily["month"] = daily["date"].dt.month
    daily["day"] = daily["date"].dt.day
    daily["day_of_week"] = daily["date"].dt.dayofweek
    daily["day_of_year"] = daily["date"].dt.dayofyear
    daily["week_of_year"] = daily["date"].dt.isocalendar().week.astype(int)
    daily["is_weekend"] = (
        daily["day_of_week"] >= 5
    ).astype(int)

    daily["sales_lag_1"] = daily["sales"].shift(1)
    daily["sales_lag_7"] = daily["sales"].shift(7)
    daily["sales_lag_30"] = daily["sales"].shift(30)

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

    daily = daily.dropna()

    model = load_model()

    features = [
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

    history = daily.copy()

    forecasts = []

    for _ in range(days):

        next_date = (
            history["date"].max()
            + pd.Timedelta(days=1)
        )

        row = {
            "year": next_date.year,
            "month": next_date.month,
            "day": next_date.day,
            "day_of_week": next_date.dayofweek,
            "day_of_year": next_date.dayofyear,
            "week_of_year": next_date.isocalendar().week,
            "is_weekend": int(next_date.dayofweek >= 5),
            "sales_lag_1": history["sales"].iloc[-1],
            "sales_lag_7": history["sales"].iloc[-7],
            "sales_lag_30": history["sales"].iloc[-30],
            "sales_rolling_7": history["sales"].tail(7).mean(),
            "sales_rolling_30": history["sales"].tail(30).mean(),
        }

        prediction = model.predict(
            pd.DataFrame([row])[features]
        )[0]

        prediction = max(float(prediction), 0)

        forecasts.append(
            {
                "date": next_date.date().isoformat(),
                "predicted_sales": round(
                    prediction,
                    2
                ),
            }
        )

        new_row = {
            "date": next_date,
            "sales": prediction,
        }

        history = pd.concat(
            [
                history,
                pd.DataFrame([new_row])
            ],
            ignore_index=True,
        )

    return forecasts