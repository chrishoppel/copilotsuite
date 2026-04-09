"""Minimal validator for Google Ads service-account JSON.

Usage:
    python scripts/test_google_ads_auth.py path/to/service_account.json

The script checks for required fields and, if `google-auth` is available,
instantiates credentials to ensure the key is well-formed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import List

REQUIRED_FIELDS: List[str] = [
    "type",
    "project_id",
    "private_key_id",
    "private_key",
    "client_email",
    "client_id",
    "token_uri",
]

try:  # Optional dependency (included in requirements.txt)
    from google.oauth2 import service_account
except Exception:  # pragma: no cover - fall back to structure-only validation
    service_account = None


def load_credentials(path_str: str) -> dict:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Service account file not found: {path}")
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def check_required_fields(data: dict) -> list[str]:
    missing = [field for field in REQUIRED_FIELDS if not data.get(field)]
    return missing


def hydrate_google_auth(data: dict) -> bool:
    if service_account is None:
        print("[WARN] google-auth not available; skipping credential instantiation test.")
        return True
    scopes = [
        "https://www.googleapis.com/auth/adwords",
        "https://www.googleapis.com/auth/cloud-platform",
    ]
    try:
        creds = service_account.Credentials.from_service_account_info(data, scopes=scopes)
    except Exception as exc:  # noqa: BLE001 - surface exact failure reason
        print(f"[ERROR] Unable to instantiate credentials with google-auth: {exc}")
        return False
    print(f"[OK] Credential valid. Client email: {creds.service_account_email}")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_google_ads_auth.py path/to/service_account.json")
        return 1

    try:
        data = load_credentials(sys.argv[1])
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1
    except json.JSONDecodeError as exc:
        print(f"[ERROR] Invalid JSON: {exc}")
        return 1

    missing = check_required_fields(data)
    if missing:
        print(f"[ERROR] Missing required fields: {', '.join(missing)}")
        return 2

    if not hydrate_google_auth(data):
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
