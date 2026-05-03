# SonicForge Live — PLUR + Kandi + RFID Station Concept

**Status:** Product brainstorm / priority addendum
**Date:** 2026-05-01
**Project:** SonicForge Live / Intergalactic DJs / DJ VANTA

## 0. North Star

Bring the real rave/community heart into SonicForge Live:

> Peace. Love. Unity. Respect. Remix.
>
> Every person gets a signal. Every signal carries care.

The Kandi Station turns SonicForge from "AI DJ app" into a ritual space: guests create or receive a bracelet/token, opt into a local party identity, tap it at stations, unlock visuals, trade moments, and carry the memory home.

This should feel like a cyber-rave friendship bracelet table crossed with a local-first access badge, not a tracking device.

## 1. PLUR as system values

### Peace

System behavior:

- calm down / chill-zone cues
- conflict de-escalation copy
- low-stimulation visual mode
- quiet corner signage
- ride/home plan reminders

UI ideas:

- `Peace Pulse` station: tap Kandi to request a softer moment / chill-zone reminder
- visual overlay: blue/green breathing wave
- DJ VANTA line: "Peace check — if the room is too hot, the chill portal is open."

### Love

System behavior:

- positive shoutouts
- birthday/celebration moments
- gratitude wall
- no harassment/no pressure defaults

UI ideas:

- `Love Note` station: tap Kandi and select/send a preset appreciation message to the party wall
- visual overlay: heart-shaped waveform, but not cheesy — neon signal glyphs
- DJ VANTA line: "Love signal received. Somebody in this room is glad you showed up."

### Unity

System behavior:

- group quests
- collaborative set voting
- shared visual triggers
- all-ages inclusivity
- accessibility reminders

UI ideas:

- `Unity Chain`: when multiple Kandi pieces tap within 30 seconds, unlock a group visual spell
- `Circle Moment`: four people tap P/L/U/R pieces to activate a PLUR visual
- DJ VANTA line: "Unity chain online — the room just became the instrument."

### Respect

System behavior:

- consent reminders
- photography/recording preferences
- personal-space reminders
- age-mode boundaries
- safe exit/ride cues

UI ideas:

- Kandi preference tags: `no photos`, `ask first`, `quiet mode`, `open to trade`
- `Respect Reminder`: visible event norms on party screen
- DJ VANTA line: "Respect the signal: ask first, listen always, keep the floor kind."

### Remix

Add SonicForge's fifth value for the builder culture.

System behavior:

- cloneable party templates
- remixable agent personalities
- reusable visual spells
- open-builder energy

UI ideas:

- `Remix Token`: Kandi tap unlocks a downloadable party template or agent variant
- `Fork the Floor`: QR card points to repo/setup route
- DJ VANTA line: "No velvet rope. Fork the station. Remix the night."

## 2. Kandi Station physical concept

A table or side-station at the party with:

- beads / string / elastic
- printed PLUR glyph cards
- optional NFC/RFID tags embedded in or attached to Kandi
- QR code linking to local party page
- clear privacy sign
- all-ages-safe drink/snack/chill-zone signage nearby

Station roles:

1. **Create:** guests make or choose Kandi.
2. **Name:** optional local nickname or generated codename.
3. **Choose values:** Peace / Love / Unity / Respect / Remix.
4. **Opt in:** choose what the Kandi can do.
5. **Tap:** unlock local party interactions.
6. **Trade:** human ritual remains the point; tech should support, not replace it.

## 3. RFID/NFC Kandi interactions

Use NFC/RFID as a local party token.

Safe defaults:

- no personal data required
- no legal name required
- no phone number/email required
- no location tracking
- no persistent cross-party identity by default
- token can be reset/wiped
- party host can run completely offline/local

Possible interactions:

### 3.1 Tap to join the party signal

Guest taps Kandi at `/kandi` station.

Output:

- local codename: `NEON-MANTA-07`
- selected PLUR value
- color palette
- optional avatar glyph
- guest sees: "You are now part of the signal."

### 3.2 Tap to affect visuals

Each Kandi has a visual spell binding:

- Peace: soft waves / lower intensity
- Love: warm bloom / gratitude pulse
- Unity: group constellation / linked nodes
- Respect: boundary ring / calm reminder
- Remix: glitch burst / clone/fork motif

### 3.3 Tap to vote safely

Guests can vote on party direction without phones:

