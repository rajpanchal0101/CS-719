"""
Data Science utility functions for the Diabetes 130-US Hospitals project.
Provides EDA, visualization, preprocessing, and model evaluation helpers.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    roc_auc_score,
    f1_score,
    ConfusionMatrixDisplay,
)


# ---------------------------------------------------------------------------
# 1. Data profiling
# ---------------------------------------------------------------------------

def profile(df: pd.DataFrame) -> pd.DataFrame:
    """Return a concise profile of every column in a DataFrame."""
    records = []
    for col in df.columns:
        s = df[col]
        rec = {
            "column": col,
            "dtype": str(s.dtype),
            "non_null": s.count(),
            "null_count": s.isna().sum(),
            "null_pct": round(s.isna().mean() * 100, 2),
            "unique": s.nunique(),
        }
        if pd.api.types.is_numeric_dtype(s):
            rec.update({
                "mean": round(s.mean(), 4),
                "std": round(s.std(), 4),
                "min": s.min(),
                "25%": s.quantile(0.25),
                "50%": s.quantile(0.50),
                "75%": s.quantile(0.75),
                "max": s.max(),
                "skew": round(s.skew(), 4),
                "kurtosis": round(s.kurtosis(), 4),
            })
        records.append(rec)
    return pd.DataFrame(records).set_index("column")


def detect_outliers_iqr(df: pd.DataFrame, factor: float = 1.5) -> pd.DataFrame:
    """Flag outliers using the IQR method for all numeric columns."""
    numeric = df.select_dtypes(include="number")
    q1 = numeric.quantile(0.25)
    q3 = numeric.quantile(0.75)
    iqr = q3 - q1
    return ((numeric < (q1 - factor * iqr)) | (numeric > (q3 + factor * iqr)))


# ---------------------------------------------------------------------------
# 2. Visualization helpers
# ---------------------------------------------------------------------------

def plot_distributions(df: pd.DataFrame, cols=None, figsize=(16, 4)):
    """Histogram + KDE for selected numeric columns."""
    if cols is None:
        cols = df.select_dtypes(include="number").columns.tolist()
    n = len(cols)
    if n == 0:
        print("No numeric columns to plot.")
        return
    rows = (n + 3) // 4
    fig, axes = plt.subplots(rows, min(n, 4), figsize=(figsize[0], figsize[1] * rows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i])
        axes[i].set_title(col)
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, figsize=(12, 10), annot=True):
    """Heatmap of Pearson correlations for numeric columns."""
    corr = df.select_dtypes(include="number").corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap="coolwarm", center=0, fmt=".2f",
                linewidths=0.5, annot_kws={"size": 7})
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()


def plot_categorical_counts(df: pd.DataFrame, cols=None, top_n=10,
                            figsize=(16, 4)):
    """Bar plots showing value counts for categorical columns."""
    if cols is None:
        cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    n = len(cols)
    if n == 0:
        print("No categorical columns to plot.")
        return
    rows = (n + 2) // 3
    fig, axes = plt.subplots(rows, min(n, 3),
                             figsize=(figsize[0], figsize[1] * rows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(cols):
        vc = df[col].value_counts().head(top_n)
        vc.plot.bar(ax=axes[i], color="steelblue")
        axes[i].set_title(col)
        axes[i].tick_params(axis='x', rotation=45)
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    plt.tight_layout()
    plt.show()


def plot_target_distribution(df: pd.DataFrame, target: str, figsize=(8, 5)):
    """Bar chart showing target variable class distribution."""
    vc = df[target].value_counts()
    colors = sns.color_palette("Set2", len(vc))
    ax = vc.plot.bar(color=colors, figsize=figsize, edgecolor="black")
    for i, (val, count) in enumerate(vc.items()):
        pct = count / len(df) * 100
        ax.text(i, count + len(df) * 0.005, f"{pct:.1f}%",
                ha='center', fontweight='bold')
    plt.title(f"Distribution of '{target}'")
    plt.ylabel("Count")
    plt.xlabel(target)
    plt.tight_layout()
    plt.show()


def plot_target_vs_features(df: pd.DataFrame, target: str,
                            cols=None, figsize=(16, 4)):
    """Box plots of numeric features grouped by target class."""
    if cols is None:
        cols = [c for c in df.select_dtypes(include="number").columns
                if c != target]
    n = len(cols)
    rows = (n + 2) // 3
    fig, axes = plt.subplots(rows, min(n, 3),
                             figsize=(figsize[0], figsize[1] * rows))
    axes = np.array(axes).flatten() if n > 1 else [axes]
    for i, col in enumerate(cols):
        sns.boxplot(data=df, x=target, y=col, ax=axes[i], palette="Set2")
        axes[i].set_title(f"{col} by {target}")
    for j in range(n, len(axes)):
        axes[j].set_visible(False)
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 3. Data cleaning helpers (Diabetes-specific)
# ---------------------------------------------------------------------------

def clean_diabetes_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the Diabetes 130-US Hospitals dataset.

    Steps:
      - Replace '?' with NaN
      - Drop columns with >40% missing or zero variance
      - Drop duplicate patient encounters (keep first)
      - Remove rows where discharge = expired/hospice
      - Map diagnosis codes to categories
    """
    df = df.copy()

    # Replace '?' with NaN
    df.replace('?', np.nan, inplace=True)

    # Drop columns with >40% missing values
    high_null_cols = [c for c in df.columns
                      if df[c].isna().mean() > 0.40]
    df.drop(columns=high_null_cols, inplace=True)
    print(f"Dropped high-null columns: {high_null_cols}")

    # Drop zero-variance columns
    zero_var = [c for c in df.columns if df[c].nunique() <= 1]
    df.drop(columns=zero_var, inplace=True)
    print(f"Dropped zero-variance columns: {zero_var}")

    # Drop encounter_id and patient_nbr (identifiers, not features)
    id_cols = [c for c in ['encounter_id', 'patient_nbr'] if c in df.columns]
    df.drop(columns=id_cols, inplace=True)

    # Remove rows where gender is Unknown/Invalid
    df = df[df['gender'] != 'Unknown/Invalid']

    # Remove expired / hospice patients (discharge_disposition_id in 11,13,14,19,20,21)
    expired_ids = [11, 13, 14, 19, 20, 21]
    df = df[~df['discharge_disposition_id'].isin(expired_ids)]
    print(f"Rows after removing expired/hospice: {len(df)}")

    df.reset_index(drop=True, inplace=True)
    return df


