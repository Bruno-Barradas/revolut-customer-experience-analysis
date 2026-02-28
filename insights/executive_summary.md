# Executive Summary — Revolut Customer Experience & Retention Analysis

## Objective
Analyze public Google Play reviews to identify satisfaction drivers, operational pain points, churn signals, and build a predictive model for satisfaction.

## Dataset
- Source: Google Play Store
- Market: US
- Language: English
- Reviews analyzed: ~1,200

Churn proxy:
- churn_risk = 1 if rating ≤ 2

## Key Findings

### 1) Ratings are polarized
Strong 5★ cluster and significant 1★ cluster driven by critical incidents.

### 2) Core churn drivers
- Account restrictions
- Verification friction
- Transfer failures
- Card declines
- Poor support responsiveness

### 3) Important insight
Rating ≠ pure sentiment.
Some 1★ reviews show neutral-ish sentiment because users describe specific operational failures rather than emotional rejection.

This suggests reliability issues in “trust moments” have disproportionate impact on churn.

## Predictive Model
Linear regression using:
- Sentiment polarity
- Review length

Results:
- MAE ≈ ~0.5 rating points
- R² ≈ ~0.25–0.30 (expected for human behavioral data)

## Conclusion
Operational reliability and transparency in high-risk flows (verification, account access, transfers) are key levers for retention improvement.