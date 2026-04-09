"""Quick smoke test for Google Ads service-account credentials.

Usage:
    python scripts/test_google_ads_auth.py [path_to_json]

If no path is provided the script looks for `google-ads-sa.json` in the repo
root. The script does not call the Ads API — it simply verifies that the JSON
is valid, lists its client email, and confirms that an access token can be
requested for the Google Ads scope.
"""
from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path

from google.oauth2 import service_account

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATH = PROJECT_ROOT / "google-ads-sa.json"
SCOPE = "https://www.googleapis.com/auth/adwords"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "creds",
        nargs="?",
        default=str(DEFAULT_PATH),
        help="Path to the Google Ads service-account JSON",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    json_path = Path(args.creds)
    if not json_path.exists():
        print(f"[ERROR] Credentials file not found: {json_path}")
        print("Create the service account JSON and save it locally first.")
        return 1

    creds = service_account.Credentials.from_service_account_file(
        json_path, scopes=[SCOPE]
    )
    scoped = creds.with_scopes([SCOPE])

    from google.auth.transport.requests import Request  # local import to avoid cost when unused

    try:
        scoped.refresh(Request())
    except Exception as exc:  # pragma: no cover - network call is optional
        print(f"[WARN] Token refresh failed: {exc}")
        print("Verify that the service account has Google Ads API access enabled.")
        return 2

    expiry = scoped.expiry or dt.datetime.utcnow()
    print("[OK] Service account authenticated")
    print(f"  • Client email: {creds.service_account_email}")
    print(f"  • Token valid until: {expiry.isoformat()}Z")
    print(f"  • Scope: {SCOPE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
