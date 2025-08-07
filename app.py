import streamlit as st
import pandas as pd
from generate_forecast import generate_forecast

# --- Title ---
st.set_page_config(page_title="📊 Sales Forecasting App", layout="wide")
st.title("📈 AI-Powered Sales Forecast")
st.markdown("Upload your sales data and get a 30-day sales forecast.")

# --- File Upload ---
uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    sample_path = "data/Sample_Superstore.csv"
    df.to_csv(sample_path, index=False)  # Save uploaded file

    # --- Forecast Generation ---
    with st.spinner("Generating forecast..."):
        forecast_df = generate_forecast(csv_path=sample_path)

    st.success("✅ Forecast generated!")

    # --- Show Forecast Table ---
    st.subheader("📅 Forecast for Next 30 Days")
    st.dataframe(forecast_df)

    # --- Download Button ---
    st.download_button(
        label="⬇ Download Forecast CSV",
        data=forecast_df.to_csv(index=False).encode('utf-8'),
        file_name="forecast.csv",
        mime="text/csv"
    )
else:
    st.warning("👆 Please upload a CSV file to begin.")

