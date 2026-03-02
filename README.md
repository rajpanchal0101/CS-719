# Data Scientist Assistant

A personal data science toolkit for rapid exploratory analysis, preprocessing, and modeling.

## Project Structure

```
├── data/                   # Datasets
│   ├── sample_housing.csv  # Demo dataset (500 rows)
│   └── generate_sample_data.py
├── notebooks/              # Jupyter notebooks
│   └── data_scientist_assistant.ipynb  # Full demo workflow
├── src/                    # Reusable utilities
│   └── ds_utils.py         # EDA, visualization, preprocessing, modeling helpers
├── requirements.txt
└── README.md
```

## Quick Start

```bash
pip install -r requirements.txt
cd notebooks
jupyter notebook data_scientist_assistant.ipynb
```

## Toolkit Capabilities

| Module | Functions |
|--------|-----------|
| **Profiling** | `profile()`, `detect_outliers_iqr()` |
| **Visualization** | `plot_distributions()`, `plot_correlation_matrix()`, `plot_target_vs_features()` |
| **Preprocessing** | `auto_encode_categoricals()`, `prepare_data()` |
| **Modeling** | `evaluate_classifier()`, `evaluate_regressor()`, `quick_cross_val()` |
| **Statistics** | `normality_test()`, `correlation_test()` |

## Usage on Your Own Data

```python
from src.ds_utils import profile, plot_distributions, prepare_data, evaluate_regressor

df = pd.read_csv('your_data.csv')
profile(df)
plot_distributions(df)

X_train, X_test, y_train, y_test, scaler = prepare_data(df, target='your_target')
model = GradientBoostingRegressor().fit(X_train, y_train)
evaluate_regressor(model, X_test, y_test)
```
