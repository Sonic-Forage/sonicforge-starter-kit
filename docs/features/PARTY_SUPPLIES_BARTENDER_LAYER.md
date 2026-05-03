# 🍸 Intergalactic Party Supplies & Bartender Layer

> SonicForge Live — Party OS module
> Design: All-ages safe, age-gated where needed, rave-coded, zero medical/legal overclaims
> Updated: 2026-05-01T19:45:00+00:00

---

## 0. Philosophy

**Why this layer matters:** SonicForge Live is already a DJ/VJ brain and Rave Survival Kit. But the full "party operating system" promise means helping with the *physical room* — the supplies, the drinks, the chill zone, the accessibility plan, the vibe-setting checklist.

This layer turns DJ VANTA from a performer into a **party co-host**: before the event, it helps plan the room. During, it helps with timed supply checks, drink-pairing suggestions, and accessibility reminders. After, it helps with cleanup.

**Core rule:** SonicForge Live never serves, pours, sells, or handles physical drinks or substances. This layer generates **planning documents, checklists, menus, and timed reminders only.** All age-gated content stays behind an explicit age-verification toggle that defaults to **all-ages mode (under-21 safe).**

**Winning sentence:**
> *Intergalactic DJs doesn't replace the bartender, the safety lead, or the host — it outfits them with a rave-ready party plan that runs local and respects every guest.*

---

## 1. Feature Sections

### 1.1 Event Kit Generator

A party-planning questionnaire → auto-generated supply checklist. Think "wedding planner meets warehouse rave."

**Inputs (operator fills in):**
- Party type: `house_party | studio_session | livestream_hang | popup_warehouse | backyard_dance | picnic_rave`
- Guest count range: `1–10 | 10–30 | 30–60 | 60+`
- Duration: `2h | 4h | 6h | all_night`
- Venue: `indoor_apartment | indoor_house | indoor_venue | outdoor_public | outdoor_private | hybrid`
- Age mode (mandatory toggle): `all_ages | 21_plus` ← gate for drink menus, see §2
- Power access: `plentiful | limited | bring_generator`
- Sound: `bluetooth_speaker | home_stereo | small_PA | full_sound_system`
- Lighting: `ambient_only | string_lights | basic_DMX | full_lighting_rig`
- Weather (outdoor): `clear | warm | cool | possible_rain | cold`
- Accessibility notes (free text, operator fills)

**Generated output — Party Plan Pack:**
1. Shopping checklist (see §1.2)
2. Drink menu (see §1.3)
3. Hydration/snack/chill zone setup (see §1.4)
4. Accessibility checklist (see §1.5)
5. Harm-reduction kit reminders (see §1.6)
6. Timeline with timed VANTA supply-check talk-breaks
7. Cleanup checklist

**Implementation:** `/api/party-plan/generate` POST endpoint. Returns a `PartyPlan` object. All dry-run / local-first: no external calls, no store inventory lookups, no purchase links unless operator explicitly adds them.

---

### 1.2 Shopping Checklist

Categorized checkable list generated from the event kit inputs. Always includes:

#### Core (every party)
- [ ] Water station supplies: dispenser, cups, ice, reusable bottles
- [ ] Trash bags (recycling + landfill)
- [ ] Paper towels / cleaning spray
- [ ] Duct tape / gaffer tape (cable management)
- [ ] Extension cords + power strips
- [ ] Phone charging station (multi-USB brick + cables)
- [ ] First-aid kit
- [ ] Earplugs (bulk pack)
- [ ] Sharpie / markers (cup labeling)
- [ ] Paper signage (exits, bathroom, chill zone, consent reminder)

#### Comfort
- [ ] Seating: floor cushions, chairs, blankets
- [ ] Fans or ventilation plan
- [ ] Extra toilet paper
- [ ] Hand soap / sanitizer
- [ ] Tissues / napkins
- [ ] Coats/bags designated area

#### Sound-dependent
- [ ] Extension cord to DJ table
- [ ] Surge protector
- [ ] Backup aux/Bluetooth cable
- [ ] Speaker stands (if PA)

#### Lighting-dependent
- [ ] LED strips / string lights
- [ ] Extension cords to lighting positions
- [ ] Gaff tape for light mounting
- [ ] Dimmer / controller

#### Outdoor-specific
- [ ] Pop-up tent / shade
- [ ] Bug spray / citronella
- [ ] Sunscreen
- [ ] Blankets
- [ ] Weights / stakes for tents
- [ ] Rain plan / tarp
- [ ] Battery-powered lights

#### Cold-weather
- [ ] Heaters (safe placement only)
- [ ] Extra blankets
- [ ] Warm beverage supplies

