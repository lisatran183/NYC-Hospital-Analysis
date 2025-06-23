import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("Hospital_Inpatient_Cost_Transparency__Beginning_2009_20240726.csv")

# Clean basic missing value:
df = df.dropna(subset=["Mean Cost", "Mean Charge", "Discharges", "APR DRG Description"])

# Add new columns:
df["Total Cost"] = df["Mean Cost"] * df["Discharges"]
df["Charge_to_Cost_Ratio"] = df["Mean Charge"] / df["Mean Cost"]

# Step 4: Remove invalid ratios
df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["Charge_to_Cost_Ratio"])

# Step 5: Show top 10 diagnoses by highest markup
top_markup = (
    df.groupby("APR DRG Description")[["Mean Cost", "Mean Charge"]]
    .mean()
    .assign(Charge_to_Cost_Ratio=lambda x: x["Mean Charge"] / x["Mean Cost"])
    .sort_values("Charge_to_Cost_Ratio", ascending=False)
    .head(10)
)

# Step 6: Print the results
print("Top 10 Diagnoses by Charge-to-Cost Ratio:")
print(top_markup)