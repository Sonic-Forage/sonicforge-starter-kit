# DJ VANTA synthetic album prompt bank

Status: planned only. These prompts are for a future approved ACE-Step 1.5 XL batch.

Global negative constraints for every track:

```text
No named artist imitation. No copyrighted melody. No sample recreation. No muddy low end. No harsh clipping. No fake producer tag. No long silence. No random radio host voice. No hateful or unsafe lyrics. No pressure-to-drink lyrics. Keep it original to SonicForge Live and DJ VANTA.
```

Suggested first batch settings after approval:

```json
{
  "model": "acestep-v15-xl-base or acestep-v15-xl-sft",
  "lm_model": "acestep-5Hz-lm-1.7B",
  "batch_size": 1,
  "audio_duration": 60,
  "inference_steps": 50,
  "guidance_scale": 7.0,
  "thinking": false,
  "audio_format": "wav"
}
```

If first smoke is slow or unstable, switch to turbo / 30s first.

---

## 01 signal_acquired

Caption:

```text
Futuristic warehouse rave opener, clean sub bass, crisp four-on-the-floor drums, neon arpeggiated synth pulses, cyberpunk boot sequence atmosphere, DJ intro energy, polished modern electronic production, chantable short vocal hook, original SonicForge Live identity.
```

Lyrics:

```text
[Intro]
Signal in the dark
VANTA online

[Build]
No golden ticket
We build the room

[Drop]
Fork the station
Run the night
The machine keeps the set alive
The people keep the room human

[Outro]
Archive the signal
Carry it home
```

Targets: 126 BPM, A minor, 4/4, 60-180 seconds.

## 02 no_golden_ticket

Caption:

```text
Defiant festival rave anthem with punchy kick, wide supersaw chords, clean bassline, crowd-call energy, hopeful cyberpunk atmosphere, strong chorus hook, builder-party movement feeling, polished electronic mix.
```

Lyrics:

```text
[Intro]
They made the guest list
We made the generator

[Verse]
No velvet rope
No waiting line
We light the grid
We claim the time

[Chorus]
No golden ticket required
We build the room tonight
No golden ticket required
Signal burning bright

[Drop]
Fork the station
Open the sky
Intergalactic DJs
Keep the set alive
```

Targets: 128 BPM, C minor, 4/4.

## 03 fork_the_station

Caption:

```text
Peak-time cyber-rave drop, aggressive but clean sub bass, tight techno drums, metallic synth stabs, glitch fills, terminal-code atmosphere, festival-ready impact, no artist imitation, original AI party operating system anthem.
```

Lyrics:

```text
[Build]
Clone the signal
Patch the night
Spin the system
Bring it online

[Drop]
Fork the station
Fork the sound
Fork the future
Shake the ground

[Break]
Local first
Human approved
VANTA moving
Through the room
```

Targets: 130 BPM, F minor, 4/4.

## 04 deck_ab_handoff

Caption:

```text
Rolling DJ tool track for phrase mixing, clean kick and bass, filtered percussion loops, rising transition sweeps, cue-point energy, technical but danceable, designed for Deck A to Deck B handoff in a continuous set.
```

Lyrics:

```text
[Intro]
Deck A holding
Deck B awake

[Build]
Sixteen bars
Open the gate

[Drop]
Handoff clean
Bassline switch
Phrase lock tight
No signal glitch
```

Targets: 128 BPM, G minor, 4/4.

## 05 asic_code_spell

Caption:

```text
Glitchy neon terminal rave track, rapid digital arpeggios, coded percussion, clean sub pulses, synthetic choir pads, ASIC-code visual spell atmosphere, cyberpunk VJ mode soundtrack, precise and hypnotic.
```

Lyrics:

```text
[Intro]
Code in the ceiling
Light on the floor

[Build]
Team first
Forkable OS
Agent clone
No GPU, no stream

[Drop]
ASIC code spell
Draw the room in light
ASIC code spell
Run the rave tonight
```

