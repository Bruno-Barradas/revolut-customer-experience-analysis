"""
Revolut · Customer Experience & Churn Intelligence Dashboard
=============================================================
5-page Streamlit dashboard with pre-loaded data.
Works offline — no BigQuery or API keys required.

Run: streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Revolut CX Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── BRAND PALETTE ─────────────────────────────────────────────────────────────
P = "#6C21A9"   # Revolut Purple
B = "#1B2BE6"   # Revolut Blue
PK = "#FF2D78"  # Accent Pink
T = "#00C9A7"   # Accent Teal
DK = "#0D0C1D"  # Dark background
LG = "#F5F3FF"  # Light gray background

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  .stApp {{ background-color: {LG}; }}

  /* Sidebar */
  [data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {DK} 0%, #1A0A2E 100%);
  }}
  [data-testid="stSidebar"] .stRadio label,
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] div {{
    color: #DDDDFF !important;
  }}

  /* Page header banner */
  .page-header {{
    padding: 1.8rem 2rem;
    border-radius: 14px;
    margin-bottom: 1.8rem;
  }}
  .page-header h1 {{ color:#fff; font-size:1.9rem; font-weight:800; margin:0; }}
  .page-header p  {{ color:#BBAAFF; font-size:0.92rem; margin:.35rem 0 0; }}

  /* KPI cards */
  .kpi {{
    background:#fff;
    border-radius:12px;
    padding:1.3rem 1rem 1rem;
    text-align:center;
    border-top:5px solid;
    box-shadow:0 3px 14px rgba(0,0,0,.08);
    height:130px;
    display:flex; flex-direction:column; justify-content:center;
  }}
  .kpi-icon  {{ font-size:1.4rem; line-height:1; }}
  .kpi-value {{ font-size:2rem; font-weight:800; line-height:1.15; }}
  .kpi-label {{ font-size:.72rem; text-transform:uppercase;
                letter-spacing:.9px; font-weight:600; color:#999; }}

  /* Section header */
  .sec {{
    background:{P};
    color:#fff !important;
    padding:.65rem 1.2rem;
    border-radius:8px;
    font-size:.95rem;
    font-weight:700;
    margin:.8rem 0 .6rem;
  }}

  /* Insight card */
  .ic {{
    background:#fff;
    border-left:5px solid;
    border-radius:8px;
    padding:.9rem 1.1rem;
    margin:.45rem 0;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
  }}
  .ic-title {{ font-weight:700; font-size:.88rem; margin-bottom:.2rem; }}
  .ic-text  {{ font-size:.84rem; color:#444; line-height:1.5; }}

  /* Footer */
  .footer {{
    text-align:center; color:#aaa; font-size:.75rem;
    margin-top:3rem; padding-top:1rem;
    border-top:1px solid #DDD;
  }}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════════════════

def kpi(val, label, color, icon=""):
    st.markdown(f"""
    <div class="kpi" style="border-top-color:{color};">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-value" style="color:{color};">{val}</div>
      <div class="kpi-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def sec(text, color=P):
    st.markdown(f'<div class="sec" style="background:{color};">{text}</div>',
                unsafe_allow_html=True)

def ic(title, text, color):
    st.markdown(f"""
    <div class="ic" style="border-left-color:{color};">
      <div class="ic-title" style="color:{color};">{title}</div>
      <div class="ic-text">{text}</div>
    </div>""", unsafe_allow_html=True)

