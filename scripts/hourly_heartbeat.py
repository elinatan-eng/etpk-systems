#!/usr/bin/env python3
"""
hourly_heartbeat.py — ETPK Hourly Heartbeat + Digest

Call send_notify for heartbeat every hour.
If events exist in run-log from the last hour, include a digest.

Usage:
  python hourly_heartbeat.py              # heartbeat only
  python hourly_heartbeat.py --digest    # heartbeat + digest (skip if no events)
  python hourly_heartbeat.py --digest-only  # digest only (skip if no events)
"""

import os
import sys
import argparse

# Add skills/notify-email to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "skills", "notify-email"))
from notify_email_entry import send_notify, send_heartbeat, send_digest

LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "heartbeat.log")


def log(msg: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    ts = __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    line = f"[{ts}] {msg}\n"
    with open(LOG_FILE, "a") as f:
        f.write(line)
    print(line.strip())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digest", action="store_true", help="Also send digest if events exist")
    parser.add_argument("--digest-only", action="store_true", help="Only send digest, skip plain heartbeat")
    args = parser.parse_args()

    if args.digest_only:
        r = send_digest()
        if r.get("ok"):
            log(f"digest sent: {r.get('event_count', 0)} events")
        else:
            log(f"digest skipped: {r.get('error', r.get('note', 'unknown'))}")
    else:
        r = send_heartbeat()
        if r.get("ok"):
            log("heartbeat sent OK")
        else:
            log(f"heartbeat FAILED: {r.get('error')}")
            sys.exit(1)

        if args.digest:
            r2 = send_digest()
            if r2.get("ok"):
                if r2.get("event_count", 0) > 0:
                    log(f"digest sent: {r2.get('event_count')} events")
                else:
                    log("digest: no events in last hour, skipped")
            else:
                log(f"digest error: {r2.get('error')}")
