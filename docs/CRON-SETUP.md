# ETPK Cron Setup — Hourly Heartbeat + Digest

## Option A: Zo Computer Automations (recommended)

1. Go to [Automations](/?t=automations) in Zo
2. Create a new automation:
   - **Trigger:** Every 1 hour
   - **Action:** Run script
   - **Script path:** `/home/workspace/etpk-systems/scripts/hourly_heartbeat.py`
   - **Args:** `--digest`
3. Save and enable

## Option B: Crontab on the Zo host

```bash
# SSH into your Zo or use Zo Terminal
# Add to crontab:

0 * * * * cd /home/workspace/etpk-systems && \
  python scripts/hourly_heartbeat.py --digest >> logs/heartbeat.log 2>&1

# Alternative: digest only (skip if no events)
0 * * * * cd /home/workspace/etpk-systems && \
  python scripts/hourly_heartbeat.py --digest-only >> logs/heartbeat.log 2>&1
```

## Option C: GitHub Actions (if Zo cron not available)

```yaml
# .github/workflows/heartbeat.yml
name: Hourly Heartbeat

on:
  schedule:
    - cron: "0 * * * *"  # Every hour at :00
  workflow_dispatch:       # Also allow manual trigger

jobs:
  heartbeat:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: python-version: "3.11"
      - run: pip install -r etpk-systems/skills/notify-email/requirements.txt
      - run: python etpk-systems/scripts/hourly_heartbeat.py --digest
        env:
          SMTP_HOST: ${{ secrets.SMTP_HOST }}
          SMTP_PORT: ${{ secrets.SMTP_PORT }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASS: ${{ secrets.SMTP_PASS }}
          NOTIFY_EMAILS: ${{ vars.NOTIFY_EMAILS }}
```

## Required environment variables

Set these in Zo [Settings > Advanced](/?t=settings&s=advanced) under **Secrets**:

| Variable | Value |
|----------|-------|
| `SMTP_HOST` | Your SMTP server (e.g. smtp.gmail.com) |
| `SMTP_PORT` | 587 (TLS) or 465 (SSL) |
| `SMTP_USER` | Your SMTP username/email |
| `SMTP_PASS` | Your SMTP app password |
| `NOTIFY_EMAILS` | `luvyoukid@proton.me;huatdeck@gmail.com;elinatan@gmail.com;jimishun@proton.me` |
| `NOTIFY_FROM` | Sender email (defaults to SMTP_USER) |

## Notification subject format

```
[ETPK][INFO] hourly_heartbeat – MiniMax 2.7 + Zo heartbeat: system alive…
[ETPK][INFO] hourly_digest – Hourly digest: 3 event(s)
[ETPK][WARNING] repo_change – zo-space force-push on main
[ETPK][ERROR] policy_block – Run blocked by policy guardrails
```

## Events that trigger notifications

| Event | Severity | Trigger |
|-------|----------|---------|
| `repo_change` | warning | New repo created or force-pushed |
| `skill_change` | info | Skill manifests or prompts changed |
| `job_complete` | info | Long-running automations finished |
| `job_failed` | error | Batch jobs, pipelines failed |
| `policy_block` | error | Runs blocked by safety/guardrail rules |
| `skill_error` | error | HTTP skill 500s, timeouts, missing files |
| `hourly_heartbeat` | info | System alive (every hour, always) |
| `hourly_digest` | info | Summary of last hour's events |
