"""
notify_email_entry.py — ETPK Email Notifier

Sends structured notifications to all configured emails.
One call = one email fanned out to luvyoukid@proton.me, huatdeck@gmail.com,
elinatan@gmail.com, jimishun@proton.me.

Usage:
  python notify_email_entry.py send \
    --event-type "repo_change" \
    --summary "zo-space force-push on main" \
    --severity "warning" \
    --details '{"repo": "zo-space", "branch": "main", "actor": "MiniMax 2.7"}'

  python notify_email_entry.py heartbeat

  python notify_email_entry.py digest
"""

import os
import smtplib
import sys
import json
import argparse
from email.mime.text import MIMEText
from datetime import datetime, timedelta

SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
NOTIFY_EMAILS = os.environ.get(
    "NOTIFY_EMAILS",
    "luvyoukid@proton.me;huatdeck@gmail.com;elinatan@gmail.com;jimishun@proton.me"
)
NOTIFY_FROM = os.environ.get("NOTIFY_FROM", SMTP_USER)
RUN_LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "docs", "run-log.md")


def send_notify(event_type: str, summary: str, severity: str = "info", details=None) -> dict:
    recipients = [e.strip() for e in NOTIFY_EMAILS.split(";") if e.strip()]
    if not recipients:
        return {"ok": False, "error": "No recipients configured"}
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASS:
        return {"ok": False, "error": "SMTP env vars not set (SMTP_HOST, SMTP_USER, SMTP_PASS)"}

    subject = f"[ETPK][{severity.upper()}] {event_type} – {summary}"
    body = f"[ETPK] Notification\n{'='*40}\nType: {event_type}\nSeverity: {severity}\nTime: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\nSummary: {summary}"
    if details:
        body += f"\n\nDetails:\n{json.dumps(details, indent=2)}"

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = NOTIFY_FROM
    msg["To"] = ", ".join(recipients)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
            s.starttls()
            s.login(SMTP_USER, SMTP_PASS)
            s.sendmail(NOTIFY_FROM, recipients, msg.as_string())
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def send_heartbeat() -> dict:
    return send_notify(
        event_type="hourly_heartbeat",
        summary="MiniMax 2.7 + Zo heartbeat: system alive, monitoring repos/skills/jobs.",
        severity="info",
        details=None
    )


def send_digest() -> dict:
    try:
        if not os.path.exists(RUN_LOG_PATH):
            return {"ok": False, "error": f"Run log not found: {RUN_LOG_PATH}", "event_count": 0}

        with open(RUN_LOG_PATH) as f:
            lines = f.readlines()

        cutoff = datetime.utcnow() - timedelta(hours=1)
        recent = []
        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 8:
                continue
            try:
                ts = datetime.strptime(parts[0].strip(), "%Y-%m-%d %H:%M")
                if ts >= cutoff:
                    recent.append(line.strip())
            except ValueError:
                continue

        if not recent:
            return {"ok": True, "event_count": 0, "note": "No events in last hour — no email sent"}

        summary = f"{len(recent)} event(s) in the last hour:\n\n" + "\n".join(recent)
        return send_notify(
            event_type="hourly_digest",
            summary=f"Hourly digest: {len(recent)} event(s)",
            severity="info",
            details={"events": recent}
        )
    except Exception as e:
        return {"ok": False, "error": str(e), "event_count": 0}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ETPK Email Notifier")
    sub = parser.add_subparsers(dest="cmd")

    p_send = sub.add_parser("send", help="Send a custom notification")
    p_send.add_argument("--event-type", required=True)
    p_send.add_argument("--summary", required=True)
    p_send.add_argument("--severity", default="info")
    p_send.add_argument("--details", default="{}")

    sub.add_parser("heartbeat", help="Send hourly heartbeat")
    sub.add_parser("digest", help="Send hourly digest from run-log")

    args = parser.parse_args()

    if args.cmd == "send":
        details = json.loads(args.details) if args.details else None
        result = send_notify(args.event_type, args.summary, args.severity, details)
    elif args.cmd == "heartbeat":
        result = send_heartbeat()
    elif args.cmd == "digest":
        result = send_digest()
    else:
        parser.print_help()
        sys.exit(0)

    print(json.dumps(result, indent=2))
    sys.exit(0 if result.get("ok") else 1)