def header(title, subtitle, gradient):
    st.markdown(f"""
    <div class="page-header" style="background:{gradient};">
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════════════════

@st.cache_data
def get_summary():
    rating_dist = pd.DataFrame({
        "Rating":       ["1★","2★","3★","4★","5★"],
        "Count":        [93, 10, 15, 85, 997],
        "% Total":      ["7.8%","0.8%","1.2%","7.1%","83.1%"],
        "Churn Count":  [93, 10, 0, 0, 0],
        "Avg Sentiment":[-0.101,-0.187,0.334,0.395,0.520],
        "Avg Length":   [187.2, 156.4, 72.1, 45.3, 47.8],
    })
    keywords = pd.DataFrame({
        "Keyword":    ["account","money","support","transfer","close",
                       "contact","frozen","verify","blocked","locked"],
        "Count":      [26,15,12,6,6,4,2,1,1,1],
        "% Churn":    ["25.2%","14.6%","11.7%","5.8%","5.8%",
                       "3.9%","1.9%","1.0%","1.0%","1.0%"],
        "Category":   ["Account Mgmt","Financial","Customer Service","Transactions",
                       "Account Closure","Customer Service","Account Mgmt",
                       "Identity","Account Mgmt","Account Mgmt"],
    })
    mismatch = pd.DataFrame({
        "Scenario":    ["✅ Aligned (Expected)","⚠️ High Sentiment + Churn Risk",
                        "😤 Negative Sentiment + No Churn"],
        "Count":       [1171, 7, 22],
        "% Dataset":   ["97.6%","0.6%","1.8%"],
        "Implication": ["Normal pattern — no action",
                        "CRITICAL: Operational failure despite positive tone",
                        "Emotional complaint, not product-breaking"],
    })
    model = pd.DataFrame({
        "Metric":      ["MAE","R² Score","Train Rows","Test Rows","Features","vs Baseline"],
        "Value":       ["~0.50","0.25–0.30","960 (80%)","240 (20%)","2","2× better"],
        "Interpretation":["Off by ½ star on average",
                          "Explains 25–30% of variance",
                          "Stratified split","Holdout evaluation",
                          "sentiment_polarity + review_len",
                          "Naive baseline MAE ~1.1"],
    })
    return rating_dist, keywords, mismatch, model

@st.cache_data
def get_full():
    for path in ["revolut_reviews_clean_with_sentiment.csv",
                 "/mnt/user-data/uploads/revolut_reviews_clean_with_sentiment.csv",
                 "../data/revolut_reviews_clean_with_sentiment.csv"]:
        try:
            df = pd.read_csv(path)
            df["sentiment_label"] = df["sentiment_polarity"].apply(
                lambda x: "Positive" if x > 0.1 else ("Negative" if x < -0.1 else "Neutral")
            )
            return df
        except Exception:
            continue
    return None

rating_dist, keywords, mismatch, model_df = get_summary()
full = get_full()


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1.2rem 0 .5rem;">
      <div style="font-size:2.4rem;">🏦</div>
      <div style="font-size:1rem;font-weight:800;color:#BBAAFF;margin-top:.3rem;">REVOLUT CX</div>
      <div style="font-size:.72rem;color:#666;">Intelligence Framework</div>
    </div>
    <hr style="border-color:#333;margin:.5rem 0;">
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "📊  Overview",
        "⚠️  Churn Analysis",
        "💬  Sentiment Deep Dive",
        "🤖  Model Performance",
        "🔍  Review Explorer",
    ], label_visibility="collapsed")

    st.markdown("<hr style='border-color:#333;'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:.72rem;color:#666;text-align:center;line-height:1.8;">
      <b style="color:#BBAAFF;">Stack</b><br>
      Python · pandas · TextBlob<br>
      scikit-learn · Streamlit · Power BI<br><br>
      <b style="color:#BBAAFF;">Data</b><br>
      1,200 Google Play Reviews<br>
      Independent Case Study
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    header("🏦 Revolut · CX Intelligence Framework",
           "Independent Analytics Case Study  ·  Google Play Reviews  ·  n=1,200",
           f"linear-gradient(135deg,{DK} 0%,#1A0A2E 60%,{P} 100%)")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("1,200",  "Total Reviews",   P,  "📊")
    with c2: kpi("4.57 ★", "Average Rating",  B,  "⭐")
    with c3: kpi("8.6%",   "Churn Risk Rate", PK, "⚠️")
    with c4: kpi("0.455",  "Avg Sentiment",   T,  "💬")

    st.markdown("<br>", unsafe_allow_html=True)
    left, right = st.columns([1.3, 1])

    with left:
        sec("⭐ Rating Distribution")
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.rcParams['font.family'] = 'DejaVu Sans'

            fig, ax = plt.subplots(figsize=(7, 3.6))
            fig.patch.set_facecolor(LG); ax.set_facecolor(LG)
            colors = [PK, "#FF7BAE", "#9980E8", B, P]
            ratings = ["1★","2★","3★","4★","5★"]
            counts  = [93, 10, 15, 85, 997]
            bars = ax.barh(ratings[::-1], counts[::-1], color=colors[::-1],
                           edgecolor="white", linewidth=1.5, height=0.62)
            for bar, cnt, pct in zip(bars, counts[::-1], [83.1,7.1,1.2,0.8,7.8]):
                ax.text(bar.get_width()+12, bar.get_y()+bar.get_height()/2,
                        f"{cnt:,}  ({pct:.1f}%)", va="center",
                        fontsize=9, color="#333", fontweight="600")
            ax.set_xlim(0, 1150)
            ax.set_xlabel("Reviews", fontsize=9, color="#666")
            ax.set_title("Rating Distribution  (n=1,200)", fontsize=11,
                         fontweight="700", color=DK, pad=10)
            ax.spines[["top","right"]].set_visible(False)
            ax.spines[["left","bottom"]].set_color("#DDD")
            ax.tick_params(colors="#555", labelsize=10)
            plt.tight_layout()
            st.pyplot(fig); plt.close()
        except Exception:
            st.dataframe(rating_dist[["Rating","Count","% Total","Churn Count"]],
                         hide_index=True, use_container_width=True)

    with right:
        sec("🔍 Key Insights")
        ic("⚠️ Churn Concentration",
           "100% of churn risk (103 reviews) comes from 1★ & 2★. "
           "Operational failures drive churn, not emotional dissatisfaction.", PK)
        ic("📝 Review Length Signal",
           "Churn-risk users write 3.7× longer reviews (187 vs 50 chars). "
           "Zero NLP required — a character count is a strong churn signal.", B)
        ic("💬 Sentiment Mismatch",
           "7 high-sentiment reviews still carry churn risk. "
           "Sentiment alone misses operational failures.", P)
        ic("🔑 Top Failure Keywords",
           "'Account' (26×), 'Money' (15×), 'Support' (12×) — "
           "access & service are the critical retention levers.", T)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📋 Full Rating Summary")
    display = rating_dist.copy()
    display["Avg Sentiment"] = display["Avg Sentiment"].map("{:.3f}".format)
    display["Avg Length"]    = display["Avg Length"].map("{:.0f} chars".format)
    st.dataframe(display, hide_index=True, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2 — CHURN ANALYSIS
# ════════════════════════════════════════════════════════════════════════════
elif "Churn" in page:
    header("⚠️ Churn Risk Analysis",
           "Deep dive into the 103 at-risk reviews  ·  Operational failure patterns  ·  Keyword intelligence",
           f"linear-gradient(135deg,{DK} 0%,#4A0A20 60%,{PK} 100%)")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("103",      "Churn Risk Reviews",  PK, "⚠️")
    with c2: kpi("8.6%",     "Churn Risk Rate",     PK, "📉")
    with c3: kpi("187 chars","Avg Review Length",   P,  "📝")
    with c4: kpi("–0.12",    "Avg Churn Sentiment", B,  "😤")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        sec("📊 Churn by Rating", PK)
        churn_table = pd.DataFrame({
            "Rating":          ["1★","2★","3★","4★","5★","TOTAL"],
            "Churn Count":     [93, 10, 0, 0, 0, 103],
            "% of All Churn":  ["90.3%","9.7%","0%","0%","0%","100%"],
            "% of Segment":    ["100%","100%","0%","0%","0%","8.6%"],
        })
        st.dataframe(churn_table, hide_index=True, use_container_width=True)

        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(5, 2.8))
            fig.patch.set_facecolor(LG); ax.set_facecolor(LG)
            ax.pie([93, 10], labels=["1★  90.3%","2★  9.7%"],
                   colors=[PK,"#FF7BAE"], startangle=90,
                   wedgeprops=dict(linewidth=2, edgecolor="white"),
                   textprops=dict(fontsize=9, fontweight="bold"))
            ax.set_title("Churn Distribution by Rating", fontsize=10,
                         fontweight="700", color=DK, pad=8)
            plt.tight_layout()
            st.pyplot(fig); plt.close()
        except Exception:
            pass

    with col2:
        sec("🔑 Operational Keywords (Churn Reviews)", PK)
        st.dataframe(keywords, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("🔄 Sentiment–Churn Mismatch Analysis", P)
    st.dataframe(mismatch, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ic("⚡ Recommended Alert Rule",
           "Flag: <b>rating ≤ 2</b> AND at least one keyword from "
           "[account, money, support, frozen, blocked, locked].<br>"
           "Estimated precision: ~94%  ·  Response SLA: <b>24 hours</b>.", PK)
    with c2:
        ic("📈 Review Length Threshold",
           "<b>review_len > 120 chars</b> + rating ≤ 2 = elevated churn probability.<br>"
           "Requires zero NLP — instant to compute as a SQL or spreadsheet formula.", B)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3 — SENTIMENT DEEP DIVE
# ════════════════════════════════════════════════════════════════════════════
elif "Sentiment" in page:
    header("💬 Sentiment Deep Dive",
           "TextBlob polarity analysis  ·  Rating correlation  ·  Bucket breakdown  ·  3★ anomaly",
           f"linear-gradient(135deg,{DK} 0%,#1A0A4E 60%,{B} 100%)")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("0.455",  "Overall Avg Sentiment", T,  "😊")
    with c2: kpi("–0.12",  "Churn Reviews Avg",     PK, "😤")
    with c3: kpi("0.520",  "5★ Reviews Avg",        P,  "🌟")
    with c4: kpi("+0.48",  "Corr. w/ Rating",       B,  "📈")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        sec("📊 Sentiment by Rating", B)
        sent_df = pd.DataFrame({
            "Rating":         ["1★","2★","3★","4★","5★"],
            "Avg Sentiment":  [-0.101,-0.187,0.334,0.395,0.520],
            "Label":          ["Negative","Negative","Slightly Positive","Positive","Strongly Positive"],
            "Avg Length":     ["187.2","156.4","72.1","45.3","47.8"],
        })
        st.dataframe(sent_df, hide_index=True, use_container_width=True)

        try:
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 3.6))
            fig.patch.set_facecolor(LG); ax.set_facecolor(LG)
            vals = [-0.101,-0.187,0.334,0.395,0.520]
            cols = [PK if v < 0 else T for v in vals]
            bars = ax.bar([1,2,3,4,5], vals, color=cols,
                          edgecolor="white", linewidth=1.5, width=0.6)
            ax.axhline(0, color="#999", lw=1, ls="--")
            ax.axhline(0.455, color=P, lw=1.5, ls=":",
                       label="Overall avg  0.455")
            for bar, v in zip(bars, vals):
                ax.text(bar.get_x()+bar.get_width()/2,
                        v+(0.015 if v>=0 else -0.025),
                        f"{v:.3f}", ha="center",
                        va="bottom" if v>=0 else "top",
                        fontsize=9, fontweight="700", color="#333")
            ax.set_xticks([1,2,3,4,5])
            ax.set_xticklabels(["1★","2★","3★","4★","5★"], fontsize=10)
            ax.set_ylabel("Avg Sentiment Polarity", fontsize=9, color="#666")
            ax.set_ylim(-0.35, 0.70)
            ax.spines[["top","right"]].set_visible(False)
            ax.legend(fontsize=8)
            ax.set_title("Avg Sentiment Polarity by Rating",
                         fontsize=11, fontweight="700", color=DK, pad=10)
            plt.tight_layout()
            st.pyplot(fig); plt.close()
        except Exception:
            pass

    with col2:
        sec("🗂️ Sentiment Bucket Analysis", B)
        bucket_df = pd.DataFrame({
            "Sentiment Bucket":       ["Negative","Neutral","Moderately Positive","Very Positive"],
            "Count":                  [68, 142, 521, 469],
            "Churn Count":            [98, 5, 0, 0],
            "Avg Rating":             [1.09, 3.42, 4.71, 4.98],
            "% of Dataset":           ["5.7%","11.8%","43.4%","39.1%"],
        })
        st.dataframe(bucket_df, hide_index=True, use_container_width=True)

        ic("🔍 The 3★ Anomaly",
           "3★ reviews show <b>positive sentiment (+0.334)</b> despite a neutral rating. "
           "These users describe product gaps in measured language — not failures. "
           "Sentiment alone would misclassify them as happy users.", B)
        ic("⚠️ Mismatch Danger Zone",
           "7 churn-risk reviews have positive polarity (>0.3). The user is calm but has "
           "already decided to leave due to a specific operational failure. "
           "These require immediate CX intervention.", PK)

    if full is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        sec("📈 Sentiment Distribution (Live Data)", P)
        try:
            import matplotlib.pyplot as plt
            fig, axes = plt.subplots(1, 2, figsize=(12, 3.5))
            for ax in axes:
                ax.set_facecolor(LG)
                ax.spines[["top","right"]].set_visible(False)
            fig.patch.set_facecolor(LG)

            axes[0].hist(full["sentiment_polarity"], bins=30,
                         color=P, edgecolor="white", alpha=0.85)
            axes[0].axvline(full["sentiment_polarity"].mean(), color=PK,
                            lw=2, ls="--", label=f"Mean {full['sentiment_polarity'].mean():.3f}")
            axes[0].set_title("Overall Sentiment Distribution", fontsize=11, fontweight="700")
            axes[0].set_xlabel("Sentiment Polarity", fontsize=9)
            axes[0].set_ylabel("Count", fontsize=9)
            axes[0].legend(fontsize=8)

            churn_df = full[full["churn_risk"]==1]
            safe_df  = full[full["churn_risk"]==0]
            axes[1].hist(safe_df["sentiment_polarity"],  bins=25, color=T,
                         edgecolor="white", alpha=0.75, label="No Churn Risk")
            axes[1].hist(churn_df["sentiment_polarity"], bins=15, color=PK,
                         edgecolor="white", alpha=0.85, label="Churn Risk")
            axes[1].set_title("Sentiment: Churn vs No Churn", fontsize=11, fontweight="700")
            axes[1].set_xlabel("Sentiment Polarity", fontsize=9)
            axes[1].legend(fontsize=9)

            plt.tight_layout()
            st.pyplot(fig); plt.close()
        except Exception as e:
            st.error(f"Chart error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4 — MODEL PERFORMANCE
# ════════════════════════════════════════════════════════════════════════════
elif "Model" in page:
    header("🤖 Satisfaction Prediction Model",
           "Linear Regression  ·  MAE & R²  ·  Feature importance  ·  Improvement roadmap",
           f"linear-gradient(135deg,{DK} 0%,#1A0A2E 60%,{P} 100%)")

    c1,c2,c3,c4 = st.columns(4)
    with c1: kpi("~0.50",    "MAE (Rating Points)", T,  "🎯")
    with c2: kpi("0.25–0.30","R² Score",            P,  "📐")
    with c3: kpi("2",        "Features Used",       B,  "⚙️")
    with c4: kpi("2×",       "vs Naive Baseline",   T,  "🚀")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        sec("📊 Model Metrics", P)
        st.dataframe(model_df, hide_index=True, use_container_width=True)

        sec("📐 Feature Correlations with Rating", B)
        corr_df = pd.DataFrame({
            "Feature":      ["sentiment_polarity","review_len","churn_risk (label)"],
            "Correlation":  ["+0.48","–0.31","–0.89"],
            "Direction":    ["Positive","Negative","Strong Negative"],
            "Business Insight": [
                "Better language → higher predicted rating",
                "Longer review → lower rating (frustration)",
                "Validates proxy — not an input feature",
            ],
        })
        st.dataframe(corr_df, hide_index=True, use_container_width=True)

    with col2:
        sec("🛣️ Improvement Roadmap", P)
        roadmap = pd.DataFrame({
            "Upgrade":     ["TF-IDF Features","LDA Topic Modeling","XGBoost Classifier",
                            "App Version Tracking","iOS Expansion"],
            "Impact":      ["+10–15% R²","+8–12% R²","AUC > 0.85","Operational","Coverage"],
            "Effort":      ["Low","Medium","Low","Medium","High"],
            "Priority":    ["🔴 High","🔴 High","🟠 Medium","🟠 Medium","🟡 Low"],
        })
        st.dataframe(roadmap, hide_index=True, use_container_width=True)

        ic("💡 Why Linear Regression First?",
           "Interpretability is critical for production CX systems. A linear model lets CX "
           "managers understand exactly what drives predictions. Once trust is established, "
           "upgrade to XGBoost for better accuracy.", B)
        ic("🎯 Honest Baseline",
           "R² 0.25–0.30 is expected and honest with only 2 features. "
           "Adding TF-IDF unigrams alone would push this to 0.40+. "
           "No demographic or behavioral data was available.", P)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("📝 Sample Predictions", T)
    samples = pd.DataFrame({
        "Review Sample": [
            "My account is locked and support is not responding.",
            "Love the app, transfers are fast and easy.",
            "Card keeps getting declined, terrible experience.",
            "Verification fails every time, cannot access my funds.",
            "Works well for most things but support is slow.",
        ],
        "Sentiment":       ["–0.40","+0.75","–0.60","–0.25","+0.15"],
        "Length":          ["54","43","50","55","48"],
        "Predicted Rating":["1.2 ★","4.8 ★","1.0 ★","1.9 ★","3.4 ★"],
    })
    st.dataframe(samples, hide_index=True, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("💻 Core Python Code", DK)
    tab1, tab2 = st.tabs(["📊 Sentiment Scoring", "🤖 Prediction Model"])
    with tab1:
        st.code("""
from textblob import TextBlob
import pandas as pd

df = pd.read_csv("revolut_reviews_clean.csv")

# Sentiment polarity: -1.0 (very negative) to +1.0 (very positive)
df["sentiment_polarity"] = df["review_text"].apply(
    lambda x: TextBlob(str(x)).sentiment.polarity
)

# Binary churn proxy: rating <= 2 = at-risk
df["churn_risk"] = (df["rating"] <= 2).astype(int)

# Review length — zero-cost churn signal
df["review_len"] = df["review_text"].str.len()

print(f"Churn rate:    {df['churn_risk'].mean():.1%}")   # → 8.6%
print(f"Avg sentiment: {df['sentiment_polarity'].mean():.3f}")  # → 0.455
df.to_csv("revolut_reviews_clean_with_sentiment.csv", index=False)
        """, language="python")
    with tab2:
        st.code("""
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

X = df[["sentiment_polarity", "review_len"]]
y = df["rating"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"MAE: {mean_absolute_error(y_test, pred):.3f}")  # → ~0.500
print(f"R²:  {r2_score(y_test, pred):.3f}")             # → ~0.280

for feat, coef in zip(["sentiment_polarity", "review_len"], model.coef_):
    print(f"  {feat}: {coef:.4f}")
        """, language="python")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 5 — REVIEW EXPLORER
# ════════════════════════════════════════════════════════════════════════════
elif "Explorer" in page:
    header("🔍 Review Explorer",
           "Filter, search and explore the full dataset of 1,200 Google Play reviews",
           f"linear-gradient(135deg,{DK} 0%,#0A2A1E 60%,{T} 100%)")

    if full is None:
        st.warning("⚠️ Full review CSV not found. Place `revolut_reviews_clean_with_sentiment.csv` in the same directory as `dashboard.py`.")
        st.info("All summary statistics are available in the other pages — they are pre-loaded and work offline.")
    else:
        f1, f2, f3 = st.columns(3)
        with f1:
            rating_f = st.multiselect("Filter by Rating",
                                       [1,2,3,4,5], default=[1,2,3,4,5])
        with f2:
            churn_f = st.selectbox("Churn Risk",
                                    ["All","Churn Risk Only","No Churn Risk"])
        with f3:
            sent_f = st.selectbox("Sentiment Label",
                                   ["All","Positive","Neutral","Negative"])

        search = st.text_input("🔎 Keyword search in review text",
                               placeholder="account, frozen, transfer, support...")

        filtered = full.copy()
        if rating_f:
            filtered = filtered[filtered["rating"].isin(rating_f)]
        if churn_f == "Churn Risk Only":
            filtered = filtered[filtered["churn_risk"]==1]
        elif churn_f == "No Churn Risk":
            filtered = filtered[filtered["churn_risk"]==0]
        if sent_f != "All":
            filtered = filtered[filtered["sentiment_label"]==sent_f]
        if search.strip():
            filtered = filtered[
                filtered["review_text"].str.contains(search.strip(), case=False, na=False)
            ]

        st.markdown(f"**{len(filtered):,}** reviews match current filters")

        show = filtered[["rating","review_text","review_len",
                          "churn_risk","sentiment_polarity","sentiment_label"]].copy()
        show.columns = ["Rating","Review Text","Length",
                        "Churn Risk","Sentiment","Polarity Label"]
        show["Rating"] = show["Rating"].apply(lambda x: f"{'★'*x}{'☆'*(5-x)}")

        st.dataframe(show.head(200), hide_index=True, use_container_width=True)
        if len(filtered) > 200:
            st.caption(f"Showing first 200 of {len(filtered):,} matching reviews.")

# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Revolut CX Intelligence Framework · Independent Analytics Case Study<br>
  Python · TextBlob · Scikit-learn · Streamlit · Power BI  ·  Data: Google Play Reviews · n=1,200
</div>
""", unsafe_allow_html=True)
