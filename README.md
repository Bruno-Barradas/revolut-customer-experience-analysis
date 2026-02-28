# 🏦 Revolut · Customer Experience & Churn Intelligence Framework

> **Independent Product & Analytics Case Study** — converting unstructured public Google Play reviews into structured retention intelligence using Python, NLP, Machine Learning, Streamlit, and Power BI.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML_Model-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-00C9A7?style=for-the-badge)](LICENSE)

</div>

---

## 🚀 Live Dashboard

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://revolut-customer-experience-analysis.streamlit.app)

---

## 📌 Overview

Digital banks like Revolut operate in high-trust environments where a single operational failure — an account blocked without explanation, a stuck transfer, a verification loop with no resolution — can override months of positive experience and trigger immediate churn.

This project converts unstructured public Google Play reviews into **structured retention intelligence**, building a complete analytics pipeline from raw data collection to machine learning to interactive dashboards.

Rather than treating reviews as qualitative noise, this framework treats them as a **zero-cost early warning system** — real-time, unfiltered, and representative of users who have already formed a definitive opinion about their experience.

---

## 📊 Key Results

<div align="center">

| Metric | Value |
|:-------|:------|
| 📋 Total Reviews Analyzed | **1,200** |
| ⭐ Average Rating | **4.57 ★** |
| ⚠️ Churn Risk Rate | **8.6%** (103 reviews) |
| 💬 Average Sentiment Polarity | **0.455** (positive) |
| 🤖 Model MAE | **~0.50 rating points** |
| 📐 Model R² | **0.25 – 0.30** |

</div>

---

## 🔍 Key Findings

### 1. Churn is Operationally Driven
100% of churn risk (103 reviews) comes from 1★ and 2★ ratings. The dominant keywords in these reviews are **account** (26×), **money** (15×), **support** (12×). Users are not saying "I hate this app" — they are describing specific operational failures: accounts blocked, transfers stuck, support unresponsive.

### 2. Review Length is a Zero-Cost Signal
Churn-risk users write **3.7× longer reviews** (187 chars vs 50 chars for satisfied users). This feature requires zero NLP — a simple character count is a strong leading indicator of dissatisfaction.

### 3. Sentiment ≠ Churn
7 reviews show **positive sentiment polarity but still represent churn risk**. These are the most dangerous cases — a calm, measured user describing a specific operational failure that has already sealed their decision to leave. Sentiment alone is insufficient.

### 4. Bimodal Distribution
83.1% of reviews are 5★, 8.6% are 1–2★. Revolut excels for most users but fails catastrophically for a meaningful minority — concentrated around trust-critical product moments.

---

## 🧠 Methodology

```
Raw Data → Scraping → Cleaning → Feature Engineering → NLP → ML Model → Dashboard
```

| Step | Tool | Output |
|:-----|:-----|:-------|
| Data Collection | google-play-scraper | 1,200 reviews |
| Cleaning & EDA | pandas, numpy | Clean structured dataset |
| Sentiment Analysis | TextBlob, NLTK | sentiment_polarity (–1 to +1) |
| Churn Labeling | Rule-based (rating ≤ 2) | churn_risk binary flag |
| ML Modeling | scikit-learn LinearRegression | MAE ~0.50, R² ~0.28 |
| Visualization | matplotlib, seaborn | EDA charts in notebooks |
| BI Dashboard | Power BI Desktop | Multi-page executive report |
| Web Dashboard | Streamlit | Live interactive web app |
| Documentation | python-docx / docx.js | Professional Word report |

---

## 🤖 Model Details

**Algorithm:** Linear Regression (scikit-learn)
**Target:** Star rating (1–5, continuous regression)
**Features:** `sentiment_polarity` + `review_len`
**Split:** 80% train (960 rows) / 20% test (240 rows)

| Feature | Correlation w/ Rating | Direction | Insight |
|:--------|:---------------------|:----------|:--------|
| `sentiment_polarity` | +0.48 | Positive | Better language → higher rating |
| `review_len` | –0.31 | Negative | Longer review → lower rating |
| `churn_risk` | –0.89 | Strong Negative | Validates proxy label |

### Improvement Path
| Upgrade | Expected Impact | Effort |
|:--------|:---------------|:-------|
| TF-IDF Unigrams | +10–15% R² | Low |
| LDA Topic Modeling | +8–12% R² | Medium |
| XGBoost Classifier | AUC > 0.85 | Low |
| App Version Tracking | Operational value | Medium |

---

## 📂 Repository Structure

