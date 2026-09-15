"""
Interactive CGM Signal Analysis Dashboard.

Run with:

    streamlit run app.py
"""

import pandas as pd
import streamlit as st


# ----------------------------------
# Page configuration
# ----------------------------------

st.set_page_config(
    page_title="CGM Signal Analyzer",
    page_icon="📊",
    layout="wide"
)


# ----------------------------------
# Title
# ----------------------------------

st.title(
    "CGM Signal Quality & Glucose Trend Analyzer"
)

st.caption(
    "Educational prototype using synthetic data. "
    "Not a medical device."
)


# ----------------------------------
# Load dataset
# ----------------------------------

df = pd.read_csv(
    "synthetic_cgm_data.csv",
    parse_dates=["timestamp"]
)


# ----------------------------------
# Calculate metrics
# ----------------------------------

average_glucose = (
    df["glucose_mg_dL"].mean()
)

flagged_readings = (
    df["flag"] != "Normal"
).sum()

rapid_changes = (
    df["flag"] == "Rapid change"
).sum()

high_variability = (
    df["flag"] == "High variability"
).sum()

out_of_range = (
    df["flag"] == "Out-of-range"
).sum()


# ----------------------------------
# Dashboard metrics
# ----------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average glucose",
        f"{average_glucose:.1f} mg/dL"
    )

with col2:
    st.metric(
        "Flagged readings",
        flagged_readings
    )

with col3:
    st.metric(
        "Rapid changes",
        rapid_changes
    )

with col4:
    st.metric(
        "Out-of-range",
        out_of_range
    )


# ----------------------------------
# Glucose chart
# ----------------------------------

st.subheader("Glucose Trend")

chart_data = df.set_index(
    "timestamp"
)[
    [
        "glucose_mg_dL",
        "rolling_mean_30m"
    ]
]

st.line_chart(
    chart_data
)


# ----------------------------------
# Rate-of-change chart
# ----------------------------------

st.subheader("Glucose Rate of Change")

rate_data = df.set_index(
    "timestamp"
)[
    ["rate_of_change_mg_dL_hr"]
]

st.line_chart(
    rate_data
)


# ----------------------------------
# Flagged readings
# ----------------------------------

st.subheader(
    "Potential Signal-Quality Events"
)

flagged_data = df[
    df["flag"] != "Normal"
][
    [
        "timestamp",
        "glucose_mg_dL",
        "rate_of_change_mg_dL_hr",
        "rolling_std_30m",
        "flag"
    ]
]

st.dataframe(
    flagged_data.head(100),
    use_container_width=True
)


# ----------------------------------
# Explanation
# ----------------------------------

st.subheader(
    "How the Prototype Works"
)

st.markdown(
    """
The prototype looks for three types of events:

**1. Rapid change**

A reading is flagged when the calculated glucose
rate of change exceeds the project's illustrative
threshold.

**2. High variability**

A reading is flagged when short-term variation
within the rolling window becomes unusually high.

**3. Out-of-range**

A reading is flagged when it falls outside the
illustrative range used by this educational project.

These thresholds are for demonstration purposes
only and are **not clinical recommendations**.
"""
)


# ----------------------------------
# Future development
# ----------------------------------

st.subheader(
    "Future Development"
)

st.markdown(
    """
- Test the algorithm using appropriately de-identified real data.
- Compare rule-based detection with machine-learning approaches.
- Measure precision, recall, and false-alert rates.
- Improve handling of missing and noisy sensor readings.
- Add uncertainty estimates.
- Work with domain experts to establish appropriate validation criteria.
- Consider medical-device software, privacy, quality, and regulatory requirements.
"""
)
