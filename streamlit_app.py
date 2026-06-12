# Hospital Readmission Risk Assessment Dashboard
# by Raj Panchal

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import json
import joblib

# page config
st.set_page_config(
    page_title="Hospital Readmission Risk Assessment",
    page_icon="\U0001F3E5",
    layout="wide",
    initial_sidebar_state="expanded",
)

# custom CSS
st.markdown("""<style>
    .main-header {
        font-size: 3rem; font-weight: 800; color: #FFFFFF;
        text-align: center; padding: 1rem 0 0.3rem 0;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.05rem; color: #607D8B;
        text-align: center; margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    .risk-high {
        background: linear-gradient(135deg, #FFCDD2 0%, #EF9A9A 100%);
        color: #B71C1C; padding: 1.4rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #EF9A9A;
        box-shadow: 0 2px 8px rgba(183,28,28,0.15);
    }
    .risk-medium {
        background: linear-gradient(135deg, #FFE0B2 0%, #FFCC80 100%);
        color: #E65100; padding: 1.4rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #FFCC80;
        box-shadow: 0 2px 8px rgba(230,81,0,0.15);
    }
    .risk-low {
        background: linear-gradient(135deg, #C8E6C9 0%, #A5D6A7 100%);
        color: #1B5E20; padding: 1.4rem; border-radius: 12px;
        text-align: center; font-size: 1.6rem; font-weight: bold;
        border: 2px solid #A5D6A7;
        box-shadow: 0 2px 8px rgba(27,94,32,0.15);
    }
    .impact-card {
        background: #F5F5F5; border-radius: 10px;
        padding: 1.2rem; margin: 0.5rem 0;
        border-left: 4px solid #1565C0;
    }
    .compare-card {
        background: #FAFAFA; border-radius: 12px;
        padding: 1.5rem; border: 1px solid #E0E0E0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .compare-header-lace {
        font-size: 1.2rem; font-weight: 700; color: #795548;
        text-align: center; margin-bottom: 0.8rem;
        padding-bottom: 0.5rem; border-bottom: 2px solid #BCAAA4;
    }
    .compare-header-ai {
        font-size: 1.2rem; font-weight: 700; color: #0D47A1;
        text-align: center; margin-bottom: 0.8rem;
        padding-bottom: 0.5rem; border-bottom: 2px solid #64B5F6;
    }
    .lace-score-box {
        background: linear-gradient(135deg, #EFEBE9 0%, #D7CCC8 100%);
        border-radius: 10px; padding: 1rem; text-align: center;
        border: 1px solid #BCAAA4; margin: 0.5rem 0;
    }
    .ai-score-box {
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        border-radius: 10px; padding: 1rem; text-align: center;
        border: 1px solid #64B5F6; margin: 0.5rem 0;
    }
    .verdict-box {
        background: #F5F5F5;
        border-radius: 12px; padding: 1.2rem; text-align: center;
        border: 2px solid #1565C0; margin-top: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        color: #212121;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 1.5rem; }
    .stTabs [data-baseweb="tab"] { font-size: 1.05rem; }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F7FA 0%, #E8EDF2 100%);
    }
    div[data-testid="stSidebar"] h1, div[data-testid="stSidebar"] h2 {
        color: #0D47A1;
    }
</style>""", unsafe_allow_html=True)

# load model artifacts
@st.cache_resource
def load_artifacts():
    model = joblib.load("model_artifacts/model.joblib")
    scaler = joblib.load("model_artifacts/scaler.joblib")
    with open("model_artifacts/feature_names.json") as f:
        feature_names = json.load(f)
    pfi_df = pd.read_csv("model_artifacts/pfi_results.csv")
    pop_stats = pd.read_csv("model_artifacts/population_stats.csv", index_col=0)
    with open("model_artifacts/config.json") as f:
        config = json.load(f)
    return model, scaler, feature_names, pfi_df, pop_stats, config

try:
    model, scaler, feature_names, pfi_df, pop_stats, config = load_artifacts()
    optimal_threshold = config["optimal_threshold"]
except Exception as e:
    st.error(f"Could not load model artifacts. Run the notebook first.\n\nError: {e}")
    st.stop()

