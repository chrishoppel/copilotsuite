"""
Audience Copilot - Audience Efficiency Analysis
"""
import streamlit as st
from src.approval_workflow import approval_panel


def run_audience():
    """Run Audience Copilot"""
    st.subheader("👥 Audience Copilot")
    st.write("Identify over/under-invested audience segments.")
    
    st.info("📋 Implementation coming soon")
    st.write("This copilot will:")
    st.write("- Calculate Audience Efficiency Index (AEI)")
    st.write("- Find over-invested segments (AEI < 70)")
    st.write("- Find under-invested segments (AEI > 120)")
    st.write("- Recommend zero-sum budget reallocation")
