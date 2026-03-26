"""
Creative Copilot - Creative Fatigue Detection
"""
import streamlit as st
from src.approval_workflow import approval_panel


def run_creative():
    """Run Creative Copilot"""
    st.subheader("🎨 Creative Copilot")
    st.write("Detect creative fatigue and recommend creative refreshes.")
    
    st.info("📋 Implementation coming soon")
    st.write("This copilot will:")
    st.write("- Calculate Creative Fatigue Index (frequency + CTR decay + CVR decay)")
    st.write("- Identify underperforming creatives")
    st.write("- Recommend pause/refresh timelines")
