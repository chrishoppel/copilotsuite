"""
Budget Copilot - Budget Reallocation Recommendations
"""
import streamlit as st
import pandas as pd
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_budget():
    """Run Budget Copilot"""
    st.subheader("💰 Budget Copilot")
    st.write("Recommend budget reallocations across channels using MMM output.")

    # Data input tabs
    tab1, tab2 = st.tabs(["📊 Live Data", "📤 Upload CSV"])

    with tab1:
        st.info("Connect to live data sources (Meta, Google Ads, TikTok, LinkedIn)")
        st.write("Coming soon: Live API integration")

    with tab2:
        st.write("Upload your MMM output and current spend allocation CSV")
        st.caption("Required columns: `channel`, `current_spend`, `mmm_allocation_pct`, `forecasted_roas`")

        uploaded_file = st.file_uploader("Choose CSV", type=['csv'], key="budget_csv")
        if uploaded_file:
            from src.csv_processor import process_upload

            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())

            # Validate
            schema_result = process_upload(df, 'budget')

            if schema_result['valid']:
                st.success(f"✅ Valid Budget data ({schema_result['rows']} rows)")
                st.session_state['budget_data'] = schema_result['data']

                if 'dropped_rows' in schema_result and schema_result['dropped_rows'] > 0:
                    st.warning(f"⚠️ Dropped {schema_result['dropped_rows']} rows with missing values")
            else:
                st.error(f"❌ {schema_result['errors']}")
                return

    # Run copilot
    if 'budget_data' in st.session_state and st.button("▶️ Run Budget Copilot"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()

    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        if 'budget_data' in st.session_state:
            df = st.session_state['budget_data']

            total_budget = df['current_spend'].sum()

            data_dict = {
                'budget_data': df.to_string(),
                'total_budget': total_budget,
            }

            prompt = load_prompt('budget')
            if not prompt.startswith("❌"):
                output = run_copilot('Budget', prompt, data_dict)
                st.session_state.last_output = output
                st.session_state.approval_state = "PENDING_REVIEW"
                st.rerun()
            else:
                st.error(prompt)

    # Approval panel
    approval_panel("Budget")
