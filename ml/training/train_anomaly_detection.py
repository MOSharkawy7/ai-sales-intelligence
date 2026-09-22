import joblib
import pandas as pd

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "ml"
    / "data"
    / "processed"
    / "sales_processed.csv"
)

MODELS_DIR = PROJECT_ROOT / "ml" / "models"

MODEL_PATH = (
    MODELS_DIR
    / "sales_anomaly_model.pkl"
)

SCALER_PATH = (
    MODELS_DIR
    / "anomaly_scaler.pkl"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "reports"
    / "sales_anomalies.csv"
)


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():

    df = pd.read_csv(DATA_PATH)

    df["order_date"] = pd.to_datetime(
        df["order_date"]
    )

    return df


# --------------------------------------------------
# Create anomaly features
# --------------------------------------------------

def create_features(df):

    features = df[
        [
            "quantity",
            "unit_price",
            "discount",
            "sales"
        ]
    ].copy()

    return features


# --------------------------------------------------
# Scale features
# --------------------------------------------------

def scale_features(X):

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


# --------------------------------------------------
# Train Isolation Forest
# --------------------------------------------------

def train_model(X_scaled):

    model = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_scaled)

    return model


# --------------------------------------------------
# Detect anomalies
# --------------------------------------------------

def detect_anomalies(
    df,
    model,
    X_scaled
):

    df = df.copy()

    # Isolation Forest:
    #  1  = normal
    # -1  = anomaly

    df["anomaly_label"] = model.predict(
        X_scaled
    )

    # Convert to easier values:
    # 0 = normal
    # 1 = anomaly

    df["is_anomaly"] = (
        df["anomaly_label"] == -1
    ).astype(int)

    # Anomaly score
    df["anomaly_score"] = (
        model.decision_function(X_scaled)
    )

    return df


# --------------------------------------------------
# Save results
# --------------------------------------------------

def save_results(df):

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    anomalies = df[
        df["is_anomaly"] == 1
    ].copy()

    anomalies = anomalies.sort_values(
        "anomaly_score"
    )

    anomalies.to_csv(
        REPORT_PATH,
        index=False
    )

    return anomalies


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Loading sales data...")

    df = load_data()

    print(
        f"Transactions analyzed: "
        f"{len(df)}"
    )

    # Create features
    X = create_features(df)

    print("\nFeatures used:")

    for column in X.columns:
        print(f"- {column}")

    # Scale
    X_scaled, scaler = scale_features(X)

    # Train model
    model = train_model(X_scaled)

    # Detect anomalies
    result = detect_anomalies(
        df,
        model,
        X_scaled
    )

    # Save models
    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    # Save anomaly report
    anomalies = save_results(result)

    # Statistics
    anomaly_count = len(anomalies)

    anomaly_percentage = (
        anomaly_count / len(result)
    ) * 100

    print("\n" + "=" * 60)

    print(
        f"Anomalies detected: "
        f"{anomaly_count}"
    )

    print(
        f"Anomaly percentage: "
        f"{anomaly_percentage:.2f}%"
    )

    print("\nTop anomalies:")

    columns_to_show = [
        "order_id",
        "order_date",
        "customer_id",
        "product",
        "quantity",
        "unit_price",
        "discount",
        "sales",
        "anomaly_score"
    ]

    print(
        anomalies[
            columns_to_show
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nModel saved to:")
    print(MODEL_PATH)

    print("\nScaler saved to:")
    print(SCALER_PATH)

    print("\nAnomaly report saved to:")
    print(REPORT_PATH)

    print("=" * 60)


if __name__ == "__main__":
    main()