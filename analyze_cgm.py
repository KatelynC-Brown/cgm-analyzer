"""
CGM Signal Quality & Glucose Trend Analyzer

Educational prototype using synthetic data.
NOT a medical device and NOT intended for diagnosis or treatment.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

DATA = Path(__file__).parent / "synthetic_cgm_data.csv"
OUTPUT = Path(__file__).parent / "outputs"

OUTPUT.mkdir(exist_ok=True)

# Load data
df = pd.read_csv(DATA, parse_dates=["timestamp"])

# -----------------------------
# Summary statistics
# -----------------------------

average_glucose = df["glucose_mg_dL"].mean()

percent_low = (
    (df["glucose_mg_dL"] < 70).mean() * 100
)

percent_high = (
    (df["glucose_mg_dL"] > 180).mean() * 100
)

flagged_readings = (
    df["flag"] != "Normal"
).sum()

print("=" * 55)
print("CGM SIGNAL QUALITY & GLUCOSE TREND ANALYZER")
print("=" * 55)

print(f"Average glucose: {average_glucose:.1f} mg/dL")
print(f"Readings below 70: {percent_low:.1f}%")
print(f"Readings above 180: {percent_high:.1f}%")
print(f"Flagged readings: {flagged_readings}")

# -----------------------------
# Chart 1: Glucose trend
# -----------------------------

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["glucose_mg_dL"],
    linewidth=1,
    label="Glucose reading"
)

plt.plot(
    df["timestamp"],
    df["rolling_mean_30m"],
    linewidth=2,
    label="30-minute rolling average"
)

plt.axhline(
    70,
    linestyle="--",
    label="70 mg/dL"
)

plt.axhline(
    180,
    linestyle="--",
    label="180 mg/dL"
)

plt.title("Synthetic Continuous Glucose Trend")
plt.xlabel("Time")
plt.ylabel("Glucose (mg/dL)")
plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT / "glucose_trend.png",
    dpi=180
)

plt.close()

# -----------------------------
# Chart 2: Rate of change
# -----------------------------

plt.figure(figsize=(12, 4))

plt.plot(
    df["timestamp"],
    df["rate_of_change_mg_dL_hr"],
    linewidth=1
)

plt.axhline(
    45,
    linestyle="--",
    label="Rapid-rise threshold"
)

plt.axhline(
    -45,
    linestyle="--",
    label="Rapid-fall threshold"
)

plt.title("Glucose Rate of Change")
plt.xlabel("Time")
plt.ylabel("mg/dL per hour")
plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT / "rate_of_change.png",
    dpi=180
)

plt.close()

# -----------------------------
# Chart 3: Flagged readings
# -----------------------------

flagged = df[df["flag"] != "Normal"]

plt.figure(figsize=(12, 5))

plt.plot(
    df["timestamp"],
    df["glucose_mg_dL"],
    linewidth=1,
    label="Glucose"
)

plt.scatter(
    flagged["timestamp"],
    flagged["glucose_mg_dL"],
    s=25,
    label="Flagged reading"
)

plt.title("Prototype Signal-Quality Flags")
plt.xlabel("Time")
plt.ylabel("Glucose (mg/dL)")
plt.legend()

plt.tight_layout()

plt.savefig(
    OUTPUT / "flagged_readings.png",
    dpi=180
)

plt.close()

print()
print(f"Charts saved to: {OUTPUT}")
