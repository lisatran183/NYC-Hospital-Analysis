import pandas as pd
import matplotlib.pyplot as plt

# 1. Average Cost by Care Type (Bar Chart)

# Load dataset
df = pd.read_csv("Hospital_Inpatient_Cost_Transparency__Beginning_2009_20240726.csv")

# Drop missing values
df = df.dropna(subset=["Mean Cost", "APR Medical Surgical Description"])

# Group and calculate average cost
avg_cost = df.groupby("APR Medical Surgical Description")["Mean Cost"].mean().reset_index()

# Plot
plt.figure(figsize=(8, 5))
bars = plt.bar(avg_cost["APR Medical Surgical Description"], avg_cost["Mean Cost"])
plt.title("Average Inpatient Cost by Care Type")
plt.xlabel("Care Type")
plt.ylabel("Mean Cost")

# Add numbers on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 200, f"{yval:,.0f}", ha='center', va='bottom')

plt.tight_layout()
plt.show()
avg_cost.to_csv("avg_cost_by_care_type.csv", index=False)

#2. Top 10 Facilities by Total Inpatient Cost (Bar Chart)

# Ensure necessary columns
df = df.dropna(subset=["Mean Cost", "Discharges", "Facility Name"])

# Create Total Cost column
df["Total Cost"] = df["Mean Cost"] * df["Discharges"]

# Group and get top 10 facilities
top_facilities = (
    df.groupby("Facility Name")["Total Cost"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Plot
plt.figure(figsize=(10, 6))
bars = plt.barh(top_facilities["Facility Name"][::-1], top_facilities["Total Cost"][::-1])
plt.title("Top 10 Facilities by Total Inpatient Cost")
plt.xlabel("Total Cost")
plt.ylabel("Facility")

# Add data labels to bars
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1_000_000, bar.get_y() + bar.get_height() / 2, f"${width:,.0f}", va='center')

plt.tight_layout()
plt.show()

top_facilities.to_csv("top_10_facilities_total_cost.csv", index=False)

# 3. Top 10 Diagnoses by Charge-to-Cost Ratio (Dot Plot)

# Drop missing values
df = df.dropna(subset=["Mean Charge", "Mean Cost", "APR DRG Description"])

# Remove 0 or bad values
df = df[df["Mean Cost"] > 0]
df["Charge_to_Cost_Ratio"] = df["Mean Charge"] / df["Mean Cost"]

# Get top 10 diagnoses by markup
top_diagnoses = (
    df.groupby("APR DRG Description")[["Mean Charge", "Mean Cost"]]
    .mean()
    .assign(Charge_to_Cost_Ratio=lambda x: x["Mean Charge"] / x["Mean Cost"])
    .sort_values("Charge_to_Cost_Ratio", ascending=False)
    .head(10)
    .reset_index()
)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(top_diagnoses["Charge_to_Cost_Ratio"], top_diagnoses["APR DRG Description"])
plt.title("Top 10 Diagnoses by Charge-to-Cost Ratio")
plt.xlabel("Charge-to-Cost Ratio")
plt.ylabel("Diagnosis")
plt.tight_layout()
plt.show()

top_diagnoses.to_csv("top_10_diagnoses_markup.csv", index=False)

