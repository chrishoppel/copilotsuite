"""
Creative Copilot - Creative Fatigue Detection
"""
import streamlit as st
import pandas as pd
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_creative():
    """Run Creative Copilot"""
    st.subheader("🎨 Creative Copilot")
    st.write("Detect creative fatigue and recommend creative refreshes.")

    # Data input tabs
    tab1, tab2 = st.tabs(["📊 Live Data", "📤 Upload CSV"])

    with tab1:
        st.info("Connect to live data sources (Meta, Google Ads, TikTok, LinkedIn)")
        st.write("Coming soon: Live API integration")

    with tab2:
        st.write("Upload your ad creative performance CSV")
        st.caption("Required columns: `ad_id`, `creative_name`, `impressions`, `clicks`, `conversions`")

        uploaded_file = st.file_uploader("Choose CSV", type=['csv'], key="creative_csv")
        if uploaded_file:
            from src.csv_processor import process_upload

            df = pd.read_csv(uploaded_file)
            st.write("Preview:")
            st.dataframe(df.head())

            schema_result = process_upload(df, 'creative')

            if schema_result['valid']:
                st.success(f"✅ Valid Creative data ({schema_result['rows']} rows)")
                st.session_state['creative_data'] = schema_result['data']

                if 'dropped_rows' in schema_result and schema_result['dropped_rows'] > 0:
                    st.warning(f"⚠️ Dropped {schema_result['dropped_rows']} rows with missing values")
            else:
                st.error(f"❌ {schema_result['errors']}")
                return

    # Run copilot
    if 'creative_data' in st.session_state and st.button("▶️ Run Creative Copilot"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()

    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        if 'creative_data' in st.session_state:
            df = st.session_state['creative_data']

            # Calculate CTR and CVR for the prompt
            df_display = df.copy()
            df_display['ctr'] = (df_display['clicks'] / df_display['impressions'] * 100).round(2)
            df_display['cvr'] = (df_display['conversions'] / df_display['clicks'].replace(0, 1) * 100).round(2)

            data_dict = {
                'creative_data': df_display.to_string(),
                'total_creatives': len(df),
            }

            prompt = load_prompt('creative')
            if not prompt.startswith("❌"):
                output = run_copilot('Creative', prompt, data_dict)
                st.session_state.last_output = output
                st.session_state.approval_state = "PENDING_REVIEW"
                st.rerun()
            else:
                st.error(prompt)

    # Approval panel
    approval_panel("Creative")
