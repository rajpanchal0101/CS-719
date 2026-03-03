"""
Diabetes Readmission Risk Assessment — Explainable AI Dashboard
Clinical Decision Support Tool for Healthcare Professionals

CS 719 — Data Scientist Assistant
Dataset: Diabetes 130-US Hospitals (101,766 encounters)
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import joblib
import os

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Readmission Risk — Explainable AI",
    page_icon="\U0001F3E5",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS — clean healthcare aesthetic
# ═══════════════════════════════════════════════════════════════
st.markdown("""<style>
    .main-header {
        font-size: 2.2rem; font-weight: 700; color: #1565C0;
        text-align: center; padding: 0.5rem 0;
    }
    .sub-header {
        font-size: 1.1rem; color: #546E7A;
        text-align: center; margin-bottom: 1.5rem;
    }
    .risk-high {
        background-color: #FFCDD2; color: #B71C1C;
        padding: 1.2rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #EF9A9A;
    }
    .risk-medium {
        background-color: #FFE0B2; color: #E65100;
        padding: 1.2rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #FFCC80;
    }
    .risk-low {
        background-color: #C8E6C9; color: #1B5E20;
        padding: 1.2rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #A5D6A7;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 1.5rem; }
    .stTabs [data-baseweb="tab"] { font-size: 1.05rem; }
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# LOAD MODEL ARTIFACTS
# ═══════════════════════════════════════════════════════════════
@st.cache_resource
def load_artifacts():
    model = joblib.load("model_artifacts/model.joblib")
    scaler = joblib.load("model_artifacts/scaler.joblib")
    with open("model_artifacts/feature_names.json", "r") as f:
        feature_names = json.load(f)
    pfi_df = pd.read_csv("model_artifacts/pfi_results.csv")
    pop_stats = pd.read_csv("model_artifacts/population_stats.csv", index_col=0)
    with open("model_artifacts/config.json", "r") as f:
        config = json.load(f)
    return model, scaler, feature_names, pfi_df, pop_stats, config

try:
    model, scaler, feature_names, pfi_df, pop_stats, config = load_artifacts()
    optimal_threshold = config["optimal_threshold"]
except Exception as e:
    st.error(
        "Could not load model artifacts. Please run the Jupyter notebook first "
        "to train the model and save artifacts.\n\n"
        f"Error: {e}"
    )
    st.stop()

# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown(
    '<div class="main-header">\U0001F3E5 Diabetes Readmission Risk Assessment</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    "Explainable AI for Clinical Decision Support \u2014 "
    "Diabetes 130-US Hospitals"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# ═══════════════════════════════════════════════════════════════
# SIDEBAR — Patient Input
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("\U0001F9D1\u200D\u2695\uFE0F Patient Parameters")
    st.markdown(
        "Adjust the sliders below to assess readmission risk "
        "for a patient encounter."
    )
    st.markdown("---")

    # --- Primary clinical inputs ---
    st.subheader("Primary Inputs")
    age_group = st.slider(
        "Age Group (midpoint)", 5, 95, 65, step=10,
        help="Patient age range midpoint (e.g. 65 = age 60\u201370)",
    )
    number_inpatient = st.slider(
        "Prior Inpatient Visits", 0, 15, 0,
        help="Inpatient visits in the year before this encounter",
    )
    num_medications = st.slider(
        "Number of Medications", 1, 50, 15,
        help="Distinct medications administered during this encounter",
    )
    time_in_hospital = st.slider(
        "Days in Hospital", 1, 14, 4,
        help="Length of the current hospital stay",
    )
    number_diagnoses = st.slider(
        "Number of Diagnoses", 1, 16, 7,
        help="Number of diagnoses coded for this encounter",
    )

    st.markdown("---")
    st.subheader("Additional Parameters")

    number_emergency = st.slider("Prior Emergency Visits", 0, 20, 0)
    number_outpatient = st.slider("Prior Outpatient Visits", 0, 20, 0)
    num_procedures = st.slider("Number of Procedures", 0, 6, 1)
    num_lab_procedures = st.slider("Number of Lab Procedures", 1, 132, 44)

    discharge_disposition_id = st.selectbox(
        "Discharge Disposition",
        options=[1, 2, 3, 4, 5, 6],
        format_func=lambda x: {
            1: "1 \u2014 Discharged to home",
            2: "2 \u2014 Short-term hospital transfer",
            3: "3 \u2014 Skilled nursing facility (SNF)",
            4: "4 \u2014 Intermediate care facility",
            5: "5 \u2014 Another type of facility",
            6: "6 \u2014 Home health service",
        }.get(x, str(x)),
        index=0,
    )
    admission_type_id = st.selectbox(
        "Admission Type",
        options=[1, 2, 3, 5, 6],
        format_func=lambda x: {
            1: "1 \u2014 Emergency",
            2: "2 \u2014 Urgent",
            3: "3 \u2014 Elective",
            5: "5 \u2014 Not Available",
            6: "6 \u2014 Trauma Center",
        }.get(x, str(x)),
        index=0,
    )

# ═══════════════════════════════════════════════════════════════
# PREDICTION ENGINE
# ═══════════════════════════════════════════════════════════════
def make_prediction():
    """Build feature vector, scale, predict, return results."""
    raw_numeric = {
        "admission_type_id": admission_type_id,
        "discharge_disposition_id": discharge_disposition_id,
        "admission_source_id": 7,
        "time_in_hospital": time_in_hospital,
        "num_lab_procedures": num_lab_procedures,
        "num_procedures": num_procedures,
        "num_medications": num_medications,
        "number_outpatient": number_outpatient,
        "number_emergency": number_emergency,
        "number_inpatient": number_inpatient,
        "number_diagnoses": number_diagnoses,
        "change": int(pop_stats.loc["change", "median"]),
        "diabetesMed": int(pop_stats.loc["diabetesMed", "median"]),
        "total_visits": number_outpatient + number_emergency + number_inpatient,
        "num_med_changed": int(pop_stats.loc["num_med_changed", "median"]),
        "num_med_active": int(pop_stats.loc["num_med_active", "median"]),
        "age_numeric": age_group,
    }
    categorical = {
        "race": "Caucasian",
        "gender": "Female",
        "diag_1": "Circulatory",
        "diag_2": "Circulatory",
        "diag_3": "Other",
    }

    patient_encoded = pd.DataFrame(0, index=[0], columns=feature_names, dtype=float)
    for col, val in raw_numeric.items():
        if col in feature_names:
            patient_encoded[col] = val
    for col, val in categorical.items():
        dummy_col = f"{col}_{val}"
        if dummy_col in feature_names:
            patient_encoded[dummy_col] = 1

    patient_scaled = pd.DataFrame(
        scaler.transform(patient_encoded), columns=feature_names
    )

    prob = float(model.predict_proba(patient_scaled)[0, 1])
    pred = int(prob >= optimal_threshold)

    if prob >= 0.30:
        risk, color = "HIGH RISK", "#FF1744"
    elif prob >= optimal_threshold:
        risk, color = "MEDIUM RISK", "#FF9100"
    else:
        risk, color = "LOW RISK", "#00C853"

    return prob, pred, risk, color, raw_numeric


prob, pred, risk, risk_color, raw_numeric = make_prediction()

# ═══════════════════════════════════════════════════════════════
# MAIN CONTENT — TABS
# ═══════════════════════════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(
    [
        "\U0001FA7A Risk Assessment",
        "\U0001F50D Explainability & What-If",
        "\U0001F4CA Model Performance",
    ]
)

