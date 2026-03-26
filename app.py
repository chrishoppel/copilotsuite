"""
Copilot Suite - Main Streamlit App
Marketing Intelligence Platform with 6 AI Copilots
"""
import streamlit as st
from config import STREAMLIT_CONFIG
from src.copilots.insights import run_insights
from src.copilots.budget import run_budget
from src.copilots.creative import run_creative
from src.copilots.audience import run_audience
from src.copilots.forecast import run_forecast
from src.copilots.executive import run_executive
from src.approval_workflow import init_approval_state

# Page config
st.set_page_config(
    page_title=STREAMLIT_CONFIG['page_title'],
    layout=STREAMLIT_CONFIG['layout'],
    initial_sidebar_state=STREAMLIT_CONFIG['initial_sidebar_state'],
)

# Initialize session state
init_approval_state()

# Sidebar navigation
st.sidebar.title("🤖 Copilot Suite")
st.sidebar.write("Marketing Intelligence Platform")
st.sidebar.divider()

page = st.sidebar.radio(
    "Select Copilot",
    [
        "Dashboard",
        "Insights",
        "Budget",
        "Creative",
        "Audience",
        "Forecast",
        "Executive"
    ],
    index=0
)

st.sidebar.divider()
st.sidebar.write("**About**")
st.sidebar.write("Six specialized AI copilots analyzing marketing data with human approval.")

# Main content
if page == "Dashboard":
    st.title("📊 Copilot Suite Dashboard")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Insights", "Ready", "+0")
    with col2:
        st.metric("Approvals", "0", "0%")
    with col3:
        st.metric("Health", "100%", "✅")
    
    st.divider()
    
    st.subheader("🚀 Quick Start")
    st.write("Select a copilot from the left sidebar to get started:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Insights Copilot**\nDetect anomalies & trends")
    with col2:
        st.info("**Budget Copilot**\nOptimize spend allocation")
    with col3:
        st.info("**Creative Copilot**\nIdentify creative fatigue")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Audience Copilot**\nFind efficiency gaps")
    with col2:
        st.info("**Forecast Copilot**\nProject revenue scenarios")
    with col3:
        st.info("**Executive Copilot**\nGenerate reports")
    
    st.divider()
    
    st.subheader("📋 Recent Approvals")
    st.write("No approvals yet. Run a copilot to get started!")

elif page == "Insights":
    run_insights()

elif page == "Budget":
    run_budget()

elif page == "Creative":
    run_creative()

elif page == "Audience":
    run_audience()

elif page == "Forecast":
    run_forecast()

elif page == "Executive":
    run_executive()

# Footer
st.divider()
st.caption("Copilot Suite v2.0 | Powered by Claude API")
