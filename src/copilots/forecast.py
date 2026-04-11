"""
Forecast Copilot - Revenue Projections
"""
import streamlit as st
import pandas as pd
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_forecast():
    """Run Forecast Copilot"""
    st.subheader("📈 Forecast Copilot")
    st.write("Project 30/60/90-day revenue across spending scenarios.")

    # Data input tabs
    tab1, tab2 = st.tabs(["📊 Live Data", "📤 Upload CSV"])

    with tab1:
        st.info("Connect to live data sources (Meta, Google Ads, TikTok, LinkedIn)")
        st.write("Coming soon: Live API integration")

    with tab2:
        st.write("Upload your historical revenue and spend CSV")
        st.caption("Required columns: `date`, `channel`, `revenue`, `spend`")

        uploaded_file = st.file_uploader("Choose CSV", type=['csv'], key="forecast_csv")
        if uploaded_file:
            from src.csv_processor import process_upload

            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())

            schema_result = process_upload(df, 'forecast')

            if schema_result['valid']:
                st.success(f"✅ Valid Forecast data ({schema_result['rows']} rows)")
                st.session_state['forecast_data'] = schema_result['data']

                if 'dropped_rows' in schema_result and schema_result['dropped_rows'] > 0:
                    st.warning(f"⚠️ Dropped {schema_result['dropped_rows']} rows with missing values")
            else:
                st.error(f"❌ {schema_result['errors']}")
                return

    # Run copilot
    if 'forecast_data' in st.session_state and st.button("▶️ Run Forecast Copilot"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()

    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        if 'forecast_data' in st.session_state:
            df = st.session_state['forecast_data']

            # Calculate summary stats for prompt
            date_range = f"{df['date'].min()} to {df['date'].max()}"
            monthly_spend = df.groupby(pd.Grouper(key='date', freq='ME'))['spend'].sum()
            monthly_revenue = df.groupby(pd.Grouper(key='date', freq='ME'))['revenue'].sum()

            current_monthly_spend = monthly_spend.iloc[-1] if len(monthly_spend) > 0 else df['spend'].sum()
            current_monthly_revenue = monthly_revenue.iloc[-1] if len(monthly_revenue) > 0 else df['revenue'].sum()

            data_dict = {
                'historical_data': df.to_string(),
                'data_period': date_range,
                'current_monthly_spend': current_monthly_spend,
                'current_monthly_revenue': current_monthly_revenue,
            }

            prompt = load_prompt('forecast')
            if not prompt.startswith("❌"):
                output = run_copilot('Forecast', prompt, data_dict)
                st.session_state.last_output = output
                st.session_state.approval_state = "PENDING_REVIEW"
                st.rerun()
            else:
                st.error(prompt)

    # Approval panel
    approval_panel("Forecast")
