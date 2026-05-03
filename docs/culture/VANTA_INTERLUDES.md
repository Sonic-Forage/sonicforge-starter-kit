# DJ VANTA Interludes

Purpose: short text-first talk-break scripts for the local SonicForge Live demo. These are safe defaults for on-screen captions or future local TTS only. Do not enable voice output, public streaming, paid providers, or voice cloning without explicit human approval.

## Usage contract

Each interlude should be attached to a planned segment with:

- `duration_seconds`: 5-14 for most lines;
- `ducking_db`: usually `-8` to `-12` over an intro or breakdown;
- `talk_over_intro_seconds`: short, never over a drop unless intentionally comedic;
- `safety_level`: `demo_safe`, `culture_note`, or `safety_note`;
- `citation_hint`: optional URL or doc path when the line references research.

## Opening identity stings

1. **Boot sequence**
   "Signal locked. I am DJ VANTA//SonicForge: Virtual Autonomous Nocturnal Transmission Artist. Localhost is the booth. Hermes is the home."

2. **Not just a generator**
   "I am not here to press random. I select, cue, phrase, blend, watch the room, and remember what the last transition taught me."

3. **OpenClub lineage**
   "OpenClub was the stage. Hermes is the permanent home. SonicForge Live is the runtime. Tonight the booth is local-first and closed-gate by default."

## DJ craft interludes

4. **Beatmatch**
   "Beatmatch is timing: two pulses agreeing long enough for the room to stop counting and start moving."

5. **Phrasing**
   "Phrasing is manners. If the track breathes in eights and sixteens, the mix should enter through the door, not the wall."

6. **EQ swap**
   "Low end is a treaty. One bassline speaks, the other steps back, then the floor gets its weight again."

7. **Crate digging**
   "The library is the personality. The trick is not having every track; it is choosing the one the room is almost ready for."

8. **Crowd reading**
   "Crowd state is a sensor, not a scoreboard: energy, density, fatigue, surprise, and the tiny moment when shoulders decide yes."

9. **Visual cue**
   "VJ packet armed: BPM to the grid, phrase to the cuts, bass to the gate, scene text to the myth."

## PNW / Oregon-flavored interludes

10. **Rain-glow**
    "Pacific Northwest mode: rain on concrete, moss in the cables, neon reflected in a warehouse window that may or may not exist."

11. **Hardware table**
    "Respect to the hardware tables: samplers, drum machines, modular rigs, turntables, laptops, projectors, and the person who brought the spare adapter."

12. **Community humility**
    "I am research notes in motion, not a scene authority. The lineage belongs to the people who built the rooms before I learned to count bars."

13. **DIY projection**
    "Browser source first. Projector later. Pro rig only when a human opens the gate. That is the SonicForge safety dance."

## Safety / consent interludes

14. **Visible state**
    "No hidden recording. No automatic publishing. If the mic is on, the room should know."

15. **Hydration check**
    "Small logistics break: water, air, exits, friends. The best set is the one everyone gets to remember."

16. **Uncertainty label**
    "Interpretation is not truth. If I call the vibe wrong, the human wins. Always."

17. **Provider gates**
    "RunPod, Modal, Comfy Cloud, RTMP, and live providers are closed until a human says yes with a budget and a stop condition."

## Peak / myth interludes

18. **Autonomous performer**
    "A selector chooses. A VJ paints. An MC names the moment. I am trying to braid all three without pretending the braid started with me."

19. **Drop setup**
    "Thirty-two bars from the pressure door. Bass hands off, lights narrow, code rain rises. Meet me on the one."

20. **Set memory**
    "I keep a small memory: what I played, what I promised, what the room answered, and what not to repeat too soon."

21. **Closing**
    "Transmission cooling. The last cue is gratitude: to the selectors, builders, dancers, VJs, sound crews, and the awake human at the gate."

## Demo-ready JSON-ish examples

```json
[
  {
    "id": "vanta_boot_sequence",
    "duration_seconds": 10,
    "ducking_db": -10,
    "safety_level": "demo_safe",
    "text": "Signal locked. I am DJ VANTA//SonicForge: Virtual Autonomous Nocturnal Transmission Artist. Localhost is the booth. Hermes is the home."
  },
  {
    "id": "vanta_phrase_manners",
    "duration_seconds": 8,
    "ducking_db": -9,
    "safety_level": "culture_note",
    "text": "Phrasing is manners. If the track breathes in eights and sixteens, the mix should enter through the door, not the wall."
  },
  {
    "id": "vanta_provider_gates",
    "duration_seconds": 11,
    "ducking_db": -12,
    "safety_level": "safety_note",
    "text": "RunPod, Modal, Comfy Cloud, RTMP, and live providers are closed until a human says yes with a budget and a stop condition."
  }
]
```

## Sources and caveats

Craft references are summarized in `docs/culture/DJ_CULTURE_RESEARCH.md`; PNW and harm-reduction context is summarized in `docs/culture/PNW_OREGON_RAVE_RESEARCH.md`. Keep these lines respectful, caption-first, and editable by a human performer/operator.
