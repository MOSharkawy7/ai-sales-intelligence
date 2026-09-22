import joblib
import pandas as pd

from pathlib import Path
from sklearn.cluster import KMeans
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

SCALER_PATH = MODELS_DIR / "customer_scaler.pkl"
MODEL_PATH = MODELS_DIR / "customer_segmentation_model.pkl"


# --------------------------------------------------
# Load data
# --------------------------------------------------

def load_data():

    df = pd.read_csv(DATA_PATH)

    df["order_date"] = pd.to_datetime(df["order_date"])

    return df


# --------------------------------------------------
# Create customer features
# --------------------------------------------------

def create_customer_features(df):

    customer_features = (
        df.groupby("customer_id")
        .agg(
            total_spend=("sales", "sum"),
            total_orders=("order_id", "nunique"),
            total_quantity=("quantity", "sum"),
            average_order_value=("sales", "mean"),
            average_discount=("discount", "mean"),
            unique_products=("product", "nunique"),
            unique_categories=("category", "nunique"),
        )
        .reset_index()
    )

    return customer_features


# --------------------------------------------------
# Select ML features
# --------------------------------------------------

def prepare_features(customer_features):

    feature_columns = [
        "total_spend",
        "total_orders",
        "total_quantity",
        "average_order_value",
        "average_discount",
        "unique_products",
        "unique_categories",
    ]

    X = customer_features[feature_columns]

    return X, feature_columns


# --------------------------------------------------
# Scale features
# --------------------------------------------------

def scale_features(X):

    scaler = StandardScaler()

    X_scaled = scaler.fit_transform(X)

    return X_scaled, scaler


# --------------------------------------------------
# Train K-Means
# --------------------------------------------------

def train_model(X_scaled):

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    return model


# --------------------------------------------------
# Add segment labels
# --------------------------------------------------

def assign_segments(customer_features, model, X_scaled):

    customer_features = customer_features.copy()

    customer_features["segment"] = model.predict(X_scaled)

    return customer_features


# --------------------------------------------------
# Describe segments
# --------------------------------------------------

def describe_segments(customer_features):

    summary = (
        customer_features
        .groupby("segment")
        .agg(
            customers=("customer_id", "count"),
            average_spend=("total_spend", "mean"),
            average_orders=("total_orders", "mean"),
            average_order_value=("average_order_value", "mean"),
            average_quantity=("total_quantity", "mean"),
            average_discount=("average_discount", "mean"),
        )
        .reset_index()
    )

    return summary


# --------------------------------------------------
# Save results
# --------------------------------------------------

def save_results(customer_features):

    reports_dir = (
        PROJECT_ROOT
        / "ml"
        / "reports"
    )

    reports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        reports_dir
        / "customer_segments.csv"
    )

    customer_features.to_csv(
        output_path,
        index=False
    )

    return output_path


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Loading sales data...")

    df = load_data()

    print(f"Sales records: {len(df)}")

    # Create customer-level dataset
    customer_features = create_customer_features(df)

    print(
        f"Customers analyzed: "
        f"{len(customer_features)}"
    )

    # Prepare features
    X, feature_columns = prepare_features(
        customer_features
    )

    print("\nFeatures used:")

    for feature in feature_columns:
        print(f"- {feature}")

    # Scale
    X_scaled, scaler = scale_features(X)

    # Train model
    model = train_model(X_scaled)

    # Assign clusters
    customer_features = assign_segments(
        customer_features,
        model,
        X_scaled
    )

    # Segment summary
    summary = describe_segments(
        customer_features
    )

    print("\nCustomer Segments")
    print("=" * 70)

    print(summary.to_string(index=False))

    # Save models
    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    joblib.dump(
        model,
        MODEL_PATH
    )

    # Save customer results
    output_path = save_results(
        customer_features
    )

    print("\n" + "=" * 70)

    print(f"Scaler saved to:")
    print(SCALER_PATH)

    print(f"\nSegmentation model saved to:")
    print(MODEL_PATH)

    print(f"\nCustomer segments saved to:")
    print(output_path)

    print("=" * 70)


if __name__ == "__main__":
    main()