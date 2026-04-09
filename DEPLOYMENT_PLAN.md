# Copilot Suite — Streamlit Cloud Deployment Plan

_Last updated: 2026-04-08_

## 1. Current Status
- **Codebase:** `copilot-suite/` repo (clean working tree, main branch aligned with `origin/main`).
- **Requirements:** `requirements.txt` already includes Streamlit 1.32+, pandas 2.2+, Anthropic, OpenAI, dotenv, Pydantic, Requests, PyArrow, SQLAlchemy.
- **Config:** `.streamlit/config.toml` defines a dark theme and headless server settings. `.streamlit/secrets.toml.example` outlines all required API keys.
- **App entry point:** `app.py` (single-page Streamlit app with sidebar navigation for six copilots).

## 2. Outstanding Pre-Deploy Work
1. **Verify large-file push reliability**
   - Past note mentioned `git http.postBuffer` errors on push. Before pushing, bump buffer and enable HTTP/2 if needed:
     ```bash
     git config --global http.postBuffer 524288000      # 500 MB buffer
     git config --global http.version HTTP/1.1          # fallback if HTTP/2 flaky
     git config --global http.lowSpeedLimit 0
     git config --global http.lowSpeedTime 999999
     ```
   - Confirm `git push origin main` succeeds from this repo after the change.
2. **Secrets staging** — collect production API keys/tokens for:
   - `anthropic.api_key`
   - `meta.access_token`, `meta.business_account_id`
   - `google_ads.credentials` (service account JSON)
   - `tiktok.access_token`, `tiktok.advertiser_id`
   - `linkedin.access_token`
3. **Data directory hygiene**
   - Ensure `uploads/` is empty (git-ignored) before pushing to avoid leaking PII/test files.

## 3. GitHub Push Checklist
1. `cd copilot-suite`
2. `git pull --rebase origin main`
3. Make any final edits and run `python -m compileall` (optional quick syntax check).
4. `git status` should be clean or show intended changes only.
5. Stage and commit: `git add . && git commit -m "Prepare Streamlit deployment"`.
6. Apply postBuffer fix if previous pushes stalled (see above) and run `git push origin main`.
7. Confirm push on GitHub: https://github.com/chrishoppel/copilotsuite

## 4. Streamlit Cloud Deployment Steps
1. Navigate to https://share.streamlit.io → **New app**.
2. Select GitHub repo `chrishoppel/copilotsuite`, branch `main`, and entrypoint `app.py`.
3. **Python version:** Set to 3.11 (matches local environment). Auto-install from `requirements.txt`.
4. **Advanced settings:**
   - Enable **wide mode** (already default via config).
   - Set secrets through UI (copy from `.streamlit/secrets.toml.example`).
   - Optional: configure `streamlit run` command logs to DEBUG for first deploy.
5. Click **Deploy** — first build takes ~2-3 minutes.

## 5. Secrets to Paste in Streamlit Cloud
Use TOML format exactly as below (replace placeholders):
```toml
[anthropic]
api_key = "sk-ant-..."

[meta]
access_token = "..."
business_account_id = "..."

[google_ads]
credentials = """
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
"""

[tiktok]
access_token = "..."
advertiser_id = "..."

[linkedin]
access_token = "..."
```

## 6. Post-Deploy Validation
1. Load the app URL and verify sidebar navigation + dashboard metrics render without errors.
2. Use the **Insights** copilot with a sample CSV (stored under `uploads/` locally) to confirm:
   - CSV upload + validation works (`src/csv_processor.py`).
   - Claude call succeeds (requires Anthropic key in secrets).
3. Run each copilot briefly to ensure prompt templates resolve (no missing files / KeyErrors).
4. Check approval workflow UI:
   - Transition from `GENERATING → PENDING_REVIEW → APPROVED/REJECTED` using dummy data.
5. Verify logs in Streamlit Cloud for any missing dependency errors.
6. Document the production URL in `copilot-suite/README.md` (Deployment section) once confirmed.

### Copilot-specific smoke tests
| Copilot | Sample file | Expected result |
|---------|-------------|-----------------|
| Insights | `samples/insights_sample.csv` | Upload succeeds, anomaly recap mentions Meta CTR uptick + TikTok drop. |
| Budget | `samples/budget_sample.csv` | Recommendations shift $10k from TikTok → Google, highlight over-investment on Meta. |
| Creative | `samples/creative_sample.csv` | Fatigue index ranks Video Prospect as “Warning”, UGC as “Safe”. |
| Audience | `samples/audience_sample.csv` | Flags Lookalike 1% as under-invested with opportunity notes. |
| Forecast | `samples/forecast_sample.csv` | Generates 30/60/90 projections + scenario comparison table. |

7. Run `python scripts/run_sample_smoketests.py` locally after any schema change to guarantee CSV readiness before uploading.

## 7. Next Automation Ideas
- Add GitHub Action to run `streamlit config show` + lint before deploy.
- Schedule nightly health check hitting the Streamlit URL and logging status to `data/uptime.json`.
- Create Discord #activity hook that posts when deployments complete (needs webhook + minimal bot message).

---
_This plan is ready to execute. Once the git push succeeds, proceed directly to Streamlit Cloud deployment and capture validation notes in `copilot-suite/DEPLOYMENT_LOG.md`._
