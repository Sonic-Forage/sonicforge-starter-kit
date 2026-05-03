# SonicForge Live — Draft-Only DJ Agent Manager

**Status:** Product concept / safety-gated revenue lane
**Date:** 2026-05-01
**Project:** SonicForge Live / Intergalactic DJs / DJ VANTA

## 1. Purpose

The DJ Agent Manager is the business-side co-pilot for a SonicForge autonomous DJ/VJ clone. It helps package the act, prepare materials, track opportunities, and draft outreach — while keeping all external actions human-approved.

It answers:

- What is this autonomous DJ act?
- What can it perform?
- What does a small venue, party host, brand, or community need to know?
- What assets do we need before pitching?
- What gigs/leads are worth pursuing?
- What deal terms should a human review?

It does **not** automatically contact people, sign contracts, accept money, claim guaranteed bookings, or make public posts.

## 2. Core modules

### 2.1 EPK Builder

Generates a draft electronic press kit for each agent.

Sections:

- Act name
- One-line pitch
- Bio
- Sonic identity
- Visual identity
- Demo links/placeholders
- Technical requirements
- Safety/local-first note
- Contact placeholder
- Booking status

### 2.2 Gig Readiness Checklist

A pass/fail checklist before trying to book anything.

Items:

- Demo route works locally
- Hero art exists
- Set mode demo works
- Safety policy visible
- Human operator identified
- No accidental stream/recording
- Rate card reviewed by human
- Venue requirements reviewed by human

### 2.3 Lead Tracker

A local JSON/CSV tracker for possible gigs.

Fields:

```json
{
  "lead_name": "Community art night",
  "type": "venue | house_party | studio | festival | brand | online_event",
  "status": "idea | researched | ready_to_contact | contacted_by_human | negotiating | won | lost",
  "fit_notes": "Why this fits the agent",
  "risk_notes": "Noise, age, alcohol, licensing, safety, venue constraints",
  "next_human_action": "Ask organizer if they want a 20-minute autonomous VJ/DJ demo"
}
```

### 2.4 Draft Outreach Studio

Creates draft messages only.

Templates:

- venue inquiry
- house-party host note
- creative studio demo invite
- sponsor/brand concept
- festival side-stage pitch
- community Discord/event pitch

All drafts should include:

- clear human sender
- no fake claims
- no pressure
- no spam automation
- ask permission before sending media/files

### 2.5 Deal Memo Draft

A checklist for human review:

- date/time
- venue/location
- duration
- setup requirements
- operator responsibilities
- payment or barter terms
- recording/streaming permissions
- alcohol/all-ages constraints
- cancellation/weather/noise plan
- equipment/liability boundaries

## 3. Safe route proposal

```text
/manager
/api/manager/epk
/api/manager/readiness
/api/manager/draft-outreach
/api/manager/deal-memo
```

Every endpoint returns drafts or local checklists only.

No endpoint sends email, DMs, posts, invoices, accepts payment, signs anything, scrapes private data, or stores credentials.

## 4. First demo flow

1. Open `/agents` and choose `DJ VANTA`.
2. Click **Open Manager**.
3. Manager shows:
   - readiness score
   - EPK draft
   - booking one-sheet
   - draft outreach template
   - deal memo checklist
4. User clicks **Generate pitch for art-house party**.
5. App creates a draft only:
   > "Here is a 20-minute autonomous DJ/VJ demo concept. Human operator present. No recording or public stream unless approved."
6. Safety footer says:
   > Draft only. Human approval required before sending, pricing, booking, payment, streaming, or recording.

## 5. Revenue posture

Do not promise revenue. Promise readiness and packaging.

Safe language:

- "draft booking kit"
- "gig readiness"
- "outreach prep"
- "deal memo checklist"
- "operator approval required"

Avoid:

- guaranteed gigs
- guaranteed money
- automated booking
- auto-DMs
- spam campaigns
- legal advice
- tax advice

## 6. Why it matters

Party Mode makes the event. Manager Mode helps the agent leave the laptop and become a real act people can invite, book, remix, and clone.

This is the business flywheel:

```text
Create Agent → Create Party → Record Local Demo Assets → Build EPK → Draft Outreach → Human Sends → Gig → New Party Proof → Better Agent
```

## 7. Build priority

After `/party`, build `/manager` as a draft-only static/deterministic MVP. It will make SonicForge feel less like a toy and more like an autonomous performer factory with a path into real-world events.