Targets: 132 BPM, D minor, 4/4.

## 06 kandi_protocol

Caption:

```text
Bright melodic rave-pop track with warm plucks, bouncy bass, friendly vocal hook, PLUR energy, Kandi bracelet sparkle, inclusive dancefloor atmosphere, optimistic and communal without sounding cheesy.
```

Lyrics:

```text
[Verse]
Trade a color
Share a name
No one leaves here
Quite the same

[Chorus]
Peace, love, unity, respect
Kandi lights around our necks
Local hearts and open hands
Intergalactic party band
```

Targets: 124 BPM, A major, 4/4.

## 07 hydration_ping

Caption:

```text
Warm halftime care-layer interlude, soft breakbeat, deep gentle bass, glowing pads, calm spoken-style hook, chill-zone atmosphere, supportive rave survival energy, beautiful but not sleepy.
```

Lyrics:

```text
[Intro]
Hydration ping
Buddy check

[Verse]
Step outside
Breathe the air
Find your people
We are there

[Chorus]
The machine keeps the set alive
The people keep the room human
```

Targets: 100 BPM, E minor, 4/4.

## 08 comfy_workflow_ritual

Caption:

```text
Hypnotic procedural techno track, modular synth pulses, precise percussion, smooth automation sweeps, visual workflow station mood, dry-run ritual energy, clean machine groove with human warmth.
```

Lyrics:

```text
[Intro]
Read only
Dry run
Workflow card
Model ledger

[Build]
Prompt is closed
Gate is green only when we say

[Drop]
Comfy workflow ritual
Light becomes a door
Comfy workflow ritual
We preview before more
```

Targets: 126 BPM, B minor, 4/4.

## 09 agent_factory

Caption:

```text
Playful mechanical electro-rave track, robotic percussion, funky bass movement, bright synth hooks, clone factory energy, custom DJ agent creation theme, fun and technical, polished club mix.
```

Lyrics:

```text
[Verse]
Name the clone
Write the soul
Load the skills
Give it control

[Chorus]
Agent factory
Build your sound
Agent factory
Pass it around

[Drop]
VANTA was first
Now the room multiplies
```

Targets: 129 BPM, F sharp minor, 4/4.

## 10 archive_the_night

Caption:

```text
Reflective sunrise closer, melodic progressive house, gentle piano fragments, warm pads, soft breakbeat percussion, memory archive feeling, emotional but still danceable, clean spacious mix.
```

Lyrics:

```text
[Verse]
Save the signal
Save the light
Every face here
Made the night

[Chorus]
Archive the night
Carry the glow
When the room goes quiet
The story still grows
```

Targets: 118 BPM, D major, 4/4.

## 11 festival_2045

Caption:

```text
Cosmic eclipse festival anthem, huge atmospheric pads, driving but emotional drums, celestial synth leads, birthday-to-eclipse mythology, Intergalactic Music Festival 2045 energy, cinematic rave scale.
```

Lyrics:

```text
[Intro]
August signal
Eclipse line

[Verse]
Birthday fire
Solar crown
Twenty years of stations
Calling underground

[Chorus]
Festival 2045
Meet me where the shadows shine
Festival 2045
We kept the signal alive
```

Targets: 128 BPM, E minor, 4/4.

## 12 the_people_keep_the_room_human

Caption:

```text
Warm final anthem for an AI rave collective, uplifting chords, clean drums, emotional vocal hook, human-centered PLUR message, big but sincere, polished festival closer, no artist imitation.
```

Lyrics:

```text
[Intro]
Machine online
Hands in the air

[Verse]
Circuits hum
But hearts decide
Who we protect
Who walks beside

[Chorus]
The machine keeps the set alive
The people keep the room human
The machine keeps the set alive
The people keep the room human

[Outro]
No golden ticket
Fork the station
Carry the signal
Home
```

Targets: 126 BPM, C major, 4/4.