# header
st.markdown(
    '<div class="main-header">\U0001F3E5 Hospital Readmission Risk Assessment</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    "Predictive Analytics & Explainable AI for Clinical Decision Support<br>"
    "Raj Panchal"
    "</div>",
    unsafe_allow_html=True,
)
st.markdown("---")

# sidebar: patient inputs
with st.sidebar:
    st.header("\U0001F9D1\u200D\u2695\uFE0F Patient Parameters")
    st.markdown("Adjust sliders to assess readmission risk for a patient encounter.")
    st.markdown("---")

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
    diag_category = st.selectbox(
        "Primary Diagnosis Category",
        options=["Circulatory", "Diabetes", "Respiratory", "Digestive",
                 "Genitourinary", "Neoplasms", "Musculoskeletal", "Injury", "Other"],
        index=0,
        help="Primary diagnosis type. Affects model prediction and LACE comorbidity score.",
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


# prediction engine
def build_feature_vector():
    """Assemble raw patient inputs into the model's feature space."""
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
        "race": "Caucasian", "gender": "Female",
        "diag_1": diag_category, "diag_2": "Circulatory", "diag_3": "Other",
    }
    return raw_numeric, categorical


def encode_and_predict(raw_numeric, categorical):
    """Encode inputs, scale, predict probability."""
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
    return prob


raw_numeric, categorical = build_feature_vector()
prob = encode_and_predict(raw_numeric, categorical)
pred = int(prob >= optimal_threshold)

if prob >= 0.30:
    risk, risk_color = "HIGH RISK", "#FF1744"
elif prob >= optimal_threshold:
    risk, risk_color = "MEDIUM RISK", "#FF9100"
else:
    risk, risk_color = "LOW RISK", "#00C853"

# compute feature contributions
# Exclude ID-coded categoricals (z-scores are meaningless for them)
categorical_coded = {"admission_type_id", "discharge_disposition_id", "admission_source_id"}
top_feats = [
    f for f in pfi_df["feature"].head(15).tolist()
    if f in pop_stats.index and f not in categorical_coded
][:8]
pfi_lookup = dict(zip(pfi_df["feature"], pfi_df["importance_mean"]))

contributions = []
for feat in top_feats:
    pat_val = raw_numeric.get(feat, 0)
    p_mean = float(pop_stats.loc[feat, "mean"])
    p_std = float(pop_stats.loc[feat, "std"])
    z = (pat_val - p_mean) / p_std if p_std > 0 else 0.0
    imp = pfi_lookup.get(feat, 0)
    contrib = z * imp
    contributions.append({
        "feature": feat,
        "patient_val": pat_val,
        "pop_mean": p_mean,
        "z_score": z,
        "importance": imp,
        "contribution": contrib,
    })
contrib_df = pd.DataFrame(contributions).sort_values("contribution", key=abs, ascending=True)

# tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "\U0001FA7A Risk Assessment",
    "\U0001F50D Explainability & What-If",
    "\U0001F4C8 Clinical Impact",
    "\u2699\uFE0F Model Performance",
])

