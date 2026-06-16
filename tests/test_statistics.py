"""Unit tests for src.analysis.statistics"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import pytest

from src.analysis.statistics import (
    describe_extended,
    outlier_summary,
    run_churn_ttests,
    segment_profile,
    top_correlations,
)

ROOT = Path(__file__).resolve().parents[1]
FEAT_PATH = ROOT / "data" / "03_features" / "ecommerce_customers_features.csv"


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(FEAT_PATH)


def test_describe_extended_has_skew_kurtosis(df):
    result = describe_extended(df)
    assert "skewness" in result.columns
    assert "kurtosis" in result.columns


def test_outlier_summary_columns(df):
    result = outlier_summary(df)
    assert {"column", "outliers", "outlier_pct"}.issubset(result.columns)


def test_top_correlations_returns_n_rows(df):
    result = top_correlations(df, n=10)
    assert len(result) <= 10


def test_churn_ttests_has_pvalues(df):
    result = run_churn_ttests(df)
    assert "p_value" in result.columns
    assert (result["p_value"] >= 0).all() and (result["p_value"] <= 1).all()


def test_segment_profile_covers_all_segments(df):
    result = segment_profile(df)
    assert result.shape[0] == df["customer_segment"].nunique()
