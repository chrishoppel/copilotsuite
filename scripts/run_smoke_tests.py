"""Run CSV validation smoke tests using the sample data kit."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SAMPLES_DIR = PROJECT_ROOT / "samples"

sys.path.insert(0, str(PROJECT_ROOT))
from src.csv_processor import process_upload  # noqa: E402

SAMPLES = {
    "insights": "insights_sample.csv",
    "budget": "budget_sample.csv",
    "creative": "creative_sample.csv",
    "audience": "audience_sample.csv",
    "forecast": "forecast_sample.csv",
}


def main() -> int:
    failures = []
    for copilot, filename in SAMPLES.items():
        path = SAMPLES_DIR / filename
        if not path.exists():
            failures.append(f"{copilot}: sample file missing ({path})")
            continue
        df = pd.read_csv(path)
        result = process_upload(df, copilot)
        if not result.get("valid"):
            failures.append(f"{copilot}: {result.get('errors')}")
        else:
            print(f"[OK] {copilot.title()} → {result['rows']} rows (dropped {result['dropped_rows']})")
    if failures:
        print("\n[FAIL] Issues detected:")
        for issue in failures:
            print(f" - {issue}")
        return 1
    print("\nAll sample datasets validated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
