"""
reporting.py — Reporting Utilities
=====================================
Helper functions for generating markdown insight summaries
and exporting key tables for the final report.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def kpi_summary(df: pd.DataFrame) -> dict:
    """Compute the headline KPIs shown across reports and the README."""
    return {
        "total_customers": len(df),
        "avg_annual_income": round(df.annual_income.mean(), 2),
        "avg_total_spend": round(df.total_spend.mean(), 2),
        "churn_rate_pct": round(df.churn_risk.mean() * 100, 2),
        "avg_satisfaction": round(df.satisfaction_score.mean(), 2),
        "avg_clv_score": round(df.clv_score.mean(), 2),
        "total_revenue": round(df.total_spend.sum(), 2),
        "top_category_by_revenue": df.groupby("preferred_category")["total_spend"]
            .sum().idxmax(),
        "top_country_by_customers": df.country.value_counts().idxmax(),
    }


def write_findings_md(df: pd.DataFrame, out_path: Path) -> None:
    """Render a markdown findings summary to *out_path*."""
    kpis = kpi_summary(df)
    seg_profile = (
        df.groupby("customer_segment")
        .agg(avg_clv=("clv_score", "mean"), churn_rate=("churn_risk", "mean"))
        .round(2)
        .sort_values("avg_clv", ascending=False)
    )

    lines = [
        "# Key Findings — Global E-Commerce Customer EDA\n",
        f"- **{kpis['total_customers']:,} customers** analysed across 12 countries\n",
        f"- Average lifetime spend: **${kpis['avg_total_spend']:,.0f}**, "
        f"average CLV score: **{kpis['avg_clv_score']:,.0f}**\n",
        f"- Overall churn risk rate: **{kpis['churn_rate_pct']}%**\n",
        f"- Top revenue category: **{kpis['top_category_by_revenue']}**\n",
        f"- Most customers come from: **{kpis['top_country_by_customers']}**\n",
        "\n## Segment Value Ranking\n",
        seg_profile.to_markdown(),
    ]
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines))
    print(f"[reporting] Findings written → {out_path}")


if __name__ == "__main__":
    feat_path = ROOT / "data" / "03_features" / "ecommerce_customers_features.csv"
    df = pd.read_csv(feat_path)
    write_findings_md(df, ROOT / "reports" / "insights" / "findings.md")
