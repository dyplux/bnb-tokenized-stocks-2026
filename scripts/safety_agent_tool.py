#!/usr/bin/env python3
"""One JSON-in/JSON-out read-only policy tool for a local agent runtime."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.safety_service import review, validate  # noqa: E402


def main(review_fn=review):
    raw = sys.stdin.buffer.read(4097)
    if len(raw) > 4096:
        print(json.dumps({"error": "Action request exceeds 4 KB"}))
        return 2
    try:
        request = json.loads(raw)
        validate(request)
    except (ValueError, UnicodeDecodeError) as exc:
        print(json.dumps({"error": str(exc)[:160]}))
        return 2
    try:
        result = review_fn(request)
    except Exception as exc:
        print("Safety tool failed: %s" % type(exc).__name__, file=sys.stderr)
        print(json.dumps({"error": "Live source unavailable; no policy decision was made"}))
        return 3
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
