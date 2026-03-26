"""
Claude API wrapper for Copilot Suite
"""
import streamlit as st
from anthropic import Anthropic
from config import CLAUDE_MODEL, CLAUDE_MAX_TOKENS


def get_claude_client():
    """Initialize Claude API client with secrets"""
    api_key = st.secrets.get("anthropic", {}).get("api_key")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in secrets")
    return Anthropic(api_key=api_key)


def run_copilot(copilot_name: str, prompt_template: str, data_dict: dict) -> str:
    """
    Run Claude with injected data.
    
    Args:
        copilot_name: Name of copilot (for logging)
        prompt_template: Prompt template with {placeholders}
        data_dict: Dictionary of data to inject into prompt
    
    Returns:
        Claude's response text
    """
    client = get_claude_client()
    
    # Inject live data into prompt
    try:
        filled_prompt = prompt_template.format(**data_dict)
    except KeyError as e:
        return f"❌ Error: Missing data key {e} for prompt template"
    
    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[
                {"role": "user", "content": filled_prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"❌ Claude API error: {str(e)}"


def load_prompt(copilot_name: str, version: str = "1.0") -> str:
    """Load prompt template from file"""
    try:
        with open(f"prompts/{copilot_name}_v{version}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ Prompt file not found: prompts/{copilot_name}_v{version}.txt"
