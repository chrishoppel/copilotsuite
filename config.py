"""
Configuration and constants for Copilot Suite
"""

# Anomaly Detection Thresholds (Insights Copilot)
ANOMALY_THRESHOLDS = {
    'ctr': 0.15,          # 15% change
    'cpc': 0.20,          # 20% change
    'cpa': 0.20,          # 20% change
    'roas': 0.15,         # 15% change
    'conversion_rate': 0.15,  # 15% change
}

# Creative Fatigue Index Weights
CREATIVE_FATIGUE_WEIGHTS = {
    'frequency': 0.40,     # 40%
    'ctr_decay': 0.35,     # 35%
    'cvr_decay': 0.25,     # 25%
}

# Creative Fatigue Severity Bands
CREATIVE_FATIGUE_BANDS = {
    'FRESH': (0, 25),
    'GOOD': (25, 50),
    'WARNING': (50, 75),
    'CRITICAL': (75, 100),
}

# Audience Efficiency Index Thresholds
AUDIENCE_EFFICIENCY_THRESHOLDS = {
    'over_invested': 70,    # AEI < 70
    'under_invested': 120,  # AEI > 120
}

# Forecast Scenarios
FORECAST_SCENARIOS = {
    'bear': 0.85,      # 15% decrease
    'base': 1.00,      # current spend
    'plus_15': 1.15,   # 15% increase
    'plus_30': 1.30,   # 30% increase
}

# Database
DATABASE_URL = "sqlite:///copilot_suite.db"

# Streamlit
STREAMLIT_CONFIG = {
    'page_title': 'Copilot Suite',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded',
}

# Claude API
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
CLAUDE_MAX_TOKENS = 2048

# Data retention
CSV_UPLOAD_TTL_HOURS = 24  # Delete uploads after 24 hours
APPROVAL_HISTORY_DAYS = 90  # Keep approval history for 90 days

# Feedback targets
TARGET_APPROVAL_RATE = 0.80        # 80%
TARGET_POSITIVE_FEEDBACK_RATE = 0.60  # 60%
