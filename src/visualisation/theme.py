"""
theme.py — Shared Visual Theme
================================
Centralised dark-mode colour palette and matplotlib/plotly styling
used consistently across every chart in this project.
"""

import matplotlib.pyplot as plt

# ── Palette ────────────────────────────────────────────────────────────────
BG       = "#060B14"
PANEL    = "#0D1421"
PANEL2   = "#111927"
BORDER   = "#1E2D40"
TEXT     = "#E2EAF4"
SUBTEXT  = "#8899AA"

C1, C2, C3, C4 = "#00D4FF", "#7B61FF", "#FF6B6B", "#FFD93D"
C5, C6, C7, C8 = "#6BCB77", "#FF9F43", "#A29BFE", "#FD79A8"
PALETTE = [C1, C2, C3, C4, C5, C6, C7, C8]

SEGMENT_COLORS = {
    "Champion": C1, "Loyal": C5, "Potential Loyalist": C2,
    "New Customer": C4, "At-Risk": C3, "Hibernating": C6, "Lost": C7,
}

TIER_COLORS = {
    "Bronze": "#CD7F32", "Silver": "#C0C0C0", "Gold": "#FFD700",
    "Platinum": "#E5E4E2", "Diamond": "#B9F2FF",
}


def apply_matplotlib_theme() -> None:
    """Apply the project's dark theme to matplotlib's global rcParams."""
    plt.rcParams.update({
        "figure.facecolor": BG, "axes.facecolor": PANEL, "axes.edgecolor": BORDER,
        "axes.labelcolor": SUBTEXT, "xtick.color": SUBTEXT, "ytick.color": SUBTEXT,
        "text.color": TEXT, "grid.color": BORDER, "grid.linestyle": "-", "grid.alpha": 0.4,
        "font.family": "DejaVu Sans", "axes.titlesize": 12, "axes.titleweight": "bold",
        "axes.titlepad": 10, "axes.spines.top": False, "axes.spines.right": False,
    })


def plotly_template():
    """Return a Plotly go.layout.Template matching the project theme."""
    import plotly.graph_objects as go

    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor=BG, plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Inter, Segoe UI, sans-serif"),
        xaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=SUBTEXT),
        yaxis=dict(gridcolor=BORDER, zerolinecolor=BORDER, color=SUBTEXT),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, l=60, r=30, b=60),
    )
    return template