# TAB 1: Risk Assessment
with tab1:
    # top metrics
    c1, c2, c3 = st.columns(3)
    with c1:
        css_cls = "risk-high" if prob >= 0.30 else ("risk-medium" if prob >= optimal_threshold else "risk-low")
        st.markdown(f'<div class="{css_cls}">{risk}</div>', unsafe_allow_html=True)
    with c2:
        st.metric("Readmission Probability", f"{prob:.0%}",
                  delta=f"{prob - 0.114:+.0%} vs baseline (11.4%)", delta_color="inverse")
    with c3:
        st.metric("Binary Prediction",
                  "Readmitted" if pred else "Not Readmitted",
                  delta=f"Threshold: {optimal_threshold:.2f}")

    st.markdown("---")

    # risk gauge + why this prediction
    col_gauge, col_why = st.columns([1, 1])

    with col_gauge:
        st.subheader("Risk Gauge")
        fig, ax = plt.subplots(figsize=(8, 2.5))
        ax.barh(["Risk"], [prob], color=risk_color, height=0.6, edgecolor="black")
        ax.barh(["Risk"], [1 - prob], left=[prob], color="#E0E0E0", height=0.6, edgecolor="black")
        ax.set_xlim(0, 1)
        ax.axvline(x=optimal_threshold, color="black", linestyle="--", lw=1.5)
        ax.text(optimal_threshold, -0.45, f"Threshold\n({optimal_threshold:.2f})",
                ha="center", fontsize=9, style="italic")
        txt_c = "white" if prob > 0.20 else "black"
        ax.text(prob / 2, 0, f"{prob:.0%}", ha="center", va="center",
                fontweight="bold", fontsize=18, color=txt_c)
        ax.set_xlabel("Predicted Probability of Readmission")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_why:
        st.subheader("Why This Prediction?")
        # waterfall-style bar chart of feature contributions
        colors = ["#EF5350" if v > 0 else "#42A5F5" for v in contrib_df["contribution"]]
        fig, ax = plt.subplots(figsize=(8, 4))
        labels = [f.replace("_", " ").title() for f in contrib_df["feature"]]
        vals = contrib_df["contribution"].values
        ax.barh(labels, vals, color=colors, edgecolor="black", alpha=0.85)
        ax.axvline(x=0, color="black", lw=1)
        ax.set_xlabel("Contribution to Risk (positive = increases risk)")
        red_p = mpatches.Patch(color="#EF5350", label="Increases risk")
        blue_p = mpatches.Patch(color="#42A5F5", label="Decreases risk")
        ax.legend(handles=[red_p, blue_p], fontsize=8, loc="lower right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # feature profile table
    st.markdown("---")
    st.subheader("Patient Feature Profile")
    profile_rows = []
    for feat in top_feats:
        pat_val = raw_numeric.get(feat, 0)
        p_mean = float(pop_stats.loc[feat, "mean"])
        p_std = float(pop_stats.loc[feat, "std"])
        z = (pat_val - p_mean) / p_std if p_std > 0 else 0
        if z > 0.5:
            status = "\u2B06\uFE0F Above Avg"
        elif z < -0.5:
            status = "\u2B07\uFE0F Below Avg"
        else:
            status = "\u27A1\uFE0F Normal"
        profile_rows.append({
            "Feature": feat.replace("_", " ").title(),
            "Patient": f"{pat_val:.1f}",
            "Population Avg": f"{p_mean:.1f}",
            "Status": status,
        })
    st.table(pd.DataFrame(profile_rows))

    # clinical action plan
    st.markdown("---")
    st.subheader("Clinical Action Plan")
    if prob >= 0.30:
        st.error("\u26A0\uFE0F **HIGH RISK** \u2014 Enhanced discharge protocol recommended")
    elif prob >= optimal_threshold:
        st.warning("\u2139\uFE0F **MODERATE RISK** \u2014 Follow-up recommended with attention to key risk drivers")
    else:
        st.success("\u2705 **LOW RISK** \u2014 Standard discharge procedures appropriate")

    # specific actions based on which features are driving risk
    actions = []
    if raw_numeric.get("number_inpatient", 0) >= 1:
        actions.append("\U0001F3E5 **Prior hospitalizations detected** \u2014 Schedule a follow-up call within 7 days of discharge")
    if discharge_disposition_id in [2, 3, 4, 5]:
        actions.append("\U0001F6CF\uFE0F **Non-home discharge** \u2014 Coordinate care transition with the receiving facility")
    if num_medications >= 20:
        actions.append("\U0001F48A **Polypharmacy (20+ medications)** \u2014 Request pharmacist-led medication reconciliation")
    if time_in_hospital >= 7:
        actions.append("\u23F0 **Extended stay (7+ days)** \u2014 Assess care transition readiness before discharge")
    if number_emergency >= 2:
        actions.append("\U0001F6A8 **Repeat ER visits** \u2014 Evaluate outpatient support and chronic disease management")
    if number_diagnoses >= 9:
        actions.append("\U0001F4CB **High diagnostic complexity** \u2014 Consider multidisciplinary care coordination")

    if not actions:
        actions.append("\u2705 No specific risk drivers flagged \u2014 Standard discharge pathway is appropriate")

    for a in actions:
        st.markdown(f"- {a}")

# TAB 2: Explainability & What-If
with tab2:
    col_pfi, col_whatif = st.columns([1, 1])

    # global feature importance
    with col_pfi:
        st.subheader("Global Feature Importance")
        st.markdown("*Which features matter most across all patients?*")
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
        ax.set_title(f"Top {top_n} Features (Permutation Importance)", fontweight="bold")
        ax.grid(True, alpha=0.3, axis="x")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # what-if analysis
    with col_whatif:
        st.subheader("What-If Analysis")
        st.markdown("*How does changing one feature affect this patient's risk?*")

        numeric_feats = [
            f for f in pfi_df["feature"].head(15).tolist()
            if f in pop_stats.index and f in feature_names and f not in categorical_coded
        ]
        selected_feat = st.selectbox(
            "Select a feature:", numeric_feats,
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
                if selected_feat in ("number_inpatient", "number_outpatient", "number_emergency"):
                    mod["total_visits"] = (
                        mod.get("number_outpatient", 0)
                        + mod.get("number_emergency", 0)
                        + mod.get("number_inpatient", 0)
                    )
                sweep_probs.append(encode_and_predict(mod, categorical))

            fig, ax = plt.subplots(figsize=(8, 5))
            ax.plot(sweep_vals, sweep_probs, color="#1565C0", lw=2.5)
            ax.axhline(y=optimal_threshold, color="gray", linestyle="--", lw=1,
                       alpha=0.7, label=f"Threshold ({optimal_threshold:.2f})")
            current_val = raw_numeric.get(selected_feat, 0)
            ax.axvline(x=current_val, color="#FF1744", linestyle="--", lw=2,
                       label=f"Current ({current_val:.0f})")
            ax.fill_between(sweep_vals, sweep_probs, alpha=0.08, color="#1565C0")
            ax.set_xlabel(selected_feat.replace("_", " ").title(), fontsize=12)
            ax.set_ylabel("Readmission Probability", fontsize=12)
            ax.set_title(f'Effect of {selected_feat.replace("_", " ")} on risk', fontweight="bold")
            ax.legend(fontsize=10)
            ax.grid(True, alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

    # scenario comparison
    st.markdown("---")
    st.subheader("Scenario Comparison")
    st.markdown("*Pick a feature, set a hypothetical value, and see how the risk changes.*")

    sc1, sc2, sc3 = st.columns([1, 1, 1])
    with sc1:
        scenario_feat = st.selectbox(
            "Feature to change:", numeric_feats, key="scenario_feat",
            format_func=lambda x: x.replace("_", " ").title(),
        )
    with sc2:
        s_min = float(pop_stats.loc[scenario_feat, "min"])
        s_max = float(pop_stats.loc[scenario_feat, "max"])
        current = raw_numeric.get(scenario_feat, 0)
        hypo_val = st.slider(
            f"Hypothetical value", min_value=int(s_min), max_value=int(s_max),
            value=int(current), key="hypo_val",
        )

    # compute hypothetical risk
    hypo_numeric = raw_numeric.copy()
    hypo_numeric[scenario_feat] = hypo_val
    if scenario_feat in ("number_inpatient", "number_outpatient", "number_emergency"):
        hypo_numeric["total_visits"] = (
            hypo_numeric.get("number_outpatient", 0)
            + hypo_numeric.get("number_emergency", 0)
            + hypo_numeric.get("number_inpatient", 0)
        )
    hypo_prob = encode_and_predict(hypo_numeric, categorical)
    delta = hypo_prob - prob

    with sc3:
        st.metric(
            "Risk Change",
            f"{hypo_prob:.0%}",
            delta=f"{delta:+.1%} from current ({prob:.0%})",
            delta_color="inverse",
        )

    if abs(delta) > 0.005:
        direction = "increases" if delta > 0 else "decreases"
        st.info(
            f"Changing **{scenario_feat.replace('_', ' ')}** from "
            f"**{current:.0f}** to **{hypo_val}** {direction} readmission risk "
            f"from **{prob:.0%}** to **{hypo_prob:.0%}** ({delta:+.1%})."
        )
    else:
        st.info("Minimal change in risk for this adjustment.")

    # method explanations
    st.markdown("---")
    ce1, ce2 = st.columns(2)
    with ce1:
        st.markdown("""
**Permutation Feature Importance (PFI)**
- Shuffles each feature and measures the drop in model accuracy
- Bigger drop = more important feature
- Computed on the held-out test set for unbiased results
""")
    with ce2:
        st.markdown("""
**What-If / Scenario Analysis**
- Shows how one feature affects this patient's prediction
- All other features held constant
- Steep curves = strong influence on this patient's risk
""")

# TAB 3: Clinical Impact
with tab3:
    st.subheader("Why This Model Matters")
    st.markdown(
        "Hospital readmissions cost the US healthcare system over **$26 billion annually**. "
        "CMS penalizes hospitals with excess readmission rates. Here's how this AI-based "
        "approach compares to traditional methods and what impact it can have."
    )
    st.markdown("---")

    # threshold comparison
    st.subheader("Threshold Optimization: The 9x Improvement")
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        st.markdown('<div class="impact-card">', unsafe_allow_html=True)
        st.metric("Default Threshold (0.50)", "~4% Recall",
                  delta="Misses 96% of readmissions", delta_color="inverse")
        st.markdown("</div>", unsafe_allow_html=True)
    with tc2:
        st.markdown('<div class="impact-card">', unsafe_allow_html=True)
        st.metric("Optimized Threshold (0.20)", "~35% Recall",
                  delta="9x improvement", delta_color="normal")
        st.markdown("</div>", unsafe_allow_html=True)
    with tc3:
        st.markdown('<div class="impact-card">', unsafe_allow_html=True)
        st.metric("Recall Gain", "+31 percentage points",
                  delta="From 4% to 35%", delta_color="normal")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "By lowering the classification threshold from 0.50 to 0.20, we trade a small "
        "amount of precision for a significant gain in recall. In healthcare, **missing a "
        "readmission is far more costly than a false alarm**. A flagged patient just "
        "gets extra follow-up, while a missed one may end up back in the ER."
    )

    st.markdown("---")

    # LACE vs AI comparison
    st.subheader("LACE Index vs. This AI Model")
    lace_col, ai_col = st.columns(2)
    with lace_col:
        st.markdown("#### LACE Index (Traditional)")
        st.markdown("""
| Aspect | LACE |
|--------|------|
| **Method** | Rule-based point scoring |
| **Inputs** | Length of stay, Acuity, Comorbidities, ED visits |
| **Output** | Single score (0\u201319) |
| **Personalization** | None \u2014 fixed weights |
| **Explainability** | Limited \u2014 just a total score |
| **Threshold** | Fixed cutoff, no probability |
| **Adaptability** | Cannot learn from new data |
        """)

    with ai_col:
        st.markdown("#### This XGBoost Model")
        st.markdown(f"""
| Aspect | Our Model |
|--------|-----------|
| **Method** | Gradient-boosted decision trees |
| **Inputs** | 46 features (clinical + demographic) |
| **Output** | Probability (0\u2013100%) |
| **Personalization** | Learns complex, non-linear patient patterns |
| **Explainability** | PFI + PDP + What-If analysis per patient |
| **Threshold** | Optimized ({optimal_threshold:.2f}), tunable per hospital |
| **Adaptability** | Retrainable as new data arrives |
        """)

    # LACE vs AI: live side-by-side comparison
    st.markdown("---")
    st.subheader("Live Comparison: This Patient")
    st.markdown("*Same patient inputs evaluated by both methods side by side.*")

    # compute LACE score from current patient inputs
    def approx_cci(d1, d2, d3):
        # CCI weights matching standard Charlson index conditions
        weights = {"Diabetes": 1, "Neoplasms": 2, "Respiratory": 1,
                   "Genitourinary": 1, "Circulatory": 1}
        return min(sum(weights.get(d, 0) for d in [d1, d2, d3]), 5)

    def compute_lace(los, admission_type, diag_1_cat, diag_2_cat, diag_3_cat, n_emergency):
        # L: Length of Stay
        if los < 1:       l_score = 0
        elif los == 1:    l_score = 1
        elif los == 2:    l_score = 2
        elif los == 3:    l_score = 3
        elif los <= 6:    l_score = 4
        elif los <= 13:   l_score = 5
        else:             l_score = 7

        # A: Acuity of Admission
        a_score = 3 if admission_type == 1 else 0

        # C: Comorbidity via approximate CCI from diagnosis categories
        cci = approx_cci(diag_1_cat, diag_2_cat, diag_3_cat)
        if cci == 0:   c_score = 0
        elif cci == 1: c_score = 1
        elif cci == 2: c_score = 2
        elif cci == 3: c_score = 3
        else:          c_score = 5

        # E: Emergency Department visits (prior 6 months)
        e_score = min(n_emergency, 4)

        total = l_score + a_score + c_score + e_score
        return total, l_score, a_score, c_score, e_score

    lace_total, l_sc, a_sc, c_sc, e_sc = compute_lace(
        time_in_hospital, admission_type_id,
        categorical["diag_1"], categorical["diag_2"], categorical["diag_3"],
        number_emergency,
    )
    lace_risk = "High Risk" if lace_total >= 10 else "Low Risk"

    lc1, lc2 = st.columns(2)

    with lc1:
        st.markdown('<div class="compare-card">', unsafe_allow_html=True)
        st.markdown('<div class="compare-header-lace">LACE Index</div>', unsafe_allow_html=True)

        st.markdown(f"""
| Component | Input | Score |
|-----------|-------|-------|
| **L**: Length of Stay | {time_in_hospital} days | {l_sc} |
| **A**: Acuity (Emergency) | {"Yes" if admission_type_id == 1 else "No"} | {a_sc} |
| **C**: Comorbidity (CCI) | {categorical["diag_1"]} | {c_sc} |
| **E**: ED Visits | {number_emergency} visits | {e_sc} |
        """)

        lace_color = "#B71C1C" if lace_total >= 10 else "#1B5E20"
        st.markdown(
            f'<div class="lace-score-box">'
            f'<span style="font-size:2.2rem;font-weight:800;color:{lace_color};">{lace_total}</span>'
            f'<span style="font-size:1rem;color:#795548;"> / 19</span><br>'
            f'<span style="font-size:1.1rem;font-weight:600;color:{lace_color};">{lace_risk}</span><br>'
            f'<span style="font-size:0.8rem;color:#9E9E9E;">Threshold: 10+</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#9E9E9E;font-size:0.85rem;text-align:center;margin-top:0.5rem;">'
            'No probability estimate. No feature-level explanation.<br>'
            'Fixed weights, cannot adapt to new data.</p>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with lc2:
        st.markdown('<div class="compare-card">', unsafe_allow_html=True)
        st.markdown('<div class="compare-header-ai">XGBoost AI Model</div>', unsafe_allow_html=True)

        # top 4 contributing features for this patient
        top4 = contrib_df.tail(4)
        feat_rows = ""
        for _, row in top4.iterrows():
            direction = "+" if row["contribution"] > 0 else "-"
            feat_rows += f"| **{row['feature'].replace('_', ' ').title()}** | {row['patient_val']:.0f} | {direction} |\n"

        st.markdown(f"""
| Top Feature | Value | Effect |
|-------------|-------|--------|
{feat_rows}        """)

        ai_color = risk_color
        st.markdown(
            f'<div class="ai-score-box">'
            f'<span style="font-size:2.2rem;font-weight:800;color:{ai_color};">{prob:.0%}</span><br>'
            f'<span style="font-size:1.1rem;font-weight:600;color:{ai_color};">{risk}</span><br>'
            f'<span style="font-size:0.8rem;color:#9E9E9E;">Threshold: {optimal_threshold:.2f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<p style="color:#9E9E9E;font-size:0.85rem;text-align:center;margin-top:0.5rem;">'
            'Calibrated probability. Feature-level explanations.<br>'
            'What-If analysis. Retrainable on new data.</p>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # verdict
    if lace_total < 10 and prob >= optimal_threshold:
        verdict_text = (
            "LACE classifies this patient as <b>Low Risk</b>, but our model detects a "
            f"<b>{prob:.0%} readmission probability ({risk})</b>. "
            "The AI model captures risk factors that LACE's fixed scoring misses."
        )
    elif lace_total >= 10 and prob < optimal_threshold:
        verdict_text = (
            f"LACE flags this patient as <b>High Risk</b> (score {lace_total}), "
            f"but our model estimates only <b>{prob:.0%} probability ({risk})</b>. "
            "The AI model's richer feature set provides a more nuanced assessment."
        )
    elif lace_total >= 10 and prob >= optimal_threshold:
        verdict_text = (
            f"Both methods agree this patient is <b>at risk</b>. "
            f"But our model goes further: it quantifies the risk at <b>{prob:.0%}</b> "
            f"and explains <i>which factors</i> are driving it."
        )
    else:
        verdict_text = (
            f"Both methods agree this patient is <b>lower risk</b>. "
            f"Our model provides additional confidence with a precise <b>{prob:.0%}</b> estimate "
            f"and a full feature-level breakdown."
        )

    st.markdown(
        f'<div class="verdict-box">'
        f'<span style="font-size:1.1rem;">{verdict_text}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # cost savings estimate
    st.subheader("Estimated Cost Savings")
    st.markdown("Based on published readmission cost data (CMS, AHRQ):")

    cs1, cs2 = st.columns([1, 1])
    with cs1:
        annual_discharges = st.number_input(
            "Annual discharges at your hospital",
            min_value=100, max_value=50000, value=5000, step=100
        )
        readmit_rate = 0.114
        cost_per_readmit = st.number_input(
            "Average cost per readmission ($)",
            min_value=5000, max_value=50000, value=15000, step=1000
        )

    with cs2:
        total_readmits = int(annual_discharges * readmit_rate)
        caught = int(total_readmits * 0.35)
        # assume 30% of flagged patients avoid readmission through intervention
        prevented = int(caught * 0.30)
        savings = prevented * cost_per_readmit

        st.metric("Expected Readmissions / Year", f"{total_readmits:,}")
        st.metric("Flagged by Model (35% recall)", f"{caught:,}")
        st.metric("Prevented (est. 30% intervention success)", f"{prevented:,}")
        st.metric("Annual Savings", f"${savings:,.0f}")

    st.info(
        f"Even with a conservative 30% intervention success rate, a hospital with "
        f"{annual_discharges:,} discharges could prevent **{prevented}** "
        f"readmissions and save approximately **${savings:,.0f}** per year."
    )

# TAB 4: Model Performance
with tab4:
    st.subheader("Model Comparison")
    st.markdown(
        f"**Selected:** {config['best_model_name']} \u2014 highest Test ROC-AUC "
        f"({config['test_roc_auc']:.4f}) with stable cross-validation performance."
    )

    if "model_results" in config:
        res_df = pd.DataFrame(config["model_results"]).T
        res_df.columns = [c.replace("_", " ").title() for c in res_df.columns]
        st.dataframe(
            res_df.style.highlight_max(axis=0, props="background-color: #BBDEFB; color: #0D47A1; font-weight: bold").format("{:.4f}"),
            use_container_width=True,
        )

    st.markdown("---")
    mi1, mi2 = st.columns(2)
    with mi1:
        st.markdown(f"""
**Dataset:** 101,766 encounters from 130 US hospitals
**Target:** Readmitted within 30 days (11.4% positive rate)
**Imbalance:** SMOTE applied on training data only
**Split:** 80/20 stratified train-test split
**Tuning:** GridSearchCV (3-fold, ROC-AUC scoring)
**Threshold:** Optimized from 0.50 to {optimal_threshold:.2f}
        """)
    with mi2:
        st.markdown("""
**Models Trained:**
- Logistic Regression (linear baseline)
- Random Forest (bagging ensemble)
- XGBoost (boosting ensemble)

**Evaluation:** Accuracy, Precision, Recall, F1, ROC-AUC
**Explainability:** PFI + PDP + Patient-level What-If
        """)

    st.markdown("---")
    st.caption(
        "Note: Predictions reflect risk for a single hospital encounter, not a "
        "permanent patient status. The probability indicates how strongly the model "
        "associates the input features with readmission within 30 days."
    )

# footer
st.markdown("---")
st.markdown(
    '<div style="text-align:center; padding: 1rem 0;">'
    '<span style="color:#90A4AE; font-size:0.85rem;">'
    "Predictive Analytics & Explainable AI for Hospital Readmission Risk"
    "</span><br>"
    '<span style="color:#B0BEC5; font-size:0.78rem;">'
    "Raj Panchal"
    "</span><br>"
    '<span style="color:#CFD8DC; font-size:0.72rem;">'
    "Built with XGBoost, Streamlit & Python \u2014 "
    "Dataset: 101,766 patient encounters from 130 US hospitals"
    "</span>"
    "</div>",
    unsafe_allow_html=True,
)
