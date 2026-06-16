"""
pipeline.py — Data Ingestion & Feature Engineering Pipeline
=============================================================
Handles raw data loading, cleaning, imputation, and the creation
of derived features used throughout the EDA project.

Usage:
    python -m src.ingestion.pipeline
"""

from pathlib import Path
import pandas as pd
import numpy as np

ROOT       = Path(__file__).resolve().parents[2]
RAW_PATH   = ROOT / "data" / "01_raw" / "ecommerce_customers_raw.csv"
CLEAN_PATH = ROOT / "data" / "02_processed" / "ecommerce_customers_clean.csv"
FEAT_PATH  = ROOT / "data" / "03_features" / "ecommerce_customers_features.csv"


# ── 1. Load ────────────────────────────────────────────────────────────────

def load_raw() -> pd.DataFrame:
    """Load the raw, unprocessed dataset."""
    df = pd.read_csv(RAW_PATH)
    print(f"[ingest] Loaded raw data → {df.shape[0]:,} rows × {df.shape[1]} cols")
    return df


# ── 2. Clean ───────────────────────────────────────────────────────────────

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Contextual imputation + de-duplication.
    Missing satisfaction scores are filled with the segment median;
    missing email open rates with the channel median.
    """
    df = df.copy()

    df["satisfaction_score"] = (
        df.groupby("customer_segment")["satisfaction_score"]
        .transform(lambda x: x.fillna(x.median()))
    )
    df["email_open_rate"] = (
        df.groupby("acquisition_channel")["email_open_rate"]
        .transform(lambda x: x.fillna(x.median()))
    )
    df["avg_session_duration_sec"] = df["avg_session_duration_sec"].fillna(
        df["avg_session_duration_sec"].median()
    )
    df["cart_abandonment_rate"] = df["cart_abandonment_rate"].fillna(
        df["cart_abandonment_rate"].median()
    )

    before = len(df)
    df.drop_duplicates(inplace=True)
    if len(df) < before:
        print(f"[clean] Removed {before - len(df)} duplicate rows")

    return df


# ── 3. Feature Engineering ────────────────────────────────────────────────

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive analytical features: CLV, engagement, RFM, tiers, cohorts."""
    df = df.copy()

    df["clv_score"] = (
        df["total_spend"] * (df["satisfaction_score"] / 5) * (1 - df["return_rate"])
    ).round(2)

    df["engagement_score"] = (
        df["email_open_rate"] * 0.25
        + (df["num_orders"] / 60) * 0.25
        + (df["referral_count"] / 15) * 0.15
        + (df["reviews_submitted"] / 20) * 0.15
        + (df["pages_per_session"] / 40) * 0.10
        + (df["newsletter_subscriber"] * 0.10)
    ).round(4)

    df["spend_to_income_ratio"] = (df["total_spend"] / df["annual_income"]).round(4)
    df["recency_score"] = (1 - df["days_since_last_order"] / 400).clip(0, 1).round(4)

    df["digital_maturity_score"] = (
        df["mobile_app_user"] * 0.4
        + (df["pages_per_session"] / 40) * 0.3
        + df["newsletter_subscriber"] * 0.3
    ).round(4)

    df["rfm_score"] = (
        df["recency_score"] * 0.35
        + (df["num_orders"] / 60) * 0.35
        + (df["total_spend"] / 12000) * 0.30
    ).round(4)

    df["value_tier"] = pd.qcut(
        df["clv_score"], q=5, labels=["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
    )
    df["income_bracket"] = pd.qcut(
        df["annual_income"], q=4, labels=["Low", "Mid", "High", "Premium"]
    )
    df["age_group"] = pd.cut(
        df["age"], bins=[17, 25, 35, 45, 55, 72],
        labels=["Gen Z (18-25)", "Millennial (26-35)", "Gen X (36-45)",
                "Boomer (46-55)", "Senior (56+)"]
    )
    df["tenure_tier"] = pd.cut(
        df["account_age_days"], bins=[0, 90, 365, 730, 1500, 2500],
        labels=["<3mo", "3-12mo", "1-2yr", "2-4yr", "4yr+"]
    )
    df["session_depth"] = pd.cut(
        df["avg_session_duration_sec"], bins=[0, 120, 300, 600, 1800],
        labels=["Bouncer", "Browser", "Explorer", "Power User"]
    )

    return df


# ── 4. Orchestration ──────────────────────────────────────────────────────

def run_pipeline() -> pd.DataFrame:
    """Run the full ingest → clean → engineer pipeline and persist outputs."""
    raw = load_raw()
    cleaned = clean(raw)
    featured = engineer_features(cleaned)

    CLEAN_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEAT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(CLEAN_PATH, index=False)
    featured.to_csv(FEAT_PATH, index=False)

    print(f"[pipeline] Clean dataset    → {CLEAN_PATH}")
    print(f"[pipeline] Featured dataset → {FEAT_PATH}  ({featured.shape[1]} columns)")
    return featured


if __name__ == "__main__":
    run_pipeline()
