"""
Approval workflow state machine
"""
import streamlit as st
from datetime import datetime


def init_approval_state():
    """Initialize approval state in session"""
    if "approval_state" not in st.session_state:
        st.session_state.approval_state = "IDLE"
    if "last_output" not in st.session_state:
        st.session_state.last_output = None
    if "feedback" not in st.session_state:
        st.session_state.feedback = None


def approval_panel(copilot_name: str) -> str:
    """
    Display approval UI and handle user actions.
    
    Args:
        copilot_name: Name of copilot
    
    Returns:
        Final approval status (APPROVED, REJECTED, PENDING_REVIEW)
    """
    init_approval_state()
    
    state = st.session_state.approval_state
    
    if state == "IDLE":
        return "IDLE"
    
    if state == "GENERATING":
        st.info("⏳ Generating output...")
        return "GENERATING"
    
    if state == "PENDING_REVIEW":
        st.warning(f"⏳ {copilot_name} output pending review")
        
        # Display output
        st.divider()
        st.subheader("📊 Generated Output")
        st.write(st.session_state.last_output)
        st.divider()
        
        # Approval options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Approve", key=f"approve_{copilot_name}"):
                st.session_state.approval_state = "APPROVED"
                st.success("✅ Output approved!")
                st.rerun()
        
        with col2:
            if st.button("❌ Reject", key=f"reject_{copilot_name}"):
                st.session_state.show_rejection_form = True
        
        with col3:
            if st.button("👍 Feedback", key=f"feedback_{copilot_name}"):
                st.session_state.show_feedback_form = True
        
        # Rejection form
        if st.session_state.get("show_rejection_form", False):
            st.text_area("Why are you rejecting this output?", key="rejection_reason")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Confirm Rejection"):
                    st.session_state.approval_state = "REJECTED"
                    st.session_state.show_rejection_form = False
                    st.info(f"Output rejected. Reason: {st.session_state.rejection_reason}")
                    st.rerun()
            with col2:
                if st.button("Cancel"):
                    st.session_state.show_rejection_form = False
                    st.rerun()
        
        # Feedback form
        if st.session_state.get("show_feedback_form", False):
            feedback = st.radio("Rate this output:", ["👍 Helpful", "😐 Neutral", "👎 Not Helpful"], key="feedback_radio")
            if st.button("Submit Feedback"):
                st.session_state.feedback = feedback
                st.session_state.show_feedback_form = False
                st.success("Feedback recorded!")
                st.rerun()
        
        return "PENDING_REVIEW"
    
    if state == "APPROVED":
        st.success("✅ Output approved and logged")
        return "APPROVED"
    
    if state == "REJECTED":
        st.error("❌ Output rejected")
        return "REJECTED"
    
    return state


def log_approval(copilot_name: str, output: str, approved_by: str = "analyst"):
    """Log approval to database"""
    # TODO: Save to database
    print(f"✅ Approval logged: {copilot_name} by {approved_by}")


def log_rejection(copilot_name: str, reason: str, rejected_by: str = "analyst"):
    """Log rejection to database"""
    # TODO: Save to database
    print(f"❌ Rejection logged: {copilot_name} - {reason} by {rejected_by}")


def log_feedback(copilot_name: str, feedback: str):
    """Log feedback to database"""
    # TODO: Save to database
    print(f"📝 Feedback logged: {copilot_name} - {feedback}")