- more energy
- less energy
- more vocals
- deeper groove
- chill break
- lights down

DJ VANTA uses the aggregate as crowd-reading input, not absolute command.

### 3.4 Tap for care requests

Optional safety/care interactions:

- water reminder
- chill-zone request
- buddy-check ping
- lower brightness / softer mode

This should be anonymous or aggregate by default.

### 3.5 Tap to trade

Two Kandi pieces tap together to log a local "trade moment":

```json
{
  "type": "kandi_trade",
  "tokens": ["local_token_a", "local_token_b"],
  "timestamp": "local_party_time",
  "values": ["Love", "Respect"]
}
```

No identity needed. The party wall can show:

> 12 Kandi trades. 4 Unity chains. 2 Peace pulses.

## 4. App surfaces

Suggested routes:

```text
/kandi
/kandi/station
/kandi/wall
/api/kandi/register
/api/kandi/tap
/api/kandi/visual-cue
/api/kandi/reset
```

### `/kandi` page

A visually rich explanation page:

- What is Kandi?
- What is PLUR?
- How SonicForge uses it respectfully
- Privacy/safety defaults
- How to make a token
- How to trade

### `/kandi/station` page

Operator UI:

- scan/tap token
- assign color/value
- choose mode: anonymous / nickname
- write local token manifest
- print/display mini card

### `/kandi/wall` page

Public party display:

- PLUR meter
- active values
- trade count
- Unity chain moments
- gratitude wall
- care reminders
- visual spell queue

## 5. Data model sketch

```json
{
  "token_id_hash": "local_hash_only",
  "party_id": "local_party_id",
  "codename": "NEON-MANTA-07",
  "plur_value": "unity",
  "color": "cyan-magenta",
  "visual_spell": "constellation_chain",
  "preferences": {
    "photo_status": "ask_first",
    "trade_status": "open_to_trade",
    "intensity": "standard"
  },
  "created_at": "local_time",
  "expires_after_party": true
}
```

Privacy rule: store only a local hash or generated internal ID, never raw UID in exported/shareable files if avoidable.

## 6. Hardware options

### MVP — no hardware

Use QR tokens first:

- printable Kandi cards
- phone scans local QR
- manual tap button in UI
- works for hackathon/demo immediately

### Next — cheap NFC stickers/cards

Use NFC tags that open local party URL with token code.

Pros:

- easy to demo
- guests can tap phones
- no special reader needed for many flows

### Later — RFID reader

Use USB NFC/RFID reader at the Kandi Station.

Pros:

- more magical booth experience
- physical tap ritual
- faster party-wall interactions

Gates:

- no hidden tracking
- visible privacy sign
- opt-in only
- reset/wipe option

## 7. Demo flow

1. Host opens `/party` and creates "Cyber Backyard Unity Jam".
2. App suggests a Kandi Station in the supply checklist.
3. Host opens `/kandi/station`.
4. Guest creates Kandi and chooses `Unity`.
5. Station assigns `NEON-MANTA-07` and cyan/magenta visual spell.
6. Guest taps Kandi.
7. `/kandi/wall` lights up: "Unity signal joined."
8. Four guests tap in sequence — visual spell triggers a constellation overlay.
9. DJ VANTA says: "Unity chain online — the room just became the instrument."
10. Party ends; host can export anonymous party memory card.

## 8. Safety copy

Display at the station:

> Kandi is for connection, not tracking. This station stores local party tokens only. No legal names, phone numbers, emails, or location data are required. You can reset your token anytime.

For all-ages:

> This party mode is all-ages. Drinks and supplies are creative, non-alcoholic, and hydration-forward.

For 21+:

> 21+ content is planning-only and must be handled by responsible adults according to local rules. SonicForge does not serve, sell, or encourage alcohol use.

## 9. Why this is powerful

This makes SonicForge feel alive in the physical room:

- The DJ/VJ reacts to the crowd without cameras or microphones.
- Guests become participants, not spectators.
- PLUR becomes operational, not decorative.
- Kandi becomes a safe, opt-in local controller.
- The party produces a memory artifact guests can take home.

## 10. Build priority

Recommended next slices:

1. Add `/kandi` concept page.
2. Add Kandi Station to `/party/supplies` checklist.
3. Add QR-token MVP before real RFID hardware.
4. Add `/kandi/wall` with fake/manual tap demo.
5. Later integrate NFC/RFID reader behind explicit hardware approval.
