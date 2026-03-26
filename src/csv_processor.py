"""
CSV upload processor and validator
"""
import pandas as pd
from typing import Dict, Tuple


# Required columns per copilot
CSV_SCHEMAS = {
    'insights': {
        'required': ['date', 'channel', 'impressions', 'clicks', 'spend', 'conversions'],
        'numeric': ['impressions', 'clicks', 'spend', 'conversions'],
        'description': 'Daily campaign metrics'
    },
    'budget': {
        'required': ['channel', 'current_spend', 'mmm_allocation_pct', 'forecasted_roas'],
        'numeric': ['current_spend', 'mmm_allocation_pct', 'forecasted_roas'],
        'description': 'MMM output and current spend allocation'
    },
    'creative': {
        'required': ['ad_id', 'creative_name', 'impressions', 'clicks', 'conversions'],
        'numeric': ['impressions', 'clicks', 'conversions'],
        'description': 'Ad performance by creative'
    },
    'audience': {
        'required': ['segment_id', 'segment_name', 'conversions', 'spend'],
        'numeric': ['conversions', 'spend'],
        'description': 'Audience segment performance'
    },
    'forecast': {
        'required': ['date', 'channel', 'revenue', 'spend'],
        'numeric': ['revenue', 'spend'],
        'description': 'Historical revenue and spend data'
    },
}


def process_upload(df: pd.DataFrame, copilot_type: str) -> Dict:
    """
    Validate and clean CSV upload.
    
    Args:
        df: Uploaded DataFrame
        copilot_type: Type of copilot (insights, budget, creative, etc.)
    
    Returns:
        Dictionary with 'valid' (bool), 'data' (DataFrame), 'rows' (int), or 'errors' (str)
    """
    
    if copilot_type not in CSV_SCHEMAS:
        return {'valid': False, 'errors': f"Unknown copilot type: {copilot_type}"}
    
    schema = CSV_SCHEMAS[copilot_type]
    required = schema['required']
    numeric_cols = schema['numeric']
    
    # Check required columns
    missing = set(required) - set(df.columns)
    if missing:
        return {'valid': False, 'errors': f"Missing columns: {', '.join(missing)}"}
    
    # Convert date columns
    if 'date' in df.columns:
        try:
            df['date'] = pd.to_datetime(df['date'])
        except Exception as e:
            return {'valid': False, 'errors': f"Invalid date format: {str(e)}"}
    
    # Convert numeric columns
    for col in numeric_cols:
        if col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception as e:
                return {'valid': False, 'errors': f"Column '{col}' should be numeric: {str(e)}"}
    
    # Remove rows with nulls in required columns
    initial_rows = len(df)
    df = df.dropna(subset=required)
    dropped_rows = initial_rows - len(df)
    
    if len(df) == 0:
        return {'valid': False, 'errors': "No valid rows after cleaning"}
    
    # Validate ranges
    if 'spend' in df.columns:
        if (df['spend'] < 0).any():
            return {'valid': False, 'errors': "Spend cannot be negative"}
    
    if 'impressions' in df.columns:
        if (df['impressions'] < 0).any():
            return {'valid': False, 'errors': "Impressions cannot be negative"}
    
    if 'conversions' in df.columns:
        if (df['conversions'] < 0).any():
            return {'valid': False, 'errors': "Conversions cannot be negative"}
    
    return {
        'valid': True,
        'data': df,
        'rows': len(df),
        'dropped_rows': dropped_rows,
        'description': schema['description']
    }
