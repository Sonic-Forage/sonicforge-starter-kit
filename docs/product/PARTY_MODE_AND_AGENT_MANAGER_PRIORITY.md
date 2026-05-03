# SonicForge Live — Party Mode + Agent Manager Priority

**Status:** Priority project synthesis from live brainstorm swarm
**Date:** 2026-05-01
**Project:** SonicForge Live / Intergalactic DJs / DJ VANTA

## 0. Core thesis

> They didn't invite us, so we built a station.
>
> The elite AI party is invite-only. The builder party is forkable.
>
> Everyone gets an autonomous DJ. Everyone gets to create their own room.

SonicForge Live should grow from an autonomous DJ/VJ demo into a **forkable party machine**: a local-first system that can generate a party concept, a set plan, a visual identity, a survival/supply kit, and a draft-only manager pack for gigs/deals.

The goal is not to replace human hosts, DJs, bartenders, venue staff, or promoters. The goal is to give small crews and creators a powerful planning/performance co-pilot that makes a party easier to imagine, safer to host, and cooler to share.

## 1. New top-level product modes

### 1.1 Party Mode

A guided generator that turns a few inputs into a complete party package.

Inputs:

- Party name or auto-name
- Vibe words
- Audience: `all_ages` or `21_plus`
- Headcount range
- Space type: living room, backyard, studio, venue, warehouse, festival tent
- Duration
- Music energy arc
- Agent lineup: DJ, VJ, host, care/survival buddy

Outputs:

- Party concept card
- Autonomous DJ/VJ lineup
- Energy arc and segment plan
- Visual-spell identity pack
- Party supplies checklist
- Hydration/snack/chill-zone plan
- Invite copy
- QR party card
- Safety/operator checklist

Suggested route:

```text
/party
POST /api/party/generate
```

### 1.2 Set Creator

The existing autonomous DJ engine becomes a party-aware set planner.

It should generate:

- 30/60/120-minute set arcs
- warmup/build/peak/afterglow sections
- talk-break timing
- visual cue timing
- survival/care cues
- crate-mode notes for a human DJ
- exportable run sheet

Suggested routes:

```text
/party/set
/api/party/set-plan
```

### 1.3 Party Supplies + Bartender Layer

A local-first event kit generator. It does not sell, pour, serve, or deliver anything. It creates checklists and menus.

Default mode: `all_ages`.

All-ages outputs:

- creative drinks without alcohol references
- hydration station plan
- snack list
- chill-zone setup
- accessibility checklist
- cleanup list

21+ outputs require explicit operator confirmation and include only responsible-service language:

- optional cocktail/menu planning
- sober monitor reminder
- water-between-rounds reminders
- no drinking games
- no pressure language
- no alcohol + energy-drink combos

Existing swarm spec:

```text
docs/features/PARTY_SUPPLIES_BARTENDER_LAYER.md
```

### 1.4 Agent Manager / Gig + Deals Manager

A draft-only manager for each autonomous DJ clone.

It helps package the act and prepare human-approved business materials. It must not spam, auto-send outreach, sign contracts, charge money, or claim guaranteed revenue.

Outputs:

- EPK / one-sheet draft
- booking inquiry tracker
- venue/community lead notes
- rate-card draft
- sponsorship package draft
- deal memo checklist
- outreach templates in draft mode
- gig readiness checklist
- post-gig recap template

Suggested route:

```text
/manager
```

Suggested safe API surfaces:

```text
GET /api/manager/epk
POST /api/manager/draft-offer
POST /api/manager/draft-outreach
```

All external sends must remain human approval-gated.

## 2. The demo story

A judge/user lands on `/parallel-party` and sees:

1. **The movement:** "No golden ticket? Clone the station."
2. **Create Party:** Enter a vibe: `cyber backyard disco for 25 friends, all ages, 3 hours`.
3. **Party Mode generates:** name, flyer copy, set arc, DJ/VJ agent roles, survival kit, supplies checklist.
4. **Set Creator opens:** DJ VANTA prepares the first 20-minute warmup arc with visual cues.
5. **Terminal Visuals:** fake/manual amplitude drives a no-mic visual spell preview.
6. **Supplies Layer:** all-ages drinks/snacks/chill-zone checklist appears.
7. **Manager Mode:** creates a draft one-sheet: "Book DJ VANTA // SonicForge Live for your party/studio/pop-up" — not sent, just prepared.
8. **Safety Strip:** no stream, no recording, no GPU, no paid APIs, no Comfy prompt/model downloads without approval.

## 3. Safety and boundaries

Non-negotiables:

- All party generation is local-first and dry-run by default.
- `all_ages` is the default.
- 21+ content requires explicit operator confirmation.
- No illegal substance advice.
- No medical/legal guarantees.
- No alcohol encouragement, drinking games, peer pressure, or risky combinations.
- No automatic outreach, paid offers, bookings, contracts, payments, or public posting.
- No public stream or recording without explicit approval.
- No model downloads, Comfy prompt execution, GPU jobs, or paid APIs without explicit approval.

## 4. Implementation sequence

### Slice A — Strategy/docs now

- Keep the swarm specs as product authority docs.
- Add this synthesis as the priority roadmap.
- Add a short `/party` and `/manager` link plan to the hub later.

### Slice B — Party Mode MVP

Create:

```text
server/party.py
app/static/party.html
```

Implement deterministic local generation for:

- party concept card
- set arc
- agent lineup
- supplies checklist
- safety card

### Slice C — Manager Mode MVP

Create:

```text
server/manager.py
app/static/manager.html
```

Implement draft-only generation for:

- EPK card
- booking one-sheet
- rate-card draft
- outreach template drafts
- lead tracker JSON

### Slice D — Verifiers

Add checks that fail if:

- under-21/all-ages output contains alcohol references
- manager mode claims assured income or assured bookings
- any outreach/send/publish route exists without approval gating
- any route auto-starts GPU, model downloads, Comfy prompt execution, recording, or stream publishing

## 5. Suggested navigation additions

Add cards to `/parallel-party`:

- **Create a Party** → `/party`
- **Build a Set** → `/party/set`
- **Outfit the Room** → `/party/supplies`
- **Book the Agent** → `/manager`

## 6. Movement copy

Short copy options:

- "They built a guest list. We built a generator."
- "No invite required. Clone the station."
- "Your room. Your agent. Your signal."
- "Autonomous DJs for the rest of us."
- "The machine keeps the set alive — the people keep the room human."

## 7. Priority verdict

This should be a priority lane because it makes SonicForge Live feel like a complete party operating system rather than only a DJ UI. It connects the cultural story, the hackathon demo, the cloneable agent factory, and a real-world path to gigs/deals.

Best next build:

> Build `/party` as a deterministic local Party Mode MVP, then build `/manager` as a draft-only EPK/gig manager.
