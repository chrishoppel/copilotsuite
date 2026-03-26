"""
Executive Copilot - Stakeholder Report Aggregator
"""
import streamlit as st
from src.approval_workflow import approval_panel


def run_executive():
    """Run Executive Copilot"""
    st.subheader("📋 Executive Copilot")
    st.write("Aggregate approved copilot outputs into stakeholder report.")
    
    st.info("📋 Implementation coming soon")
    st.write("This copilot will:")
    st.write("- Pull all 5 approved copilot outputs")
    st.write("- Generate formatted weekly report")
    st.write("- Aggregate metrics and recommendations")
    st.write("- Ready-to-send to stakeholders")
