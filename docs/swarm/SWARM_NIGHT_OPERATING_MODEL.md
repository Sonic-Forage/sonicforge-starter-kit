# Swarm Night Operating Model

A "swarm night" means small safe agents keep improving docs, setup, tests, packaging, and reports while the human sleeps.

## Allowed unattended work

Docs/onboarding improvements, verifier/script hardening, local-only manifests, static status JSON, secret scans, git commits/pushes to approved repos, and wake-up reports.

## Forbidden unattended work

Cron jobs must not create/update/remove cron jobs. No GPU jobs, paid APIs, public posting, private media uploads, model training, secret changes, token printing, or deletion outside approved workspace.

## Agent roles

Orchestrator, Builder, QA Sentinel, GitHub Guardian, and Creative Alchemist.

## Handoff format

Every run should report status, files changed, verification, commit/push result, and next best step.
