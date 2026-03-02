"""
Data Science utility functions for quick exploratory data analysis,
feature engineering, and model evaluation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    mean_squared_error,
    r2_score,
    mean_absolute_error,
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

def plot_distributions(df: pd.DataFrame, cols: list[str] | None = None,
                       figsize: tuple = (14, 4)):
    """Histogram + KDE for selected numeric columns."""
    if cols is None:
        cols = df.select_dtypes(include="number").columns.tolist()
    n = len(cols)
    fig, axes = plt.subplots(1, n, figsize=(figsize[0], figsize[1]))
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        sns.histplot(df[col].dropna(), kde=True, ax=ax)
        ax.set_title(col)
    plt.tight_layout()
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame, figsize: tuple = (10, 8),
                            annot: bool = True):
    """Heatmap of Pearson correlations for numeric columns."""
    corr = df.select_dtypes(include="number").corr()
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot, cmap="coolwarm", center=0, fmt=".2f")
    plt.title("Correlation Matrix")
    plt.tight_layout()
    plt.show()


def plot_target_vs_features(df: pd.DataFrame, target: str,
                            cols: list[str] | None = None,
                            figsize: tuple = (14, 4)):
    """Scatter plots of target vs each feature."""
    if cols is None:
        cols = [c for c in df.select_dtypes(include="number").columns if c != target]
    n = len(cols)
    fig, axes = plt.subplots(1, n, figsize=(figsize[0], figsize[1]))
    if n == 1:
        axes = [axes]
    for ax, col in zip(axes, cols):
        ax.scatter(df[col], df[target], alpha=0.5, s=10)
        ax.set_xlabel(col)
        ax.set_ylabel(target)
        ax.set_title(f"{target} vs {col}")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# 3. Preprocessing helpers
# ---------------------------------------------------------------------------

def auto_encode_categoricals(df: pd.DataFrame, max_cardinality: int = 10):
    """One-hot encode low-cardinality categoricals; label-encode the rest."""
    df = df.copy()
    cat_cols = df.select_dtypes(include=["object", "category"]).columns
    for col in cat_cols:
        if df[col].nunique() <= max_cardinality:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df.drop(columns=col), dummies], axis=1)
        else:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    return df


def prepare_data(df: pd.DataFrame, target: str, test_size: float = 0.2,
                 scale: bool = True, random_state: int = 42):
    """Split into train/test, optionally scale features."""
    X = df.drop(columns=[target])
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    if scale:
        scaler = StandardScaler()
        X_train = pd.DataFrame(scaler.fit_transform(X_train),
                               columns=X.columns, index=X_train.index)
        X_test = pd.DataFrame(scaler.transform(X_test),
                              columns=X.columns, index=X_test.index)
        return X_train, X_test, y_train, y_test, scaler
    return X_train, X_test, y_train, y_test, None


# ---------------------------------------------------------------------------
# 4. Model evaluation helpers
# ---------------------------------------------------------------------------

def evaluate_classifier(model, X_test, y_test):
    """Print classification report and plot confusion matrix."""
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    plt.show()


def evaluate_regressor(model, X_test, y_test):
    """Print regression metrics and plot actual vs predicted."""
    y_pred = model.predict(X_test)
    print(f"R²:   {r2_score(y_test, y_pred):.4f}")
    print(f"MAE:  {mean_absolute_error(y_test, y_pred):.4f}")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")
    plt.figure(figsize=(6, 6))
    plt.scatter(y_test, y_pred, alpha=0.5, s=10)
    mn, mx = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
    plt.plot([mn, mx], [mn, mx], "r--")
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.tight_layout()
    plt.show()


def quick_cross_val(model, X, y, cv: int = 5, scoring: str = "accuracy"):
    """Run cross-validation and print summary statistics."""
    scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
    print(f"CV {scoring}: {scores.mean():.4f} (+/- {scores.std():.4f})")
    return scores


# ---------------------------------------------------------------------------
# 5. Statistical tests
# ---------------------------------------------------------------------------

def normality_test(series: pd.Series, alpha: float = 0.05):
    """Shapiro-Wilk test for normality (use on samples <= 5000)."""
    sample = series.dropna()
    if len(sample) > 5000:
        sample = sample.sample(5000, random_state=42)
    stat, p = stats.shapiro(sample)
    result = "normal" if p > alpha else "not normal"
    print(f"Shapiro-Wilk: stat={stat:.4f}, p={p:.4f} → {result} (α={alpha})")
    return stat, p


def correlation_test(x: pd.Series, y: pd.Series):
    """Pearson and Spearman correlation with p-values."""
    mask = x.notna() & y.notna()
    r_p, p_p = stats.pearsonr(x[mask], y[mask])
    r_s, p_s = stats.spearmanr(x[mask], y[mask])
    print(f"Pearson:  r={r_p:.4f}, p={p_p:.4f}")
    print(f"Spearman: r={r_s:.4f}, p={p_s:.4f}")
    return {"pearson": (r_p, p_p), "spearman": (r_s, p_s)}
