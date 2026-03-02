"""Generate a synthetic housing dataset for demonstration purposes."""

import numpy as np
import pandas as pd

np.random.seed(42)
n = 500

sqft = np.random.normal(1800, 500, n).clip(600, 5000).astype(int)
bedrooms = np.random.choice([1, 2, 3, 4, 5], n, p=[0.05, 0.2, 0.4, 0.25, 0.1])
bathrooms = np.minimum(bedrooms, np.random.choice([1, 2, 3, 4], n, p=[0.15, 0.45, 0.3, 0.1]))
year_built = np.random.randint(1960, 2024, n)
lot_size = (sqft * np.random.uniform(1.5, 4.0, n)).astype(int)
neighborhood = np.random.choice(["Downtown", "Suburbs", "Rural", "Midtown"], n,
                                p=[0.25, 0.35, 0.25, 0.15])
garage = np.random.choice([0, 1, 2, 3], n, p=[0.15, 0.35, 0.35, 0.15])

# Price model with realistic coefficients + noise
price = (
    50_000
    + 120 * sqft
    + 15_000 * bedrooms
    + 20_000 * bathrooms
    + 500 * (year_built - 1960)
    + 5 * lot_size
    + 25_000 * garage
    + np.where(neighborhood == "Downtown", 60_000, 0)
    + np.where(neighborhood == "Midtown", 30_000, 0)
    + np.where(neighborhood == "Rural", -20_000, 0)
    + np.random.normal(0, 30_000, n)
).astype(int)

df = pd.DataFrame({
    "sqft": sqft,
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "year_built": year_built,
    "lot_size": lot_size,
    "neighborhood": neighborhood,
    "garage_spaces": garage,
    "price": price,
})

# Introduce a few missing values to make it realistic
for col in ["sqft", "year_built", "lot_size"]:
    mask = np.random.random(n) < 0.03
    df.loc[mask, col] = np.nan

df.to_csv("data/sample_housing.csv", index=False)
print(f"Generated {len(df)} rows → data/sample_housing.csv")
