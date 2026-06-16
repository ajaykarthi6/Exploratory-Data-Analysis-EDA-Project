"""Unit tests for src.ingestion.pipeline"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
import pytest

from src.ingestion.pipeline import clean, engineer_features, load_raw


@pytest.fixture(scope="module")
def raw_df():
    return load_raw()


def test_load_raw_shape(raw_df):
    assert raw_df.shape[0] > 0
    assert "customer_id" in raw_df.columns


def test_clean_removes_missing(raw_df):
    cleaned = clean(raw_df)
    assert cleaned["satisfaction_score"].isnull().sum() == 0
    assert cleaned["email_open_rate"].isnull().sum() == 0


def test_engineer_features_adds_columns(raw_df):
    cleaned = clean(raw_df)
    featured = engineer_features(cleaned)
    for col in ["clv_score", "engagement_score", "rfm_score", "value_tier"]:
        assert col in featured.columns


def test_clv_score_non_negative(raw_df):
    cleaned = clean(raw_df)
    featured = engineer_features(cleaned)
    assert (featured["clv_score"] >= 0).all()


def test_value_tier_has_five_levels(raw_df):
    cleaned = clean(raw_df)
    featured = engineer_features(cleaned)
    assert featured["value_tier"].nunique() <= 5