```
revolut-customer-experience-analysis/
│
├── 📁 data/
│   ├── revolut_reviews.csv                        # Raw scraped reviews
│   ├── revolut_reviews_clean.csv                  # Cleaned + engineered features
│   └── revolut_reviews_clean_with_sentiment.csv   # + TextBlob sentiment scores
│
├── 📁 notebooks/
│   ├── 01_scraping_and_eda.ipynb                  # Data collection & exploration
│   ├── 02_sentiment_and_churn.ipynb               # NLP + churn labeling
│   └── 03_satisfaction_prediction.ipynb           # ML satisfaction model
│
├── 📁 dashboard/
│   ├── dashboard.py                               # Streamlit web dashboard (5 pages)
│   └── revolut_cx_powerbi.xlsx                   # Power BI data source (5 sheets)
│
├── 📁 docs/
│   └── revolut_cx_report.docx                    # Professional analysis report
│
├── requirements.txt                               # Python dependencies
└── README.md                                      # This file
```

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/revolut-customer-experience-analysis.git
cd revolut-customer-experience-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit dashboard
```bash
streamlit run dashboard/dashboard.py
```

### 4. Open the notebooks
```bash
jupyter notebook notebooks/
```

---

## 📦 Requirements

```
pandas>=2.2.0
numpy>=1.26.0
matplotlib>=3.8.0
scikit-learn>=1.4.0
nltk>=3.8.1
textblob>=0.18.0
wordcloud>=1.9.3
jupyter>=1.0.0
ipykernel>=6.29.0
streamlit>=1.35.0
openpyxl>=3.1.0
python-docx>=1.1.0
```

---

## 📊 Dashboard Pages

| Page | Content |
|:-----|:--------|
| 📊 Overview | KPI cards + rating distribution chart + key insights |
| ⚠️ Churn Analysis | Churn by segment + keyword frequency + mismatch + alert thresholds |
| 💬 Sentiment Deep Dive | Sentiment by rating + distributions + 3★ anomaly analysis |
| 🤖 Model Performance | Metrics + correlations + improvement roadmap + Python code |
| 🔍 Review Explorer | Full dataset with interactive filters + keyword search |

---

## 📈 Power BI Setup

The file `revolut_cx_powerbi.xlsx` contains **5 structured sheets** ready for Power BI import:

| Sheet | Content | Recommended Visual |
|:------|:--------|:------------------|
| Overview | KPI summary + rating distribution | Card visuals + bar chart |
| Raw Data | Full 1,200 reviews with all features | Table + slicers |
| Churn Analysis | Churn by rating + keywords + mismatch | Pie + stacked bar |
| Model Performance | Metrics + correlations + roadmap | Multi-row card + table |
| Pivots for Power BI | Pre-aggregated tables | All chart types |

**Step-by-step:**
1. Open Power BI Desktop → **Get Data → Excel Workbook**
2. Select `revolut_cx_powerbi.xlsx` → Import all 5 sheets
3. Build visuals using the **Pivots for Power BI** sheet
4. Apply brand colors: `#6C21A9` · `#1B2BE6` · `#FF2D78` · `#00C9A7`

---

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub (public)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Configure:
   - **Repository:** `your-username/revolut-customer-experience-analysis`
   - **Branch:** `main`
   - **Main file path:** `dashboard/dashboard.py`
4. Click **Deploy** — live in ~2 minutes

> ✅ The dashboard works **without any external connections** — all data is pre-loaded. No API keys or BigQuery required.

---

## 💼 Business Recommendations

### Immediate (0–30 days)
- **Alert System:** Auto-flag reviews with `rating ≤ 2` + keywords [account, money, support, frozen, blocked] → CX response within 24h
- **Monitoring Dashboard:** Track daily 1–2★ volume as a leading churn indicator in real time

### Medium-term (30–90 days)
- **Root Cause Analysis:** Deep-dive account access failures — the #1 churn keyword (25% of at-risk reviews)
- **Version Correlation:** Map churn spikes to app release versions to detect UX regressions in days
- **Model Upgrade:** Add TF-IDF features → push R² to 0.45+; XGBoost classifier → AUC > 0.85

### Strategic
> In digital banking, **trust is the product.** Account access failures, stuck transfers, and unresponsive support are not service issues — they are product bugs that cost revenue. Every 1★ review citing operational failures is a feature request disguised as a complaint.

---

## 📑 Notebooks

| Notebook | Description |
|:---------|:------------|
| `01_scraping_and_eda.ipynb` | Google Play scraping, data cleaning, EDA, rating distribution visualization |
| `02_sentiment_and_churn.ipynb` | TextBlob sentiment scoring, churn proxy labeling, mismatch analysis, keyword frequency |
| `03_satisfaction_prediction.ipynb` | Feature engineering, Linear Regression, MAE/R² evaluation, sample predictions |

All notebooks are compatible with **Google Colab** and local Jupyter.

---

## ⚠️ Disclaimer

Independent analysis based solely on publicly available user feedback from the Google Play Store. Not affiliated with or endorsed by Revolut Ltd. All analysis is for educational and portfolio purposes only.

---

## 📄 License

MIT License — free to use, modify, and distribute with attribution.

---

<div align="center">
  <b>Built with</b> Python · TextBlob · Scikit-learn · Streamlit · Power BI<br>
  <i>Revolut Customer Experience & Churn Intelligence Framework</i>
</div>