# ──────────────────────────────────────────────────────────────
# TAB 1 — RISK ASSESSMENT
# ──────────────────────────────────────────────────────────────
with tab1:
    # Top metrics row
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        css_cls = (
            "risk-high" if prob >= 0.30
            else ("risk-medium" if prob >= optimal_threshold else "risk-low")
        )
        st.markdown(f'<div class="{css_cls}">{risk}</div>', unsafe_allow_html=True)
    with col2:
        baseline_rate = 0.114
        st.metric(
            "Readmission Probability",
            f"{prob:.0%}",
            delta=f"{prob - baseline_rate:+.0%} vs baseline (11.4%)",
            delta_color="inverse",
        )
    with col3:
        st.metric(
            "Binary Prediction",
            "1 \u2014 Readmitted" if pred else "0 \u2014 Not Readmitted",
            delta=f"Threshold: {optimal_threshold:.2f}",
        )

    st.markdown("---")

    # Risk gauge + Feature profile
    col_gauge, col_features = st.columns([1, 1])

    with col_gauge:
        st.subheader("Risk Gauge")
        fig, ax = plt.subplots(figsize=(8, 2.5))
        ax.barh(["Risk"], [prob], color=risk_color, height=0.6, edgecolor="black")
        ax.barh(
            ["Risk"], [1 - prob], left=[prob],
            color="#E0E0E0", height=0.6, edgecolor="black",
        )
        ax.set_xlim(0, 1)
        ax.axvline(x=optimal_threshold, color="black", linestyle="--", lw=1.5)
        ax.text(
            optimal_threshold, -0.45,
            f"Threshold\n({optimal_threshold:.2f})",
            ha="center", fontsize=9, style="italic",
        )
        txt_c = "white" if prob > 0.15 else "black"
        ax.text(
            prob / 2, 0, f"{prob:.0%}",
            ha="center", va="center", fontweight="bold", fontsize=18, color=txt_c,
        )
        ax.set_xlabel("Predicted Probability of Readmission")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_features:
        st.subheader("Feature Profile vs Population")
        top_feats = [
            f for f in pfi_df["feature"].head(10).tolist() if f in pop_stats.index
        ][:6]

        feat_z, feat_labels, feat_colors = [], [], []
        for feat in top_feats:
            pat_val = raw_numeric.get(feat, 0)
            p_mean = pop_stats.loc[feat, "mean"]
            p_std = pop_stats.loc[feat, "std"]
            z = (pat_val - p_mean) / p_std if p_std > 0 else 0
            feat_z.append(z)
            feat_labels.append(feat.replace("_", " ").title())
            feat_colors.append(
                "#FF1744" if z > 0.5 else "#2196F3" if z < -0.5 else "#9E9E9E"
            )

        fig, ax = plt.subplots(figsize=(8, 3.5))
        ax.barh(
            feat_labels[::-1], feat_z[::-1],
            color=feat_colors[::-1], edgecolor="black", alpha=0.85,
        )
        ax.axvline(x=0, color="black", lw=1)
        ax.set_xlabel("Standard deviations from population average")
        red_p = mpatches.Patch(color="#FF1744", label="Above average")
        blue_p = mpatches.Patch(color="#2196F3", label="Below average")
        gray_p = mpatches.Patch(color="#9E9E9E", label="Near average")
        ax.legend(handles=[red_p, blue_p, gray_p], fontsize=8, loc="lower right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Contributing features table
    st.subheader("Top Contributing Features")
    contrib_rows = []
    for feat in top_feats:
        pat_val = raw_numeric.get(feat, 0)
        p_mean = pop_stats.loc[feat, "mean"]
        p_std = pop_stats.loc[feat, "std"]
        z = (pat_val - p_mean) / p_std if p_std > 0 else 0
        if z > 0.5:
            status = "\u2B06\uFE0F Above Avg"
        elif z < -0.5:
            status = "\u2B07\uFE0F Below Avg"
        else:
            status = "\u27A1\uFE0F Normal"
        contrib_rows.append(
            {
                "Feature": feat.replace("_", " ").title(),
                "Patient Value": f"{pat_val:.1f}",
                "Population Average": f"{p_mean:.1f}",
                "Status": status,
            }
        )
    st.table(pd.DataFrame(contrib_rows))

    # Clinical alert
    st.markdown("---")
    if prob >= 0.30:
        st.error(
            "\u26A0\uFE0F **Clinical Alert:** This patient is at **HIGH** risk of "
            "readmission within 30 days. Consider enhanced discharge planning, "
            "follow-up scheduling within 7 days, and medication reconciliation."
        )
    elif prob >= optimal_threshold:
        st.warning(
            "\u2139\uFE0F **Clinical Note:** This patient has **MODERATE** readmission "
            "risk. Standard follow-up protocols recommended with attention to the "
            "contributing factors above."
        )
    else:
        st.success(
            "\u2705 **Clinical Note:** This patient is at **LOW** risk of "
            "readmission. Standard discharge procedures are appropriate."
        )

# ──────────────────────────────────────────────────────────────
# TAB 2 — EXPLAINABILITY & WHAT-IF
# ──────────────────────────────────────────────────────────────
with tab2:
    col_pfi, col_whatif = st.columns([1, 1])

    # --- PFI ---
    with col_pfi:
        st.subheader("Permutation Feature Importance (Global)")
        st.markdown(
            "*Which features matter most for the model's predictions "
            "across **all** patients?*"
        )
        top_n = 15
        top_pfi = pfi_df.head(top_n)

        fig, ax = plt.subplots(figsize=(8, 7))
        ax.barh(
            top_pfi["feature"][::-1].str.replace("_", " ").str.title(),
            top_pfi["importance_mean"][::-1],
            xerr=top_pfi["importance_std"][::-1],
            color="#1565C0", edgecolor="black", alpha=0.85, capsize=3,
        )
        ax.set_xlabel("Mean decrease in ROC-AUC when feature is shuffled")
        ax.set_title(f"Top {top_n} Most Important Features", fontweight="bold")
        ax.grid(True, alpha=0.3, axis="x")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # --- What-If Analysis ---
    with col_whatif:
        st.subheader("What-If Analysis (Patient-Specific)")
        st.markdown(
            "*How does changing **one** feature affect **this** patient's risk? "
            "Select a feature and see the effect in real time.*"
        )

        numeric_feats = [
            f for f in pfi_df["feature"].head(10).tolist()
            if f in pop_stats.index and f in feature_names
        ]
        selected_feat = st.selectbox(
            "Select a feature to explore:",
            numeric_feats,
            format_func=lambda x: x.replace("_", " ").title(),
        )

        if selected_feat:
            f_min = float(pop_stats.loc[selected_feat, "min"])
            f_max = float(pop_stats.loc[selected_feat, "max"])
            sweep_vals = np.linspace(f_min, f_max, 50)
            sweep_probs = []

            for val in sweep_vals:
                mod = raw_numeric.copy()
                mod[selected_feat] = val
                if selected_feat in (
                    "number_inpatient", "number_outpatient", "number_emergency"
                ):
                    mod["total_visits"] = (
                        mod.get("number_outpatient", 0)
                        + mod.get("number_emergency", 0)
                        + mod.get("number_inpatient", 0)
                    )

                enc = pd.DataFrame(0, index=[0], columns=feature_names, dtype=float)
                for c, v in mod.items():
                    if c in feature_names:
                        enc[c] = v
                for c, v in {
                    "race": "Caucasian", "gender": "Female",
                    "diag_1": "Circulatory", "diag_2": "Circulatory",
                    "diag_3": "Other",
                }.items():
                    dc = f"{c}_{v}"
                    if dc in feature_names:
                        enc[dc] = 1
                scaled = pd.DataFrame(
                    scaler.transform(enc), columns=feature_names
                )
                sweep_probs.append(float(model.predict_proba(scaled)[0, 1]))

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(sweep_vals, sweep_probs, color="#1565C0", lw=2.5)
            ax.axhline(
                y=optimal_threshold, color="gray", linestyle="--", lw=1,
                alpha=0.7, label=f"Threshold ({optimal_threshold:.2f})",
            )
            current_val = raw_numeric.get(selected_feat, 0)
            ax.axvline(
                x=current_val, color="#FF1744", linestyle="--", lw=2,
                label=f"Current patient ({current_val:.0f})",
            )
            ax.fill_between(sweep_vals, sweep_probs, alpha=0.08, color="#1565C0")
            ax.set_xlabel(selected_feat.replace("_", " ").title(), fontsize=12)
            ax.set_ylabel("Predicted Readmission Probability", fontsize=12)
            ax.set_title(
                f'What-If: How does "{selected_feat.replace("_", " ")}" '
                f"affect this patient's risk?",
                fontsize=13, fontweight="bold",
            )
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.info(
                f"**Interpretation:** Moving this patient's "
                f"*{selected_feat.replace('_', ' ')}* from its current value of "
                f"**{current_val:.0f}** shows how the readmission probability "
                f"changes while holding all other features constant. "
                f"This helps clinicians understand which interventions could "
                f"most effectively reduce readmission risk."
            )

    st.markdown("---")
    st.subheader("Understanding the Explainability Methods")

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        st.markdown("""
**Permutation Feature Importance (PFI)**
- Measures how much the model's accuracy drops when a feature is randomly shuffled
- A large drop means the feature is critical for predictions
- Applied on the held-out test set for unbiased estimates
- Higher bars = more important features
        """)
    with col_e2:
        st.markdown("""
**What-If Analysis (Local Sensitivity)**
- Shows how changing one feature affects **this specific patient's** prediction
- Keeps all other features constant (ceteris paribus)
- The red dashed line marks the current patient's value
- Steep curves = the feature has a strong effect on this patient's risk
        """)

# ──────────────────────────────────────────────────────────────
# TAB 3 — MODEL PERFORMANCE
# ──────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Model Selection Summary")
    st.markdown(
        f"**Selected Model:** {config['best_model_name']} \u2014 chosen for "
        f"highest Test ROC-AUC ({config['test_roc_auc']:.4f}) and "
        f"cross-validation stability."
    )

    if "model_results" in config:
        res_df = pd.DataFrame(config["model_results"]).T
        res_df.columns = [c.replace("_", " ").title() for c in res_df.columns]
        st.dataframe(
            res_df.style.highlight_max(axis=0, color="#C8E6C9").format("{:.4f}"),
            use_container_width=True,
        )

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown(f"""
**Dataset:** 101,766 encounters from 130 US hospitals
**Target:** Readmitted within 30 days (11.4% positive rate)
**Imbalance handling:** SMOTE on training data only
**Split:** 80% train / 20% test (stratified)
**Threshold:** Optimized from 0.50 \u2192 {optimal_threshold:.2f} for max F1
        """)
    with col_i2:
        st.markdown("""
**Models compared:**
- Logistic Regression (linear baseline)
- Random Forest (bagging ensemble)
- XGBoost (boosting ensemble)

**Evaluation metrics:** Accuracy, Precision, Recall, F1, ROC-AUC
**Explainability:** PFI + PDP + What-If Analysis
        """)

    st.markdown("---")
    st.caption(
        "Note: The binary prediction uses two values \u2014 0 (not readmitted) "
        "and 1 (readmitted within 30 days). The predicted probability shows how "
        "strongly the model believes this outcome for the current hospital visit. "
        "The contributing features explain which factors influenced the decision. "
        "This output reflects a risk assessment for one visit only and does not "
        "represent a permanent patient status."
    )

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown(
    '<div style="text-align:center; color:#9E9E9E; font-size:0.85rem;">'
    "CS 719 \u2014 Data Scientist Assistant | "
    "Diabetes 130-US Hospitals Dataset | "
    "Explainable AI for Healthcare"
    "</div>",
    unsafe_allow_html=True,
)
