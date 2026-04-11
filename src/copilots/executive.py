"""
Executive Copilot - Stakeholder Report Aggregator
"""
import streamlit as st
from datetime import datetime, timedelta
from src.claude_handler import run_copilot, load_prompt
from src.approval_workflow import approval_panel


def run_executive():
    """Run Executive Copilot"""
    st.subheader("📋 Executive Copilot")
    st.write("Aggregate approved copilot outputs into a stakeholder-ready weekly report.")

    st.divider()

    # Collect approved outputs from other copilots
    copilot_outputs = {
        'insights': st.session_state.get('approved_insights', None),
        'budget': st.session_state.get('approved_budget', None),
        'creative': st.session_state.get('approved_creative', None),
        'audience': st.session_state.get('approved_audience', None),
        'forecast': st.session_state.get('approved_forecast', None),
    }

    # Status display
    st.subheader("📊 Copilot Output Status")

    col1, col2, col3, col4, col5 = st.columns(5)

    status_cols = [col1, col2, col3, col4, col5]
    names = ['Insights', 'Budget', 'Creative', 'Audience', 'Forecast']
    keys = ['insights', 'budget', 'creative', 'audience', 'forecast']

    ready_count = 0
    for col, name, key in zip(status_cols, names, keys):
        with col:
            if copilot_outputs[key]:
                st.success(f"✅ {name}")
                ready_count += 1
            else:
                st.warning(f"⏳ {name}")

    st.divider()

    # Manual input option for outputs not yet in session
    st.subheader("📝 Manual Output Entry")
    st.write("Paste approved outputs from copilots if they're not in session:")

    for name, key in zip(names, keys):
        if not copilot_outputs[key]:
            text = st.text_area(
                f"{name} Output",
                placeholder=f"Paste approved {name} copilot output here...",
                key=f"manual_{key}",
                height=100,
            )
            if text.strip():
                copilot_outputs[key] = text.strip()
                ready_count += 1

    st.divider()

    # Minimum requirement: at least 2 copilot outputs
    if ready_count < 2:
        st.info(f"📋 Need at least 2 approved copilot outputs to generate report. Currently have {ready_count}/5.")
        st.write("Run the other copilots first, approve their outputs, then return here.")
        return

    st.success(f"✅ {ready_count}/5 copilot outputs ready for report generation")

    # Run copilot
    if st.button("▶️ Generate Weekly Report"):
        st.session_state.approval_state = "GENERATING"
        st.rerun()

    # Process if generating
    if st.session_state.get("approval_state") == "GENERATING":
        # Build report period string
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        report_period = f"{week_start.strftime('%B %d')} – {today.strftime('%B %d, %Y')}"

        data_dict = {
            'insights_output': copilot_outputs.get('insights', 'Not available this week.'),
            'budget_output': copilot_outputs.get('budget', 'Not available this week.'),
            'creative_output': copilot_outputs.get('creative', 'Not available this week.'),
            'audience_output': copilot_outputs.get('audience', 'Not available this week.'),
            'forecast_output': copilot_outputs.get('forecast', 'Not available this week.'),
            'report_period': report_period,
        }

        prompt = load_prompt('executive')
        if not prompt.startswith("❌"):
            output = run_copilot('Executive', prompt, data_dict)
            st.session_state.last_output = output
            st.session_state.approval_state = "PENDING_REVIEW"
            st.rerun()
        else:
            st.error(prompt)

    # Approval panel
    approval_panel("Executive")