def map_diagnosis(code):
    """Map an ICD-9 diagnosis code to a clinical category."""
    if pd.isna(code):
        return "Other"
    code = str(code)
    if code.startswith("E") or code.startswith("V"):
        return "Other"
    try:
        num = float(code)
    except ValueError:
        return "Other"
    if 390 <= num <= 459 or num == 785:
        return "Circulatory"
    elif 460 <= num <= 519 or num == 786:
        return "Respiratory"
    elif 520 <= num <= 579 or num == 787:
        return "Digestive"
    elif 250 <= num < 251:
        return "Diabetes"
    elif 800 <= num <= 999:
        return "Injury"
    elif 710 <= num <= 739:
        return "Musculoskeletal"
    elif 580 <= num <= 629 or num == 788:
        return "Genitourinary"
    elif 140 <= num <= 239:
        return "Neoplasms"
    else:
        return "Other"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create derived features for the diabetes dataset."""
    df = df.copy()

    # Map diagnosis codes to clinical categories
    for diag_col in ['diag_1', 'diag_2', 'diag_3']:
        if diag_col in df.columns:
            df[diag_col] = df[diag_col].apply(map_diagnosis)

    # Total visits before this encounter
    df['total_visits'] = (df['number_outpatient']
                          + df['number_emergency']
                          + df['number_inpatient'])

    # Count of medications changed
    med_cols = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
                'glimepiride', 'glipizide', 'glyburide', 'pioglitazone',
                'rosiglitazone', 'insulin']
    existing_med_cols = [c for c in med_cols if c in df.columns]
    df['num_med_changed'] = df[existing_med_cols].apply(
        lambda row: sum(1 for v in row if v in ['Up', 'Down']), axis=1
    )
    df['num_med_active'] = df[existing_med_cols].apply(
        lambda row: sum(1 for v in row if v != 'No'), axis=1
    )

    # Binary: was any medication changed?
    df['change'] = (df['change'] == 'Ch').astype(int)

    # Binary: was diabetes medication prescribed?
    df['diabetesMed'] = (df['diabetesMed'] == 'Yes').astype(int)

    # Age midpoint (numeric)
    age_map = {
        '[0-10)': 5, '[10-20)': 15, '[20-30)': 25, '[30-40)': 35,
        '[40-50)': 45, '[50-60)': 55, '[60-70)': 65, '[70-80)': 75,
        '[80-90)': 85, '[90-100)': 95,
    }
    df['age_numeric'] = df['age'].map(age_map)

    # Encode A1Cresult and max_glu_serum as ordinal
    a1c_map = {'None': 0, 'Norm': 1, '>7': 2, '>8': 3}
    glu_map = {'None': 0, 'Norm': 1, '>200': 2, '>300': 3}
    if 'A1Cresult' in df.columns:
        df['A1Cresult'] = df['A1Cresult'].fillna('None').map(a1c_map).fillna(0).astype(int)
    if 'max_glu_serum' in df.columns:
        df['max_glu_serum'] = df['max_glu_serum'].fillna('None').map(glu_map).fillna(0).astype(int)

    return df


# ---------------------------------------------------------------------------
# 4. Preprocessing helpers
# ---------------------------------------------------------------------------

def encode_and_prepare(df: pd.DataFrame, target: str,
                       test_size: float = 0.2,
                       random_state: int = 42):
    """Encode categoricals, split data, and scale features.

    Returns: X_train, X_test, y_train, y_test, scaler, label_encoder
    """
    df = df.copy()

    # Encode target
    le_target = LabelEncoder()
    df[target] = le_target.fit_transform(df[target])

    # Separate features and target
    y = df[target]
    X = df.drop(columns=[target])

    # Drop remaining high-cardinality string columns
    cat_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    low_card = [c for c in cat_cols if X[c].nunique() <= 15]
    high_card = [c for c in cat_cols if X[c].nunique() > 15]
    if high_card:
        X.drop(columns=high_card, inplace=True)
        print(f"Dropped high-cardinality columns: {high_card}")

    # One-hot encode remaining categoricals
    X = pd.get_dummies(X, columns=low_card, drop_first=True, dtype=int)
    print(f"Final feature matrix shape: {X.shape}")

    # Train/test split (stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Scale numeric features
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train),
                           columns=X.columns, index=X_train.index)
    X_test = pd.DataFrame(scaler.transform(X_test),
                          columns=X.columns, index=X_test.index)

    return X_train, X_test, y_train, y_test, scaler, le_target


# ---------------------------------------------------------------------------
# 5. Model evaluation helpers
# ---------------------------------------------------------------------------

def evaluate_classifier(model, X_test, y_test, label_names=None):
    """Print classification report and plot confusion matrix."""
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=label_names))

    fig, ax = plt.subplots(figsize=(7, 6))
    ConfusionMatrixDisplay.from_predictions(
        y_test, y_pred, display_labels=label_names,
        cmap="Blues", ax=ax
    )
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    plt.show()

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    return {"accuracy": acc, "f1_weighted": f1}


def compare_models(results: dict, figsize=(10, 5)):
    """Bar chart comparing model metrics."""
    df_results = pd.DataFrame(results).T
    df_results.plot.bar(figsize=figsize, edgecolor='black', rot=0)
    plt.title("Model Comparison")
    plt.ylabel("Score")
    plt.ylim(0, 1)
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.show()
    return df_results


def quick_cross_val(model, X, y, cv=5, scoring="accuracy"):
    """Run stratified cross-validation and print summary statistics."""
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=skf, scoring=scoring)
    print(f"CV {scoring}: {scores.mean():.4f} (+/- {scores.std():.4f})")
    return scores


# ---------------------------------------------------------------------------
# 6. Statistical tests
# ---------------------------------------------------------------------------

def normality_test(series: pd.Series, alpha: float = 0.05):
    """Shapiro-Wilk test for normality (uses sample if > 5000 rows)."""
    sample = series.dropna()
    if len(sample) > 5000:
        sample = sample.sample(5000, random_state=42)
    stat, p = stats.shapiro(sample)
    result = "normal" if p > alpha else "not normal"
    print(f"Shapiro-Wilk: stat={stat:.4f}, p={p:.4f} -> {result} (a={alpha})")
    return stat, p


def correlation_test(x: pd.Series, y: pd.Series):
    """Pearson and Spearman correlation with p-values."""
    mask = x.notna() & y.notna()
    r_p, p_p = stats.pearsonr(x[mask], y[mask])
    r_s, p_s = stats.spearmanr(x[mask], y[mask])
    print(f"Pearson:  r={r_p:.4f}, p={p_p:.4f}")
    print(f"Spearman: r={r_s:.4f}, p={p_s:.4f}")
    return {"pearson": (r_p, p_p), "spearman": (r_s, p_s)}


def chi2_test(df: pd.DataFrame, col1: str, col2: str, alpha=0.05):
    """Chi-squared test of independence between two categorical columns."""
    ct = pd.crosstab(df[col1], df[col2])
    chi2, p, dof, expected = stats.chi2_contingency(ct)
    result = "dependent" if p < alpha else "independent"
    print(f"Chi2={chi2:.2f}, p={p:.4f}, dof={dof} -> {result} (a={alpha})")
    return chi2, p, dof
