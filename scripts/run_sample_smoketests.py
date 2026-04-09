"""Run CSV schema smoke tests using the sample data set."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.csv_processor import process_upload  # noqa: E402

SAMPLES = {
    "insights": PROJECT_ROOT / "samples" / "insights_sample.csv",
    "budget": PROJECT_ROOT / "samples" / "budget_sample.csv",
    "creative": PROJECT_ROOT / "samples" / "creative_sample.csv",
    "audience": PROJECT_ROOT / "samples" / "audience_sample.csv",
    "forecast": PROJECT_ROOT / "samples" / "forecast_sample.csv",
}


def main() -> int:
    failures = []
    for copilot, path in SAMPLES.items():
        if not path.exists():
            failures.append((copilot, f"Sample file missing: {path}"))
            continue
        df = pd.read_csv(path)
        result = process_upload(df, copilot)
        if not result.get("valid"):
            failures.append((copilot, result.get("errors", "unknown error")))
            print(f"[FAIL] {copilot}: {failures[-1][1]}")
        else:
            rows = result.get("rows")
            print(f"[OK] {copilot}: {rows} rows validated (dropped {result.get('dropped_rows')})")
    if failures:
        print("\nSummary: failures detected ->")
        for copilot, error in failures:
            print(f" - {copilot}: {error}")
        return 1
    print("All sample smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
