"""
Generate synthetic CGM-style data.

This data is completely artificial and is intended only
for educational/portfolio purposes.
"""

from pathlib import Path

import numpy as np
import pandas as pd


# Reproducible random numbers
rng = np.random.default_rng(42)

# Seven days, one measurement every five minutes
minutes = np.arange(
    0,
    7 * 24 * 60,
    5
)

timestamps = (
    pd.Timestamp("2026-01-05 00:00")
    + pd.to_timedelta(minutes, unit="m")
)

# Convert minutes into hours and days
hour = (minutes / 60) % 24
day = minutes / (24 * 60)

# ----------------------------------
# Create baseline glucose signal
# ----------------------------------

glucose = (
    105
    + 8 * np.sin(
        2 * np.pi * (hour - 5) / 24
    )
    + 5 * np.sin(
        2 * np.pi * day / 7
    )
)

# ----------------------------------
# Simulate meal-related increases
# ----------------------------------

meals = [
    (8, 35),    # breakfast
    (13, 28),   # lunch
    (19, 42)    # dinner
]

for meal_hour, amplitude in meals:

    distance = np.minimum(
        np.abs(hour - meal_hour),
        24 - np.abs(hour - meal_hour)
    )

    glucose += (
        amplitude
        * np.exp(-(distance / 1.5) ** 2)
    )

# ----------------------------------
# Add sensor-like random noise
# ----------------------------------

glucose += rng.normal(
    0,
    3.5,
    size=len(glucose)
)

# ----------------------------------
# Add artificial anomalies
# ----------------------------------

anomaly_indices = rng.choice(
    len(glucose),
    size=18,
    replace=False
)

anomaly_types = rng.choice(
    ["spike", "drop"],
    size=len(anomaly_indices)
)

for index, anomaly_type in zip(
    anomaly_indices,
    anomaly_types
):

    magnitude = rng.uniform(
        35,
        65
    )

    if anomaly_type == "spike":
        glucose[index] += magnitude

    else:
        glucose[index] -= magnitude

# Keep values within a reasonable
# synthetic range.
glucose = np.clip(
    glucose,
    45,
    280
)

# ----------------------------------
# Create DataFrame
# ----------------------------------

df = pd.DataFrame({
    "timestamp": timestamps,
    "glucose_mg_dL": np.round(
        glucose,
        1
    )
})

# ----------------------------------
# Calculate rolling statistics
# ----------------------------------

df["rolling_mean_30m"] = (
    df["glucose_mg_dL"]
    .rolling(
        window=6,
        min_periods=1
    )
    .mean()
)

# Five-minute measurements converted
# into an hourly rate of change.
df["rate_of_change_mg_dL_hr"] = (
    df["glucose_mg_dL"].diff()
    / (5 / 60)
)

df["rolling_std_30m"] = (
    df["glucose_mg_dL"]
    .rolling(
        window=6,
        min_periods=3
    )
    .std()
)

# ----------------------------------
# Flag potentially unusual readings
# ----------------------------------

rapid_change = (
    df["rate_of_change_mg_dL_hr"]
    .abs()
    > 45
)

high_variability = (
    df["rolling_std_30m"]
    > 18
)

out_of_range = (
    (df["glucose_mg_dL"] < 70)
    |
    (df["glucose_mg_dL"] > 180)
)

df["flag"] = np.select(
    [
        rapid_change,
        high_variability,
        out_of_range
    ],
    [
        "Rapid change",
        "High variability",
        "Out-of-range"
    ],
    default="Normal"
)

# ----------------------------------
# Save CSV
# ----------------------------------

output_file = (
    Path(__file__).parent
    / "synthetic_cgm_data.csv"
)

df.to_csv(
    output_file,
    index=False
)

print("Synthetic CGM dataset created!")
print(f"Saved to: {output_file}")
print(f"Number of readings: {len(df)}")
