import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Industrial AI Maintenance Agent", layout="wide")

# --- Title ---
st.title("🤖 Industrial Maintenance Agent (Agentic AI)")
st.markdown("This AI agent analyzes machine sensor data and recommends maintenance actions based on temperature and vibration anomalies.")

# --- Upload Section ---
uploaded_file = st.file_uploader("📄 Upload Sensor CSV File", type=["csv"])

# --- Load data ---
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    return df.tail(100)  # Only last 100 records

if uploaded_file:
    df = load_data(uploaded_file)
else:
    st.info("Using default simulated_sensor_data.csv")
    df = load_data("simulated_sensor_data.csv")

# --- Display raw data ---
with st.expander("📊 View Raw Sensor Data"):
    st.dataframe(df, use_container_width=True)

# --- Anomaly Detection ---
def detect_anomalies(records):
    alerts = []
    for _, row in records.iterrows():
        if row["temperature"] > 85 or row["vibration"] > 0.9:
            issue = "Overheating" if row["temperature"] > 85 else "High Vibration"
            alerts.append({
                "machine_id": row["machine_id"],
                "timestamp": row["timestamp"],
                "temperature": row["temperature"],
                "vibration": row["vibration"],
                "issue": issue
            })
    return alerts

def recommend_maintenance(alerts):
    recs = []
    for alert in alerts:
        rec = f"🔧 {alert['issue']} on **{alert['machine_id']}** at {alert['timestamp']} (Temp: {alert['temperature']}°C, Vibration: {alert['vibration']})."
        recs.append(rec)
    return recs

# --- Run Agent ---
alerts = detect_anomalies(df)
if alerts:
    st.subheader("🚨 Maintenance Recommendations")
    recommendations = recommend_maintenance(alerts)
    for r in recommendations:
        st.markdown(f"- {r}")
else:
    st.success("✅ All machines are operating within safe parameters.")

# --- Footer ---
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + Agentic AI logic.")
