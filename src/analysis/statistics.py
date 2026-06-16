"""
statistics.py — Statistical Analysis Toolkit
==============================================
Hypothesis testing, correlation analysis, segment profiling,
and ML-based clustering for the EDA project.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[2]


# ── Descriptive Statistics ────────────────────────────────────────────────

def describe_extended(df: pd.DataFrame) -> pd.DataFrame:
    """Extended describe(): adds skewness, kurtosis, and IQR per numeric column."""
    base = df.describe(include="number").T
    num = df.select_dtypes("number")
    base["skewness"] = num.skew()
    base["kurtosis"] = num.kurtosis()
    base["IQR"] = num.quantile(0.75) - num.quantile(0.25)
    return base.round(4)


def outlier_summary(df: pd.DataFrame) -> pd.DataFrame:
    """IQR-based outlier count and percentage per numeric column."""
    records = []
    for col in df.select_dtypes("number").columns:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        mask = (df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)
        records.append({
            "column": col,
            "outliers": int(mask.sum()),
            "outlier_pct": round(mask.mean() * 100, 2),
        })
    return pd.DataFrame(records).sort_values("outliers", ascending=False)


# ── Correlation ────────────────────────────────────────────────────────────

def top_correlations(df: pd.DataFrame, n: int = 15, target: str | None = None) -> pd.DataFrame:
    """Top-n absolute correlations, optionally restricted to a target column."""
    corr = df.select_dtypes("number").corr()
    if target:
        s = corr[target].drop(target).abs().sort_values(ascending=False).head(n)
        return s.reset_index().rename(columns={"index": "feature", target: "abs_corr"})

    pairs = corr.unstack().reset_index()
    pairs.columns = ["var1", "var2", "corr"]
    pairs = pairs[pairs.var1 != pairs.var2].copy()
    pairs["abs_corr"] = pairs["corr"].abs()
    return pairs.drop_duplicates("abs_corr").nlargest(n, "abs_corr").reset_index(drop=True)


# ── Hypothesis Testing ────────────────────────────────────────────────────

def ttest_churn(df: pd.DataFrame, feature: str) -> dict:
    """Two-sample Welch's t-test: active vs. at-risk customers on *feature*."""
    active = df.loc[df.churn_risk == 0, feature].dropna()
    at_risk = df.loc[df.churn_risk == 1, feature].dropna()
    t, p = stats.ttest_ind(active, at_risk, equal_var=False)
    return {
        "feature": feature,
        "t_stat": round(t, 4),
        "p_value": round(p, 6),
        "significant_at_05": p < 0.05,
        "active_mean": round(active.mean(), 4),
        "at_risk_mean": round(at_risk.mean(), 4),
    }


def run_churn_ttests(df: pd.DataFrame) -> pd.DataFrame:
    """Run Welch's t-tests across all numeric features against churn_risk."""
    features = [c for c in df.select_dtypes("number").columns
                if c not in ("churn_risk", "customer_id")]
    return pd.DataFrame([ttest_churn(df, f) for f in features])


def anova_segment(df: pd.DataFrame, feature: str) -> dict:
    """One-way ANOVA: does *feature* differ significantly across customer segments?"""
    groups = [g[feature].dropna().values for _, g in df.groupby("customer_segment")]
    f, p = stats.f_oneway(*groups)
    return {"feature": feature, "f_stat": round(f, 4), "p_value": round(p, 6),
            "significant_at_05": p < 0.05}


# ── Segment & Category Profiling ──────────────────────────────────────────

def segment_profile(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate KPIs per customer segment."""
    return (
        df.groupby("customer_segment")
        .agg(
            n_customers=("customer_id", "count"),
            avg_spend=("total_spend", "mean"),
            avg_orders=("num_orders", "mean"),
            avg_satisfaction=("satisfaction_score", "mean"),
            churn_rate=("churn_risk", "mean"),
            avg_clv=("clv_score", "mean"),
            avg_engagement=("engagement_score", "mean"),
            avg_rfm=("rfm_score", "mean"),
        )
        .round(2)
    )


def category_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and satisfaction breakdown per product category."""
    return (
        df.groupby("preferred_category")
        .agg(
            customers=("customer_id", "count"),
            revenue=("total_spend", "sum"),
            avg_satisfaction=("satisfaction_score", "mean"),
            avg_clv=("clv_score", "mean"),
            churn_rate=("churn_risk", "mean"),
        )
        .sort_values("revenue", ascending=False)
        .round(2)
    )


# ── Clustering ─────────────────────────────────────────────────────────────

def kmeans_segments(df: pd.DataFrame, k: int = 4, random_state: int = 42):
    """
    Run K-Means on key behavioural features and return
    (dataframe with cluster labels, cluster profile summary).
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans

    features = ["total_spend", "num_orders", "satisfaction_score",
                "engagement_score", "recency_score", "clv_score"]
    X = df[features].fillna(df[features].median())
    X_scaled = StandardScaler().fit_transform(X)

    model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    df = df.copy()
    df["cluster"] = model.fit_predict(X_scaled)

    profile = df.groupby("cluster")[features + ["churn_risk"]].mean().round(2)
    return df, profile


if __name__ == "__main__":
    feat_path = ROOT / "data" / "03_features" / "ecommerce_customers_features.csv"
    df = pd.read_csv(feat_path)

    print("\n── Extended Statistics (top 8) ──────────────────")
    print(describe_extended(df).head(8).to_string())

    print("\n── Outlier Summary ──────────────────────────────")
    print(outlier_summary(df).head(10).to_string(index=False))

    print("\n── Significant Churn T-Tests ─────────────────────")
    tt = run_churn_ttests(df)
    print(tt[tt.significant_at_05].to_string(index=False))

    print("\n── Segment Profile ───────────────────────────────")
    print(segment_profile(df).to_string())
