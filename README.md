# Predictive Analytics and Explainable AI for Hospital Readmission Risk

**Course:** CS 719: Data Science Project  
**Student:** Raj Panchal (200490453)  
**Instructor:** Dr. Howard J. Hamilton  
**University of Regina** | Winter 2026

---

## Overview

This project predicts whether a hospital patient will be readmitted within 30 days of discharge, using the UCI 130-US Hospitals dataset (101,766 encounters). Beyond building a predictive model, the focus is on **explainability** (understanding *why* the model makes each prediction) and making those insights accessible through an interactive Streamlit dashboard designed for clinical use.

The project also includes a quantitative comparison between the trained XGBoost model and the **LACE Index**, a rule-based scoring system widely used in Canadian hospitals, evaluated on the same held-out test set.

---

## Project Structure

```
├── Data/
│   └── data.csv                                      # UCI 130-US Hospitals dataset
├── notebooks/
│   └── Executed_200490453_Raj_Panchal_CS719_Project_Notebook.ipynb
├── src/
│   └── utils.py                                      # Reusable helper functions
├── model_artifacts/
│   ├── model.joblib                                  # Trained XGBoost model
│   ├── scaler.joblib                                 # StandardScaler
│   ├── feature_names.json                            # 46 feature names
│   ├── pfi_results.csv                               # Permutation Feature Importance results
│   ├── population_stats.csv                          # Population averages for dashboard
│   └── config.json                                   # Threshold, model name, test metrics
├── streamlit_app.py                                  # Interactive dashboard
├── requirements.txt
└── README.md
```

---

## Dataset

| Property | Value |
|----------|-------|
| Source | UCI ML Repository: 130-US Hospitals (1999–2008) |
| Raw size | 101,766 encounters × 50 features |
| After cleaning | 99,340 encounters × 23 columns |
| After encoding | 46 features |
| Target | Binary: readmitted within 30 days (1) vs. not (0) |
| Class balance | ~11.4% positive (severe imbalance) |

---

## Methodology

The notebook walks through 18 sections end-to-end:

1. **Setup & Imports**
2. **Data Loading & Inspection**: shape, types, memory, initial profile
3. **Data Cleaning**: dropped high-null columns, zero-variance columns, removed expired/hospice discharges
4. **Feature Engineering**: `total_visits`, `num_med_changed`, `num_med_active`, `age_numeric`; binary target conversion
5. **Exploratory Data Analysis**: distributions, correlation matrix, readmission rate by age and prior visits
6. **Statistical Tests**: Shapiro-Wilk normality, Pearson/Spearman correlation, Chi-squared
7. **Preprocessing**: one-hot encoding, 80/20 stratified split, SMOTE on training set only, StandardScaler
8. **Model Training & Hyperparameter Tuning**: GridSearchCV (3-fold, ROC-AUC) on Logistic Regression, Random Forest, XGBoost
9. **Model Evaluation & Comparison**: confusion matrices, ROC curves, Precision-Recall curves, 5-fold CV stability
10. **Best Model Selection**: selected based on test ROC-AUC + CV stability
11. **Explainability: PFI**: Permutation Feature Importance on XGBoost
12. **Explainability: PDP**: Partial Dependence Plots for top features
13. **Threshold Optimization**: swept 0.05–0.95, maximized F1; moved from 0.50 → 0.20
14. **LACE Index vs. XGBoost**: head-to-head comparison on the same test set (ROC-AUC, precision, recall, F1)
15. **Sample Predictions**: 20 random test patients with actual vs. predicted
16. **Patient Risk Assessment**: interactive `predict_patient()` function with risk gauge and feature profile
17. **Export Model Artifacts**: saved model, scaler, feature names, PFI, population stats, config
18. **Conclusion**: summary table and key takeaways

---

## Model Results

| Model | ROC-AUC | F1 Score | Accuracy |
|-------|---------|----------|----------|
| Logistic Regression | 0.6418 | 0.7053 | 64.1% |
| Random Forest | 0.6470 | 0.8374 | 88.5% |
| **XGBoost** | **0.6648** | **0.8406** | **88.6%** |

**Optimal threshold:** 0.20 (up from default 0.50)  
Recall improved from ~4% → ~35% at the optimal threshold. This is critical in a clinical setting where missing a high-risk patient carries real cost.

---

## LACE vs. XGBoost

The LACE Index (Length of stay, Acuity, Comorbidity, ED visits) uses just 4 factors to classify readmission risk. This project computes LACE scores for every patient in the held-out test set and benchmarks it directly against XGBoost: same patients, same ground truth, no retraining.

XGBoost outperforms LACE on every metric that matters for catching readmissions: ROC-AUC (0.6648 vs 0.5585), Precision, Recall (35.2% vs 2.1%), and F1 Score. LACE does show higher raw accuracy (87.95% vs 79.08%), but that's the accuracy paradox at work. With only 1.1% of patients flagged as high-risk, LACE gets most predictions "right" by simply saying "not readmitted" almost every time. XGBoost's richer feature set (46 features vs 4) gives it far better discriminative power, while LACE's simplicity (no training needed, works anywhere) explains why hospitals still rely on it.

---

## Explainability

**Top predictors by Permutation Feature Importance:**

| Rank | Feature | Why it matters |
|------|---------|---------------|
| 1 | `number_inpatient` | Prior hospital use is the strongest readmission signal |
| 2 | `discharge_disposition_id` | Where a patient goes after discharge strongly affects return risk |
| 3 | `total_visits` | Combined history of outpatient + emergency + inpatient visits |
| 4 | `number_diagnoses` | More diagnoses = higher complexity = higher risk |
| 5 | `admission_type_id` | Emergency admissions correlate with higher readmission rates |

Partial Dependence Plots confirm a strong monotonic relationship between `number_inpatient` and predicted readmission probability.

---

## Streamlit Dashboard

The dashboard (`streamlit_app.py`) wraps the trained model into a clinical tool with four tabs:

- **Risk Assessment**: adjust patient parameters via sliders, get a real-time risk score and verdict
- **Explainability & What-If**: see which features drive the prediction and simulate changes
- **Clinical Impact**: threshold optimization impact, LACE vs. XGBoost comparison, live side-by-side patient scoring, and cost savings estimator
- **Model Performance**: model comparison table with dataset and training details

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the Streamlit dashboard
streamlit run streamlit_app.py
```

To re-run the notebook, open it in Google Colab (recommended) or Jupyter and upload `Data/data.csv` and `src/utils.py` when prompted by the Colab setup cell.

---

## Requirements

```
pandas>=2.0
numpy>=1.24
matplotlib>=3.7
seaborn>=0.12
scikit-learn>=1.3
scipy>=1.11
imbalanced-learn>=0.11
xgboost>=2.0
streamlit>=1.32
joblib>=1.3
```
