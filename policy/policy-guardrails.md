# ETPK AI Policy & Guardrails v1

## 1. User roles and permissions

- **You (founder)**: may let AI draft, propose, and execute low‑risk actions; high‑risk actions require your explicit review.
- **Teen mode**: AI may answer questions and draft suggestions, but cannot access financial accounts, private repos, or PII beyond what you explicitly paste.
- **Investor view**: read‑only dashboards and reports; AI can summarize and simulate but cannot trigger deploys, transfers, or repo changes.
- **Developer / agent**: can propose code changes, PRs, infra configs; merges/deploys require your approval.

## 2. PII and data handling

- **Redact or mask**: full NRIC, passport, bank account, credit card numbers, exact home address before sending to Workers AI or third‑party models.
- **Allowed unredacted**: public data, anonymized metrics, non‑identifying business data, synthetic examples.
- **Storage**: logs with PII must be minimized, encrypted at rest, and rotated; never store raw IDs in prompt logs.

## 3. Access control (Zero‑Trust)

- All internal dashboards and private models must sit behind Cloudflare Access (SSO, device posture checks).
- No direct public endpoints for admin actions; admin APIs must require Access JWT or equivalent.
- For any "god mode" tools (financial ops, repo admins), require a second factor (e.g. email/OTP confirmation) for irreversible actions.

## 4. Quality and evaluation

- Maintain a prompt test suite for key flows (briefing, alerts, PR review, lease decode) with expected patterns.
- Run these tests after major prompt/model changes; block deploy if regressions appear.
- Enable "shadow mode" for new automations: log AI‑proposed actions without executing for a trial period, compare against what you actually do.
- Capture feedback via "good / bad / correct this" buttons and feed back into prompt tuning.

## 5. Performance and cost controls

- Define daily and monthly budget caps for Workers AI spend; set alerts at 50%, 80%, and 100% of budget.
- Monitor latency, error rates, and queue sizes for cron/background tasks.
- Separate heavy jobs into Queues/Workflows so interactive user requests stay fast.

## 6. Productization practices

- Use feature flags per AI app (distress dashboard, simulators, copilots, teen mode, investor mode) for gradual rollout.
- Design schemas with per‑user / per‑org isolation (multi‑tenant ready) if you onboard others later.
- Document one "high‑risk" action at a time with a yes/no checklist that must pass before allowing full automation (e.g. "star spike email only" or "GitHub issue suggestions").

---

**Next high‑risk action checklist** (complete before full automation):

> Coming soon — specify one action (e.g. "auto‑label GitHub issues" or "auto‑send low‑stakes emails")