"""
Budget Copilot - Budget Reallocation Recommendations
"""
import streamlit as st
from src.approval_workflow import approval_panel


def run_budget():
    """Run Budget Copilot"""
    st.subheader("💰 Budget Copilot")
    st.write("Recommend budget reallocations across channels using MMM output.")
    
    st.info("📋 Implementation coming soon")
    st.write("This copilot will:")
    st.write("- Read MMM allocation percentages")
    st.write("- Calculate dollar amounts per channel")
    st.write("- Project ROAS improvements")
    st.write("- Generate reallocation recommendations")
