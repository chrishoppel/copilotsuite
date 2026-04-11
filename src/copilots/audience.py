"""
Audience Copilot - Audience Efficiency Analysis
"""
import streamlit as st
import pandas as pd
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_audience():
    """Run Audience Copilot"""
    st.subheader("👥 Audience Copilot")
    st.write("Identify over/under-invested audience segments and recommend zero-sum reallocations.")

    # Data input tabs
    tab1, tab2 = st.tabs(["📊 Live Data", "📤 Upload CSV"])

    with tab1:
        st.info("Connect to live data sources (Meta, Google Ads, TikTok, LinkedIn)")
        st.write("Coming soon: Live API integration")

    with tab2:
        st.write("Upload your audience segment performance CSV")
        st.caption("Required columns: `segment_id`, `segment_name`, `conversions`, `spend`")

        uploaded_file = st.file_uploader("Choose CSV", type=['csv'], key="audience_csv")
        if uploaded_file:
            from src.csv_processor import process_upload

            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())

            schema_result = process_upload(df, 'audience')

            if schema_result['valid']:
                st.success(f"✅ Valid Audience data ({schema_result['rows']} rows)")
                st.session_state['audience_data'] = schema_result['data']

                if 'dropped_rows' in schema_result and schema_result['dropped_rows'] > 0:
                    st.warning(f"⚠️ Dropped {schema_result['dropped_rows']} rows with missing values")
            else:
                st.error(f"❌ {schema_result['errors']}")
                return

    # Run copilot
    if 'audience_data' in st.session_state and st.button("▶️ Run Audience Copilot"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()

    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        if 'audience_data' in st.session_state:
            df = st.session_state['audience_data']

            total_spend = df['spend'].sum()
            total_conversions = df['conversions'].sum()

            # Calculate AEI for display
            df_display = df.copy()
            df_display['spend_share_pct'] = (df_display['spend'] / total_spend * 100).round(2)
            df_display['conversion_share_pct'] = (df_display['conversions'] / total_conversions * 100).round(2)
            df_display['aei'] = (df_display['conversion_share_pct'] / df_display['spend_share_pct'].replace(0, 0.01) * 100).round(1)

            data_dict = {
                'audience_data': df_display.to_string(),
                'total_segments': len(df),
                'total_spend': total_spend,
                'total_conversions': total_conversions,
            }

            prompt = load_prompt('audience')
            if not prompt.startswith("❌"):
                output = run_copilot('Audience', prompt, data_dict)
                st.session_state.last_output = output
                st.session_state.approval_state = "PENDING_REVIEW"
                st.rerun()
            else:
                st.error(prompt)

    # Approval panel
    approval_panel("Audience")