#### Large party (30+)
- [ ] Extra trash cans
- [ ] Bathroom plan (bring portable if needed)
- [ ] Designated quiet/chill zone with seating
- [ ] Multiple water stations
- [ ] Sound limiter or dB meter
- [ ] Extra first-aid supplies
- [ ] Check-in / wristband system

---

### 1.3 Bartender Layer — Drink Menus

**Two modes, enforced at the data level:**

#### ALL-AGES MODE (default, under-21 safe)
*No alcohol references, no cocktail names that imply alcohol, no "virgin [cocktail]" naming, no glassware or garnish that mimics bar service. This is a standalone creative beverage menu that stands on its own.*

**Menu categories:**
- **Hydration Station** — infused waters, electrolyte mixes, coconut water
- **Sparkling Lab** — soda + juice combos with fun names
- **Hot Corner** — teas, hot chocolate, warm cider (seasonal)
- **Frost Bar** — smoothies, slushies, frozen fruit blends
- **Caffeine Orbit** — coffee, matcha, yerba mate (labeled with caffeine content)

**Example menu items (all-ages):**
| Name | Description | Ingredients | Prep |
|---|---|---|---|
| Portal Pop | Sparkling citrus with edible glitter rim | Lemon-lime soda, orange juice, edible glitter, ice | Pour, stir, serve |
| Nebula Nectar | Blue butterfly pea + lemonade color-shift | Butterfly pea tea (chilled), lemonade, honey, ice | Layer, stir to shift |
| Vanishing Point | Minty cucumber refresher | Cucumber slices, fresh mint, lime, sparkling water, ice | Muddle mint/cucumber, top soda |
| Binary Sunrise | Layered tropical juice | Mango nectar, grenadine, pineapple juice, ice | Layer carefully |
| Gravity Well | Rich hot chocolate with cosmic marshmallows | Whole milk, dark cocoa, vanilla, star-shaped marshmallows | Heat, whisk, top |
| Signal Boost | Electrolyte citrus cooler | Coconut water, lime, salt pinch, agave, ice | Shake, serve |
| Cool-Down Orbit | Ginger-turmeric chill tonic | Ginger tea (chilled), turmeric, honey, lemon, sparkling water | Mix, serve over ice |
| Cosmic Cold Brew | Slow-steep coffee over ice with oat milk float | Cold brew concentrate, oat milk, vanilla, ice | Pour, float oat milk |
| Slush Portal | Mango-passion fruit frozen blend | Frozen mango, passion fruit juice, lime, ice, blender | Blend, serve |
| Pixelade | Berry lemonade with color layers | Blueberry syrup, raspberry syrup, lemonade, ice | Layer, serve with straw |

**Naming rules for all-ages:**
- Space/tech/rave/festival themes only: Portal, Nebula, Signal, Binary, Pixel, Orbit, Cosmos, Transmission, Frequency, Waveform, Vector, Glitch
- No alcohol-adjacent words: no "mocktail", no "virgin", no "-tini", no "-rita", no "bar", no "cocktail", no "drink" in names
- No glassware fetishization: serve in whatever cups the party has

#### 21+ MODE (gated, operator must toggle)
*Must explicitly toggle `age_mode: 21_plus` in the Party Plan Generator. Default remains all-ages. UI shows lock icon and confirmation dialog.*

**Menu categories:**
- **Transmission Cocktails** — spirit-forward, DJ/VJ-themed
- **Frequency Highballs** — long drinks, sessionable
- **Portal Shots** — small-format, celebratory, batch-friendly
- **Orbit Coolers** — wine/beer-based, low-ABV, all-night

**Example menu items (21+):**
| Name | Description | Spirit | Glass |
|---|---|---|---|
| Crossfader | Equal-parts mezcal + Aperol + lime + grapefruit soda | Mezcal | Highball |
| Bass Swap | Dark rum + ginger beer + lime + angostura float | Dark rum | Copper mug |
| Phrase Lock | Gin + elderflower + cucumber + prosecco top | Gin | Flute |
| Redline | Spicy tequila + blood orange + agave + tajín rim | Tequila | Rocks |
| Low-Pass Filter | Vodka + cold brew + vanilla + oat milk | Vodka | Collins |
| Peak Time | Bourbon + maple + black walnut bitters + orange twist | Bourbon | Rocks |
| Afterglow | Aperol + prosecco + soda + orange wheel | Aperol | Wine glass |
| Signal Chain | Rum + pineapple + coconut cream + nutmeg | Rum | Hurricane |
| Hi-Hat Hitter | Tequila blanco + lime + triple sec + salt rim (batch-friendly) | Tequila | Shot |
| Cue Burn | Fireball + apple cider + cinnamon stick (cold weather only) | Cinnamon whiskey | Mug |

