# Streamlit Secrets Readiness Kit

_Last updated: 2026-04-08_

This kit turns the deployment-blocking secrets work into a repeatable checklist. Use it when collecting API credentials for Copilot Suite before pushing to Streamlit Cloud. Pair it with `DEPLOYMENT_PLAN.md` for the full deployment workflow.

## 1. Inventory & Owners

| Section | Keys Needed | Source of Truth | Owner / Contact | Status | Verification Step |
|---------|-------------|-----------------|-----------------|--------|-------------------|
| `[anthropic]` | `api_key` | Anthropic Console → API Keys | Chris | ☐ Pending | `curl https://api.anthropic.com/v1/messages -H "x-api-key: $KEY" -H "anthropic-version: 2023-06-01" -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":1,"messages":[{"role":"user","content":"ping"}]}'` |
| `[meta]` | `access_token`, `business_account_id` | Meta Business Manager → Marketing API Tools | Paid Social Lead (or Chris) | ☐ Pending | `curl -G "https://graph.facebook.com/v19.0/act_<BUSINESS_ID>/insights" -d access_token=$TOKEN -d limit=1` |
| `[google_ads]` | `credentials` (service account JSON) | Google Cloud Console → IAM & Admin → Service Accounts | Marketing Ops / Chris | ☐ Pending | `python scripts/test_google_ads_auth.py` (see Section 3) |
| `[tiktok]` | `access_token`, `advertiser_id` | TikTok Ads Manager → Assets → Developer Apps | Paid Social Lead | ☐ Pending | `curl -G "https://business-api.tiktok.com/open_api/v1.3/ad/get/" -d advertiser_id=$ID -d access_token=$TOKEN` |
| `[linkedin]` | `access_token` | LinkedIn Developer Portal → Marketing Developer Platform App | Marketing Ops | ☐ Pending | `curl -G "https://api.linkedin.com/v2/adAccounts" -H "Authorization: Bearer $TOKEN" -d q=search -d search.type=BUSINESS` |

## 2. Collection Workflow

1. **Duplicate this checklist** (copy/paste into the daily note) so status boxes can be marked in real time.
2. **Request credentials** in parallel:
   - Send Anthropic key request to Chris (primary owner) if not already stored in 1Password.
   - Ping paid social owners for Meta/TikTok, marketing ops for Google Ads + LinkedIn.
3. **Store raw secrets** in 1Password (vault: "Copilot Suite") with shared access for Chris + Han.
4. **Paste values** into `.streamlit/secrets.toml` (never commit the file). Template lives in `.streamlit/secrets.toml.example`.
5. Run `python scripts/validate_secrets.py` — repeat until `[OK]` is printed.
6. Upload the same TOML block into Streamlit Cloud → **App → Settings → Secrets**.
7. Log completion in `DEPLOYMENT_LOG.md` with timestamp + owner initials.

## 3. Optional: Lightweight Token Tests

To avoid burning deployment minutes with invalid credentials, run these local checks after populating `secrets.toml`:

- **Anthropic sanity check:**
  ```bash
  python - <<'PY'
  import anthropic, os
  client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
  msg = client.messages.create(model="claude-3-5-sonnet-20241022", max_tokens=5, messages=[{"role":"user","content":"ping"}])
  print(msg.usage)
  PY
  ```
  (export `ANTHROPIC_API_KEY` before running.)

- **Google Ads placeholder script:**
  Save the service-account JSON as `google-ads-sa.json`, then:
  ```python
  # scripts/test_google_ads_auth.py (create if needed)
  from google.oauth2 import service_account
  CREDS = service_account.Credentials.from_service_account_file("google-ads-sa.json")
  print("Valid until:", CREDS.expiry)
  ```

- **LinkedIn + Meta token expiry:** both tokens expose `expires_in`. Hit the `/debug_token` endpoints to confirm they survive the deploy window.

## 4. Streamlit Secrets TOML Template

Paste into Streamlit Cloud once all fields are filled:

```toml
[anthropic]
api_key = "SK-ANT-..."

[meta]
access_token = "EAA..."
business_account_id = "your_business_id"

[google_ads]
credentials = """
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "",
  "client_id": "",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": ""
}
"""

[tiktok]
access_token = ""
advertiser_id = ""

[linkedin]
access_token = ""
```

## 5. Escalation Rules

- If any owner cannot supply a key within 24h, log the blocker in `DEPLOYMENT_LOG.md` and notify #activity with owner + dependency.
- If partial credentials arrive, populate what you have and rerun `validate_secrets.py`; the script will list exactly which keys remain missing.
- Keep `scripts/validate_secrets.py` updated whenever new providers are added.

---
This document should live next to the deployment plan so anybody picking up the work can finish secrets collection without DM archaeology.
