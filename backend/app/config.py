from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "sales_processed.csv"
)

CUSTOMER_SEGMENTS_PATH = (
    PROJECT_ROOT
    / "ml"
    / "reports"
    / "customer_segments.csv"
)

ANOMALIES_PATH = (
    PROJECT_ROOT
    / "ml"
    / "reports"
    / "sales_anomalies.csv"
)

FORECAST_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "models"
    / "sales_forecasting_model.pkl"
)