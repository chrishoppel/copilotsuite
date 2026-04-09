# Copilot Suite

**Marketing Intelligence Platform** — Six specialized AI copilots that analyze marketing data, surface insights, and recommend actions.

Built with Python + Streamlit, deployed via GitHub to Streamlit Cloud.

## Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/chris/copilot-suite
cd copilot-suite
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Secrets

Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill in your API keys:

```toml
[anthropic]
api_key = "sk-ant-..."

[meta]
access_token = "..."
business_account_id = "..."

[google_ads]
credentials = """..."""

[tiktok]
access_token = "..."

[linkedin]
access_token = "..."
```

### 3. Run Locally

```bash
streamlit run app.py
```

Visit `http://localhost:8501`

### 4. Deploy to Streamlit Cloud

1. Push to GitHub: `git push origin main`
2. Go to https://share.streamlit.io
3. Click "New App" → Select this repo
4. Add secrets in Streamlit Cloud dashboard
5. Done! Auto-deploys on every push

➡️ See `DEPLOYMENT_PLAN.md`, `DEPLOYMENT_LOG.md`, and `docs/SECRETS_READINESS.md` for the deployment checklist + secrets runbook. Use `scripts/validate_secrets.py` and `scripts/test_google_ads_auth.py` before every push.

## Six Copilots

| Copilot | Purpose | Input |
|---------|---------|-------|
| **Insights** | Anomaly detection & executive summaries | Daily metrics (CSV or API) |
| **Budget** | Budget reallocation recommendations | MMM output + current spend |
| **Creative** | Creative fatigue detection | Ad performance data |
| **Audience** | Audience efficiency analysis | Segment conversion data |
| **Forecast** | Revenue projections (30/60/90 days) | Historical data + scenarios |
| **Executive** | Weekly stakeholder reports | Approved copilot outputs |

## Data Input Methods

### Live APIs
- Meta (Facebook Ads)
- Google Ads
- TikTok Ads
- LinkedIn Ads

### CSV Uploads
- Daily campaign metrics
- MMM output
- Audience segment data
- Historical revenue/spend

## Approval Workflow

```
IDLE → GENERATING → PENDING_REVIEW → APPROVED/REJECTED
```

All outputs require analyst approval before being shared with stakeholders.

## File Structure

```
copilot-suite/
├── app.py                      # Main Streamlit app
├── config.py                   # Configuration & constants
├── requirements.txt
├── .streamlit/
│   ├── config.toml            # Streamlit theme
│   └── secrets.toml.example   # Template for secrets
├── src/
│   ├── claude_handler.py      # Claude API wrapper
│   ├── csv_processor.py       # CSV validation
│   ├── approval_workflow.py   # Approval UI
│   └── copilots/              # Six copilot implementations
├── prompts/                    # Prompt templates (versioned)
├── db/                        # Database schema
└── uploads/                   # Temp CSV storage (git-ignored)
```

## Development

### Deployment hygiene
- Use `DEPLOYMENT_PLAN.md` for the full Streamlit Cloud checklist.
- Run `python scripts/validate_secrets.py` to confirm `.streamlit/secrets.toml` has all required keys before pushing.
- Log each deploy/validation step in `DEPLOYMENT_LOG.md` so we have an audit trail.

### Add a new prompt version

1. Create `prompts/copilot_name_v1.1.txt`
2. Update Claude handler to load new version
3. Test with historical data
4. Commit and deploy

### Add a new data source

1. Extend `src/data_loader.py`
2. Add API client initialization
3. Add schema to `src/csv_processor.py`
4. Test with sample data

## Security

- API keys in `.streamlit/secrets.toml` (git-ignored)
- No PII in prompts (aggregated data only)
- Audit logs for all approvals
- Session timeout: 8 hours

## Support

For issues or questions, open a GitHub issue or reach out to @chris

---

**Version:** 2.0 | **Built with:** Python, Streamlit, Claude API
