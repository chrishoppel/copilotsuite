"""
Forecast Copilot - Revenue Projections
"""
import streamlit as st
from src.approval_workflow import approval_panel


def run_forecast():
    """Run Forecast Copilot"""
    st.subheader("📈 Forecast Copilot")
    st.write("Project 30/60/90-day revenue across spending scenarios.")
    
    st.info("📋 Implementation coming soon")
    st.write("This copilot will:")
    st.write("- Use historical 90-day ROAS trends")
    st.write("- Apply seasonality indices")
    st.write("- Model 4 spend scenarios (bear / base / +15% / +30%)")
    st.write("- Project revenue at each scenario")