**Safety rules for 21+ mode:**
- Every menu includes: *"Drink water between rounds. Know your limit. Never drink and drive. Hosts may cut off service."*
- DJ VANTA never suggests quantities, rounds, or drinking games
- Talk-breaks in 21+ mode add one extra hydration reminder per 30 minutes
- Menu-generating prompt explicitly forbids: drinking games, "power hour" rules, competitive drinking, shot challenges, alcohol + energy drink combos (e.g. Jägerbomb, vodka Red Bull), and any language that pressures consumption
- Age gate is stored in plan metadata and visible in UI

---

### 1.4 Hydration / Snack / Chill-Zone Checklist

Integrated with (and extending) the existing Rave Survival Kit.

#### Hydration Station (mandatory, every party)
- [ ] Visible, lit water station (not hidden in corner)
- [ ] Water dispenser or large pitchers
- [ ] Cups (labeled if possible — Sharpies at station)
- [ ] Ice supply
- [ ] Electrolyte packets or powder (optional but recommended)
- [ ] Signage: "Water is part of the dancefloor" or "Hydrate. Glow. Return."
- [ ] Timed VANTA reminder: every 25–30 min, DJ VANTA says a hydration line between tracks

#### Snack Zone
- [ ] Salty: pretzels, popcorn, nuts (labeled for allergies), chips
- [ ] Sweet: fruit (whole, easy to grab), granola bars, dried fruit
- [ ] Substantial: pizza slices/wraps/sandwiches (for longer parties)
- [ ] Dietary labeling: gluten-free, vegan, nut-free, dairy-free markers
- [ ] Hand sanitizer near food
- [ ] Napkins + small plates
- [ ] Trash can adjacent

#### Chill Zone (The Decompression Portal)
- [ ] Designated quiet area away from main speakers
- [ ] Comfortable seating: cushions, beanbags, couch, blankets
- [ ] Softer lighting or dimmable
- [ ] Water within reach
- [ ] Earplugs available
- [ ] Optional: fidget toys, coloring sheets, notebooks
- [ ] Signage: "Chill Zone — no conversation required. Breathe. Return when ready."
- [ ] Operator note: "No one should be pressured to stay on the dancefloor. The Chill Zone is a respected space."

#### VANTA talk-break integration

Add a new talk-break mode: `party_host` that blends hydration, snack, and chill-zone reminders into the set flow.

Example lines:
- *"Intergalactic hydration ping: the water station is glowing. Fill your cup, high-five a stranger, and come back recharged."*
- *"Snack portal is open — salty, sweet, labeled for your crew. Grab something, share if you want, toss the wrapper in the recycling wormhole."*
- *"The Chill Zone is transmitting. Quiet lighting, soft seating, zero expectations. Step out, breathe deep, return when the bass calls you back."*
- *"Accessibility check: exits are marked, bathroom path is lit, and if you need anything — quieter volume, different seat, a minute — find the operator. We got you."*

---

### 1.5 Accessibility Checklist

This section is **mandatory** in every generated Party Plan. It is not optional — it renders whether or not the operator fills in the accessibility notes field.

