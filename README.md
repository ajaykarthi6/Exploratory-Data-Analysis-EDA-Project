<div align="center">

# 🌐 Exploratory Data Analysis (EDA) Project
### Global E-Commerce Customer Intelligence

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-10%20passing-6BCB77?style=for-the-badge)

*Turning 1,500 raw customer records into a living, interactive intelligence report.*

**[📊 Open the Interactive Report →](reports/html/interactive_report.html)**

</div>

---

## 💡 What makes this project different

Most EDA projects stop at static charts in a notebook. This one ships a **self-contained interactive HTML dashboard** (Plotly, zero server required), a **medallion-style data architecture** (raw → processed → features), **unsupervised K-Means validation** of manually-defined segments, and a **tested, modular `src/` package** — not just analysis scripts, but a small reusable analytics library.

| Feature | Why it's here |
|---------|----------------|
| 🖱️ **Interactive HTML report** | 3D scatter, animated bar race, sunburst, parallel-categories flow — explore the data, don't just look at it |
| 🏗️ **Medallion architecture** | `01_raw → 02_processed → 03_features` mirrors real-world data engineering practice |
| 🤖 **K-Means + PCA validation** | Checks whether manually-defined RFM segments hold up against unsupervised clustering |
| ✅ **10 passing unit tests** | Cleaning and feature-engineering logic is verified, not just eyeballed |
| 🎨 **One shared theme module** | Every chart — static or interactive — pulls colours from a single `theme.py` |
| 📓 **Modular `src/` package** | `ingestion`, `analysis`, `visualisation`, `utils` — reusable beyond this one notebook |

---

## 🗂️ Repository Structure

```
EDA-Project/
├── data/
│   ├── 01_raw/                          ← Immutable source data
│   │   ├── ecommerce_customers_raw.csv      (1,500 × 30 features)
│   │   └── data_dictionary.csv
│   ├── 02_processed/                    ← Cleaned + analytical outputs
│   │   ├── ecommerce_customers_clean.csv
│   │   ├── statistical_summary.csv
│   │   ├── outlier_summary.csv
│   │   ├── churn_ttests.csv
│   │   ├── segment_profiles.csv
│   │   └── category_analysis.csv
│   └── 03_features/                     ← Final analytical dataset
│       └── ecommerce_customers_features.csv  (1,500 × 42 features incl. cluster)
│
├── notebooks/
│   └── eda_analysis.ipynb               ← End-to-end walkthrough (21 cells)
│
├── reports/
│   ├── figures/                         ← 6 static dark-themed dashboards
│   │   ├── 01_overview/hero_kpi_dashboard.png
│   │   ├── 02_demographics/demographics_deep_dive.png
│   │   ├── 03_behaviour/behaviour_engagement.png
│   │   ├── 04_churn/churn_risk_intelligence.png
│   │   ├── 05_financial/financial_intelligence.png
│   │   └── 06_advanced/advanced_analytics.png
│   ├── html/
│   │   └── interactive_report.html      ← 🌟 Self-contained interactive report
│   └── insights/
│       └── findings.md
│
├── src/
│   ├── ingestion/pipeline.py            ← load_raw, clean, engineer_features
│   ├── analysis/statistics.py           ← hypothesis tests, correlation, K-Means
│   ├── visualisation/theme.py           ← shared colour palette / styling
│   └── utils/reporting.py               ← KPI + markdown summary generation
│
├── tests/
│   ├── test_pipeline.py                 ← 5 tests
│   └── test_statistics.py               ← 5 tests
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── DATA_DICTIONARY.md
│
├── Makefile
├── requirements.txt
└── README.md
```

---

## 📊 Dataset at a Glance

| Property | Detail |
|----------|--------|
| Customers | 1,500 |
| Raw features | 30 |
| Engineered features | +12 (CLV, RFM, engagement, recency, value tier, cluster, …) |
| Countries / Regions | 12 countries → 5 world regions |
| Segments | 7 RFM-style tiers (Champion → Lost) |
| Missing data | ~4% satisfaction, ~2% email rate — imputed contextually (by segment / channel) |

---

## 🔍 Headline Findings

1. **Satisfaction predicts churn** — Welch's t-test confirms a statistically significant gap (p < 0.001) between active and at-risk customers' CSAT scores.
2. **Email engagement is a leading indicator** — open rates decline measurably *before* churn occurs, not just after.
3. **K-Means validates the segmentation** — 4 unsupervised clusters (PCA-projected) align closely with the manually engineered RFM segments, lending confidence to the segment definitions.
4. **Champions carry outsized value** — a small minority of customers account for a disproportionate share of total CLV.
5. **Desktop converts higher value despite lower share** — Mobile dominates traffic (52%), but Desktop shows higher average order value.
6. **Sports & Fitness and Electronics dominate revenue** — concentrate merchandising and promotions here.

Full reasoning and supporting visuals live in [`reports/insights/findings.md`](reports/insights/findings.md) and the interactive report.

---

## 🖥️ Explore the Interactive Report

Open **`reports/html/interactive_report.html`** directly in any browser — no server, no dependencies. It includes:

- 🌅 **Sunburst** — customer segments nested by region (click to drill down)
- 🌌 **3D scatter** — engagement × recency × CLV, coloured by satisfaction (drag to rotate)
- 📊 **Filterable bar chart** — revenue by category, switch income brackets on the fly
- 🌊 **Parallel categories** — trace customers from segment → value tier → churn status
- 🎬 **Animated scatter** — press play to watch income-vs-spend shift across generations
- 🔻 **Loyalty funnel** — from "all customers" down to "Champions only"

---

## ⚙️ Setup & Run

```bash
# Clone
git clone https://github.com/ajaykarthi6/Exploratory-Data-Analysis-EDA-Project.git
cd Exploratory-Data-Analysis-EDA-Project

# Install
make install        # or: pip install -r requirements.txt

# Run the full pipeline (raw → clean → features)
make pipeline

# Run the statistical analysis suite
make stats

# Run tests
make test

# Launch the notebook
make notebook
```

Or without `make`:

```bash
pip install -r requirements.txt
python -m src.ingestion.pipeline
python -m src.analysis.statistics
pytest tests/ -v
jupyter notebook notebooks/eda_analysis.ipynb
```

---

## 🧪 Testing

```
10 passed in ~1s
```

Covers: missing-value imputation correctness, feature-engineering output integrity, CLV non-negativity, value-tier cardinality, statistical-test output ranges, and segment-profile completeness.

---

## 📚 Further Reading

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — medallion data flow & module responsibilities
- [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md) — full column reference, raw + engineered

---

<div align="center">

Made with 🔍 curiosity and 📊 data — by **Ajay** @ RMKEC

</div>
