"""Quick validator for .streamlit/secrets.toml before deployment.

Usage:
    python scripts/validate_secrets.py [path_to_secrets]

If no path is provided the script checks `.streamlit/secrets.toml`,
falling back to `.streamlit/secrets.toml.example` when the real
secrets file is missing.
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path
from typing import Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SECRETS = PROJECT_ROOT / ".streamlit" / "secrets.toml"
EXAMPLE_SECRETS = PROJECT_ROOT / ".streamlit" / "secrets.toml.example"

REQUIRED_KEYS: Dict[str, List[str]] = {
    "anthropic": ["api_key"],
    "meta": ["access_token", "business_account_id"],
    "google_ads": ["credentials"],
    "tiktok": ["access_token", "advertiser_id"],
    "linkedin": ["access_token"],
}


def load_secrets(path_override: str | None) -> tuple[Path, dict]:
    """Return (path_used, parsed_data)."""
    if path_override:
        candidate = Path(path_override)
    else:
        candidate = DEFAULT_SECRETS if DEFAULT_SECRETS.exists() else EXAMPLE_SECRETS

    if not candidate.exists():
        raise FileNotFoundError(
            "No secrets file found. Create .streamlit/secrets.toml (see example)."
        )

    with candidate.open("rb") as fp:
        data = tomllib.load(fp)
    return candidate, data


def find_missing_keys(data: dict) -> Dict[str, List[str]]:
    missing: Dict[str, List[str]] = {}
    for section, keys in REQUIRED_KEYS.items():
        section_data = data.get(section)
        for key in keys:
            if not section_data or not section_data.get(key):
                missing.setdefault(section, []).append(key)
    return missing


def main() -> int:
    try:
        path_used, secrets = load_secrets(sys.argv[1] if len(sys.argv) > 1 else None)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        return 1

    missing = find_missing_keys(secrets)
    if missing:
        print(f"[WARN] Checked: {path_used}")
        print("Missing keys:")
        for section, keys in missing.items():
            joined = ", ".join(keys)
            print(f"  - [{section}] → {joined}")
        return 2

    print(f"[OK] Secrets file ready: {path_used}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