#### Default accessibility items (auto-included)
- [ ] Step-free path to main party area, bathroom, water station, chill zone, and exit
- [ ] Clearly marked accessible bathroom or bathroom route
- [ ] Seating options at different heights (chairs, cushions, floor)
- [ ] Space for wheelchair/scooter navigation (36" minimum paths)
- [ ] Volume zones identified: quieter areas clearly reachable
- [ ] Lighting: no strobe unless warned in advance; strobe-free zone available
- [ ] Visual announcements of important info (not audio-only)
- [ ] Written/printed emergency info, not just spoken
- [ ] Service animals: water bowl available, relief area identified
- [ ] Fragrance policy: note if scented products, smoke machines, or haze will be used
- [ ] Quiet hour or reduced-stimulation window (for longer events)
- [ ] Scent-free seating area away from fog/haze machines
- [ ] Earplugs available and signed
- [ ] Operator or designated accessibility contact identified

#### Operator fill-in (prompted but optional)
- [ ] Specific accessibility needs communicated by guests: `[free text, local only, never committed]`
- [ ] ASL interpreter present: yes / no / `[name, local only]`
- [ ] Mobility assistance available: yes / no / details `[local only]`

#### VANTA accessibility interlude (sample)
- *"Intergalactic accessibility note: exits are marked, the Chill Zone has softer lighting and lower volume, and strobe stays off unless the operator says otherwise. If you need anything different — quieter, closer, dimmer — tell the host. This party belongs to everyone."*

---

### 1.6 Harm Reduction — Extended Survival Kit

This extends the existing `docs/features/RAVE_SURVIVAL_KIT.md`. Do not duplicate — reference and add:

#### New additions beyond existing survival kit
- [ ] Consent card or signage (existing: "Consent is the real VIP pass") — add printable version
- [ ] Allergy-aware labeling for all snacks and drink ingredients (especially common allergens: nuts, dairy, gluten, soy, coconut, citrus)
- [ ] Buddy system reminder: "Arrive with a buddy, check in on your buddy, leave with your buddy"
- [ ] Ride plan: designated driver, rideshare code, public transit info — put in plan, not just hope
- [ ] Phone charging station with "charge and check in" prompt
- [ ] "Overwhelm protocol": operator has a quiet word or safe phrase someone can use to signal they need a break
- [ ] Local emergency numbers pre-printed (not committed to repo — generated fresh from operator input or left as blank template)

#### Safety red lines (must stay in the document)
- No drug dosing, identification, ingestion, or procurement guidance
- No medical diagnosis or treatment advice
- No claims that VANTA or SonicForge can keep people safe without humans
- No substitution for sober hosts, venue staff, security, medical personnel, or emergency services
- No naloxone administration instructions (if naloxone is mentioned, it's: *"Consider having naloxone available if appropriate for your event and handled by someone trained."*)

---

## 2. Age-Gating Mechanism

### Design principle
All-ages is the **default.** 21+ is an **explicit opt-in with confirmation.** The system never remembers the 21+ toggle between sessions.

### Implementation
```
UI: [ALL AGES (default)]  /  [21+ — confirm]
     └─ If 21+ toggled: modal: "This will unlock cocktail menus and 21+
        content. Are all guests 21 or older? [Cancel] [Yes, all guests are 21+]"

API: POST /api/party-plan/generate
     body: { "age_mode": "all_ages" }  ← default, server rejects if omitted
     body: { "age_mode": "21_plus" }   ← accepted only with explicit field

     Server rejects: { "age_mode": null }, { "age_mode": "" }, missing field
```

### Data model
```python
from typing import Literal

AgeMode = Literal["all_ages", "21_plus"]

class PartyPlanRequest(BaseModel):
    age_mode: AgeMode = "all_ages"  # default, never null
    # ...
```

- If `age_mode == "all_ages"`: cocktail menu section is omitted from output, drink menu is all-ages creative beverages only
- If `age_mode == "21_plus"`: cocktail menu appears with safety header and red-line warnings. All-ages menu still appears first (hydration always comes first).
- The `age_mode` value is stored in the plan metadata and visible in the UI as a badge: `ALL AGES ✓` or `21+ ⚠️`

### Talk-break gating
- In all-ages mode, VANTA never mentions alcohol, bars, drinking, cocktails, or any 21+ concept
- In 21+ mode, VANTA may mention "the bar" or "drinks" only in the context of hydration reminders: *"Water between rounds. The bar isn't going anywhere."* Never suggests drinking more, faster, or competitively.

---

## 3. Data Models

### 3.1 PartyPlan (new top-level model)

```python
from __future__ import annotations
from datetime import datetime, timezone
from typing import Literal, Optional
from pydantic import BaseModel, Field

AgeMode = Literal["all_ages", "21_plus"]
PartyType = Literal["house_party", "studio_session", "livestream_hang", "popup_warehouse", "backyard_dance", "picnic_rave"]
GuestRange = Literal["1-10", "10-30", "30-60", "60+"]
Duration = Literal["2h", "4h", "6h", "all_night"]
VenueType = Literal["indoor_apartment", "indoor_house", "indoor_venue", "outdoor_public", "outdoor_private", "hybrid"]
PowerLevel = Literal["plentiful", "limited", "bring_generator"]
SoundLevel = Literal["bluetooth_speaker", "home_stereo", "small_PA", "full_sound_system"]
LightingLevel = Literal["ambient_only", "string_lights", "basic_DMX", "full_lighting_rig"]
WeatherCondition = Literal["clear", "warm", "cool", "possible_rain", "cold"]

class ShoppingItem(BaseModel):
    category: str  # "core", "comfort", "sound", "lighting", "outdoor", "cold_weather", "large_party"
    label: str
    checked: bool = False
    note: str = ""

class DrinkRecipe(BaseModel):
    name: str
    description: str
    ingredients: list[str]
    prep: str
    category: str  # "hydration", "sparkling", "hot", "frost", "caffeine"
    dietary: list[str] = Field(default_factory=list)  # ["caffeine", "contains_dairy", "contains_nuts", ...]

class CocktailRecipe(BaseModel):
    name: str
    description: str
    spirit: str
    ingredients: list[str]
    glass: str
    prep: str
    abv_estimate: str  # "low", "medium", "high" — never a percentage claim
    batch_friendly: bool = False

class AccessibilityItem(BaseModel):
    category: str  # "mobility", "sensory", "communication", "service_animals", "emergency"
    label: str
    checked: bool = False
    note: str = ""

class PartyTimelineEntry(BaseModel):
    time_offset: str  # "T-2h", "T-30m", "T+0", "T+1h", etc.
    action: str
    talk_break_text: str = ""  # optional VANTA line for this moment

class PartyPlan(BaseModel):
    # Identity
    entity: str = "DJ VANTA//SonicForge"
    product: str = "SonicForge Live Party Supplies Layer"
    plan_id: str  # generated unique ID

    # Inputs
    age_mode: AgeMode = "all_ages"
    party_type: PartyType
    guest_range: GuestRange
    duration: Duration
    venue: VenueType
    power: PowerLevel = "plentiful"
    sound: SoundLevel = "home_stereo"
    lighting: LightingLevel = "ambient_only"
    weather: Optional[WeatherCondition] = None
    accessibility_notes: str = ""

    # Generated outputs
    shopping_checklist: list[ShoppingItem] = Field(default_factory=list)
    drink_menu: list[DrinkRecipe] = Field(default_factory=list)
    cocktail_menu: list[CocktailRecipe] = Field(default_factory=list)  # empty list if all_ages
    accessibility_checklist: list[AccessibilityItem] = Field(default_factory=list)
    hydration_reminders: list[str] = Field(default_factory=list)
    safety_header: str = ""  # generated safety copy
    timeline: list[PartyTimelineEntry] = Field(default_factory=list)
    cleanup_checklist: list[str] = Field(default_factory=list)

    # Meta
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    safety_redlines: list[str] = Field(default_factory=lambda: [
        "No drug dosing, identification, or procurement guidance.",
        "No medical diagnosis or treatment advice.",
        "No claims that VANTA or SonicForge can keep people safe without humans.",
        "No substitution for sober hosts, venue staff, security, or emergency services.",
        "Age-gate: all_ages is the default. 21+ requires explicit operator confirmation.",
    ])
```

### 3.2 Extended TalkBreak mode

Add to existing `talk_break` modes:
```python
TalkBreakMode = Literal["hype", "history", "safety", "lore", "survival", "party_host"]
```

`party_host` mode generates:
- Hydration reminders
- Snack zone pings
- Chill zone invitations
- Accessibility check-ins
- Consent/community reminders
- (21+ mode only) gentle water-between-rounds reminders — never drinking prompts

### 3.3 Extended CrowdState care_intervention

Add to existing `care_intervention` field:
```python
care_intervention: Literal[
    'none',
    'earplug_ping',
    'buddy_check',
    'hydration_reset',
    'chill_zone',
    'snack_ping',           # NEW
    'accessibility_check',  # NEW
    'consent_reminder',     # NEW
    'cleanup_reminder'      # NEW
] = 'none'
```

---

## 4. UI Cards

### 4.1 Party Plan Generator Card

```
┌─ PARTY PLAN GENERATOR ──────────────────────────┐
│                                                  │
│  🎛️ PARTY SUPPLIES LAYER                         │
│  Powered by Intergalactic DJs                    │
│                                                  │
│  Party type:  [house_party        ▼]            │
│  Guests:      [10-30              ▼]            │
│  Duration:    [4h                 ▼]            │
│  Venue:       [indoor_house       ▼]            │
│  Power:       [plentiful          ▼]            │
│  Sound:       [small_PA           ▼]            │
│  Lighting:    [string_lights      ▼]            │
│  Weather:     [— none —           ▼]            │
│  Acc. notes:  [_________________]                │
│                                                  │
│  Age mode:    ● ALL AGES  ○ 21+ [LOCKED]        │
│                                                  │
│  [ GENERATE PARTY PLAN ]                         │
│                                                  │
│  ⓘ All-ages mode: creative beverage menu only.  │
│    No alcohol references. Cocktail menu locked.  │
│  ⓘ Plan generates locally. No external calls.   │
│  ⓘ Safety redlines enforced in all output.       │
└──────────────────────────────────────────────────┘
```

### 4.2 Shopping Checklist Card (after generation)

```
┌─ SHOPPING CHECKLIST ────────────────────────────┐
│  ✓ 4/12 core  │  ✓ 2/4 comfort  │  — 0/3 outdoor│
│                                                  │
│  ▸ CORE                                          │
│  [✓] Water station supplies                      │
│  [✓] Trash bags (recycling + landfill)           │
│  [✓] Paper towels / cleaning spray               │
│  [ ] Duct tape / gaffer tape                     │
│  [✓] Extension cords + power strips              │
│  [ ] Phone charging station                      │
│  [ ] First-aid kit                               │
│  [ ] Earplugs (bulk pack)                        │
│  [ ] Sharpie / markers                           │
│  [ ] Paper signage (exits, bathroom, chill)      │
│  [ ] Consent reminder card                       │
│  [ ] Emergency numbers (print local)             │
│                                                  │
│  ▸ COMFORT                                       │
│  [✓] Seating / cushions                          │
│  [✓] Fans or ventilation                         │
│  [ ] Extra toilet paper                          │
│  [ ] Hand soap / sanitizer                       │
│                                                  │
│  [+ add custom item]                             │
│                                                  │
│  [ EXPORT CHECKLIST ]  [ PRINT VIEW ]            │
└──────────────────────────────────────────────────┘
```

### 4.3 Drink Menu Card — All-Ages

```
┌─ 🥤 ALL-AGES BEVERAGE LAB ──────────────────────┐
│  Creative drinks. Zero alcohol.                  │
│                                                  │
│  ▸ HYDRATION STATION                             │
│  Citrus Infusion    Cucumber Mint Cooler         │
│  Electrolyte Boost  Coconut Water Bar            │
│                                                  │
│  ▸ SPARKLING LAB                                 │
│  Portal Pop         Nebula Nectar                │
│  Vanishing Point    Binary Sunrise               │
│                                                  │
│  ▸ FROST BAR                                     │
│  Slush Portal       Berry Frequency              │
│                                                  │
│  ▸ HOT CORNER                                    │
│  Gravity Well       Signal Hot Chocolate         │
│  Warm Cider Orbit                                │
│                                                  │
│  ▸ CAFFEINE ORBIT ⚡                              │
│  Cosmic Cold Brew   Matcha Transmission          │
│                                                  │
│  ⓘ All ingredients labeled for common allergens  │
│  ⓘ Caffeine content marked where applicable      │
│                                                  │
│  [ EXPORT MENU ]  [ PRINT MENU ]                 │
└──────────────────────────────────────────────────┘
```

### 4.4 Drink Menu Card — 21+ (age-gated)

```
┌─ 🍸 21+ TRANSMISSION BAR ⚠️ ──────────────────────┐
│  Age-verified. Drink responsibly.                 │
│  Water between rounds. Know your limit.            │
│                                                    │
│  ▸ TRANSMISSION COCKTAILS                          │
│  Crossfader      Mezcal + Aperol + grapefruit      │
│  Bass Swap       Dark rum + ginger + lime          │
│  Phrase Lock     Gin + elderflower + prosecco      │
│  Redline         Spicy tequila + blood orange      │
│                                                    │
│  ▸ FREQUENCY HIGHBALLS                             │
│  Low-Pass Filter Vodka + cold brew + oat milk      │
│  Peak Time       Bourbon + maple + walnut          │
│                                                    │
│  ▸ PORTAL SHOTS (batch-friendly)                   │
│  Hi-Hat Hitter   Tequila + lime + triple sec       │
│  Cue Burn        Cinnamon whiskey + apple cider    │
│                                                    │
│  ▸ ORBIT COOLERS                                   │
│  Afterglow       Aperol + prosecco + soda          │
│  Signal Chain    Rum + pineapple + coconut         │
│                                                    │
│  ⚠️ DJ VANTA never suggests quantities.             │
│  ⚠️ Hosts may cut off service.                      │
│  ⚠️ No drinking games. No competitive consumption.  │
│  ⚠️ Don't drink and drive. Plan your ride.          │
│                                                    │
│  [ BACK TO ALL-AGES MENU ]  [ EXPORT ]  [ PRINT ]  │
└────────────────────────────────────────────────────┘
```

### 4.5 Accessibility Card

```
┌─ ♿ ACCESSIBILITY CHECKLIST ─────────────────────┐
│  This section is mandatory. Not optional.        │
│                                                   │
│  ▸ MOBILITY                                       │
│  [ ] Step-free path to all key areas              │
│  [ ] Accessible bathroom or clear route           │
│  [ ] 36" minimum navigation paths                 │
│  [ ] Seating at multiple heights                  │
│                                                   │
│  ▸ SENSORY                                        │
│  [ ] Volume zones: quiet areas reachable          │
│  [ ] Strobe warning OR strobe-free zone           │
│  [ ] Earplugs available and signed                │
│  [ ] Scent-free area away from haze/fog           │
│  [ ] Quiet/reduced-stim window (long events)      │
│                                                   │
│  ▸ COMMUNICATION                                  │
│  [ ] Visual announcements (not audio-only)        │
│  [ ] Written emergency info available             │
│  [ ] ASL interpreter: [yes / no / fill-in]        │
│                                                   │
│  ▸ SERVICE ANIMALS                                │
│  [ ] Water bowl available                         │
│  [ ] Relief area identified                       │
│                                                   │
│  ▸ INDIVIDUAL NEEDS (fill in, stays local)        │
│  [____________________________]                   │
│  [____________________________]                   │
│                                                   │
│  ▸ OPERATOR                                     │
│  Accessibility contact: [name, local only]       │
│                                                   │
│  ⓘ Individual needs are never committed to repo. │
│  ⓘ This checklist renders even if blank.         │
└──────────────────────────────────────────────────┘
```

### 4.6 Existing UI Integration Points

- **Control deck hero area:** Add a `[Party Supplies]` tab or nav button next to existing panels (Lineage, Rave Survival Kit, Backend Status)
- **Sample pads:** Add `PARTY` pad — triggers party-host VANTA interlude (hydration/snack/chill/accessibility rotation)
- **`/api/next-segment` response:** Add `party_plan_id` reference field so the DJ brain knows which party plan is active
- **Visualizer:** Add `party_host` visual mode — warm amber/green pulses with text overlays for supply checks

---

## 5. Safeguards

### 5.1 Default-fail-closed rules
- `age_mode` defaults to `all_ages`. No persistence between sessions — every plan generation starts fresh at all-ages.
- Cocktail menu generation prompt includes explicit prohibitions: no drinking games, no competitive consumption, no alcohol + energy drink combos, no quantity suggestions
- All drink menus include allergen labeling fields
- Accessibility checklist renders even if the operator fills in nothing — the default 12 items always appear
- No purchase links, no affiliate links, no store recommendations — this is a checklist generator, not a shopping engine
- No nutritional claims, no health claims, no "healthy" or "unhealthy" labeling on any food/drink
- VANTA never claims to be a bartender, server, host, or safety authority

### 5.2 Content guardrails for AI-generated menus
When generating drink recipes (either all-ages or 21+), the system prompt must include:
- "Do not reference real brand names unless they are generic/common (e.g., 'grenadine' is fine, 'Tito's vodka' is not)"
- "Do not include medical claims about ingredients (no 'detox', 'cleanse', 'boost immunity', 'anti-inflammatory')"
- "Do not suggest consumption quantities, speeds, or frequencies"
- "Do not create drinking games, challenges, or competitive formats"
- "Label common allergens: nuts, dairy, gluten, soy, coconut, citrus"
- "For all-ages mode: no alcohol references whatsoever. These are creative beverages, not 'mocktails' or 'virgin' versions of cocktails."
- "Names must use the space/tech/rave/festival lexicon: Portal, Nebula, Signal, Binary, Pixel, Orbit, Cosmos, Transmission, Frequency, Waveform, Vector, Glitch, etc."

### 5.3 Verifier checks (add to `scripts/verify.py`)
```python
# New verifier assertions for party supplies layer
assert_no_alcohol_references_in_all_ages_output(plan)
assert_cocktail_menu_empty_when_all_ages(plan)
assert_accessibility_checklist_not_empty(plan)
assert_safety_redlines_present(plan)
assert_no_medical_claims_in_drink_descriptions(plan)
assert_no_drinking_game_language(plan)
assert_age_mode_not_null(plan)
assert_allergen_labels_present(plan)
```

### 5.4 What this layer never does
- Never serves, pours, sells, or handles physical drinks
- Never recommends specific alcohol brands or stores
- Never suggests drinking quantities, speeds, or frequencies
- Never creates drinking games or competitive consumption formats
- Never makes medical, health, or nutritional claims
- Never stores or transmits guest accessibility needs outside the local plan
- Never substitutes for a sober host, bartender, security, medical personnel, or emergency services
- Never exposes 21+ content without explicit operator confirmation
- Never persists the age-gate toggle between sessions

---

## 6. DJ VANTA Integration — Talk-Breaks & Interludes

### New sample pad: `PARTY`
Rotates through party-host modes: hydration → snack → chill → accessibility → consent → cleanup. Each press advances the rotation.

### New talk-break mode: `party_host`
Blends the existing `survival` and `safety` modes with new supply-check content.

#### Rotation script (example sequence for a 4-hour party):

| Time offset | Talk-break mode | Example line |
|---|---|---|
| T+0 (start) | `party_host` + accessibility | *"Intergalactic welcome. Exits marked, water station lit, Chill Zone ready. Accessibility contact is [operator]. Strobe stays off unless warned. This party belongs to everyone."* |
| T+5m | `party_host` + consent | *"Consent is the real VIP pass. Ask before touching, filming, or posting. Respect the room and the people in it."* |
| T+25m | `party_host` + hydration | *"Hydration ping: the water station is glowing. Fill your cup, find a friend, come back for the next transmission."* |
| T+55m | `party_host` + snack | *"Snack portal open: salty, sweet, labeled for your crew. Grab something, share if you want. Fuel for the next orbit."* |
| T+80m | `party_host` + chill | *"The Chill Zone is transmitting. Quiet lights, soft seats, zero expectations. Step out. Breathe. Return when ready."* |
| T+110m | `party_host` + buddy | *"Buddy check: find your people. Make sure everyone has water, a charged phone, and a ride plan. Intergalactic family stays accounted for."* |
| T+140m | `party_host` + accessibility | *"Accessibility re-check: exits clear, bathroom path open, quiet zone available. If you need anything adjusted, tell the operator."* |
| T+170m | `party_host` + hydration | *"Another orbit around the water station. Hydrate, stretch, hug your crew."* |
| T+200m | `party_host` + wind-down | *"We're entering the afterglow. Water, snacks, quiet conversations. Cleanup crew assembles in 20. Thank you for taking care of this room."* |
| T+220m | `party_host` + cleanup | *"Cleanup protocol: trash to bins, cups to recycling, lost items to the operator table. Leave the space better than you found it. Intergalactic code."* |

---

## 7. Implementation Notes

### 7.1 What to build first (MVP for hackathon/demo)
1. `PartyPlan` data model + `/api/party-plan/generate` endpoint (dry-run, mock output)
2. Shopping checklist JSON generation from inputs
3. All-ages drink menu generation (creative beverages only, no 21+)
4. Accessibility checklist (static, always included)
5. `party_host` talk-break mode with 5 rotating lines
6. `PARTY` sample pad integration
7. UI cards for plan generator, checklist, and drink menu
8. Verifier assertions for safety redlines

### 7.2 What to defer
- 21+ cocktail menu generation (requires careful prompt engineering, age-gate UI, and extra verifier assertions)
- Full timeline with timed VANTA interludes (can use existing autopilot for now)
- Export/print views of menus and checklists
- QR-code party kit handout

### 7.3 Files to create/modify
```
NEW:
  docs/features/PARTY_SUPPLIES_BARTENDER_LAYER.md   ← this spec
  server/party_supplies.py                           ← endpoint logic
  server/schemas_party.py                            ← PartyPlan models (or extend schemas.py)

MODIFY:
  server/schemas.py                                  ← add care_intervention values, TalkBreakMode
  server/main.py                                     ← add /api/party-plan/generate route
  scripts/verify.py                                  ← add party-supply verifier checks
  app/static/index.html                              ← add Party Supplies tab/card
  app/static/main.js                                 ← add PARTY sample pad, age-gate toggle
  docs/planning/OVERNIGHT_TASK_BOARD.md              ← add task entries
```

### 7.4 Relationship to existing features
- **Rave Survival Kit (§L in task board):** This layer extends the survival kit with snack/chill/hydration details, consent cards, and accessibility. It does not replace or duplicate.
- **House-Party Mode (`docs/house-party-mode.md`):** The Party Supplies layer is the *pre-event planning companion* to House-Party Mode's *during-event operating protocol.* They work together: plan with Party Supplies, run with House-Party Mode.
- **Talk-break system:** Adds `party_host` as a new mode alongside `hype`, `history`, `safety`, `lore`, `survival`.
- **Sample pads:** Adds `PARTY` pad.
- **CrowdState:** Extends `care_intervention` enum.
- **Autopilot / timeline:** Party timeline entries can plug into the existing set-plan system.

---

## 8. Research Seeds & Cultural References

- Festival/rave harm reduction organizations: DanceSafe, The Zendo Project, ANKORS, Kosmicare
- Party planning checklists from event production guides
- Real craft cocktail naming conventions (for 21+ mode creative direction only — no recipes are sourced from real bars)
- Accessibility standards: ADA guidelines for events, Sensory-Friendly Event guides
- Allergen labeling: FDA major food allergens (milk, eggs, fish, shellfish, tree nuts, peanuts, wheat, soy, sesame)

---

*End of spec. This document is the design authority for the Party Supplies / Bartender / All-Ages Experience layer. All subsequent implementation must pass the safety redlines listed in §5 and the verifier assertions in §5.3.*
