"""
Insights Copilot - Anomaly Detection & Executive Summary
"""
import streamlit as st
import pandas as pd
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_insights():
    """Run Insights Copilot"""
    st.subheader("🔍 Insights Copilot")
    st.write("Detect anomalies, identify root causes, generate executive summaries.")
    
    # Data input tabs
    tab1, tab2 = st.tabs(["📊 Live Data", "📤 Upload CSV"])
    
    with tab1:
        st.info("Connect to live data sources (Meta, Google Ads, TikTok, LinkedIn)")
        # TODO: Implement live data fetching
        st.write("Coming soon: Live API integration")
    
    with tab2:
        st.write("Upload your daily campaign metrics CSV")
        
        uploaded_file = st.file_uploader("Choose CSV", type=['csv'], key="insights_csv")
        if uploaded_file:
            from src.csv_processor import process_upload
            
            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())
            
            # Validate
            schema_result = process_upload(df, 'insights')
            
            if schema_result['valid']:
                st.success(f"✅ Valid Insights data ({schema_result['rows']} rows)")
                st.session_state['insights_data'] = schema_result['data']
                
                # Store in session
                if 'dropped_rows' in schema_result and schema_result['dropped_rows'] > 0:
                    st.warning(f"⚠️ Dropped {schema_result['dropped_rows']} rows with missing values")
            else:
                st.error(f"❌ {schema_result['errors']}")
                return
    
    # Run copilot
    if 'insights_data' in st.session_state and st.button("▶️ Run Insights Copilot"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()
    
    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        if 'insights_data' in st.session_state:
            df = st.session_state['insights_data']
            
            # Prepare data dictionary for prompt
            data_dict = {
                'current_week_metrics': df.tail(7).to_string(),
                'baseline_metrics': df.iloc[-14:-7].to_string(),
                'total_rows': len(df),
            }
            
            # Load and run copilot
            prompt = load_prompt('insights')
            if not prompt.startswith("❌"):
                output = run_copilot('Insights', prompt, data_dict)
                st.session_state.last_output = output
                st.session_state.approval_state = "PENDING_REVIEW"
                st.rerun()
            else:
                st.error(prompt)
    
    # Approval panel
    approval_panel("Insights")
