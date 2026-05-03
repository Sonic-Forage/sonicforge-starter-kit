#!/usr/bin/env python3
"""Generate a Discord introductions welcome mix using the existing ComfyUI/OmniVoice/ACE-Step engine.

Structure: intro -> song -> intro -> song -> outro.
This imports the proven trippy-pizza ComfyUI mix runner and overrides only the creative brief.
"""
from pathlib import Path
import run_trippy_pizza_comfy_mix as m

m.OUT_ROOT = Path("/opt/data/audio_cache/sonicforge_discord_intro_mix")
m.VOICE_TAGS = [
    "male, middle-aged, low pitch, american accent",
    "female, young adult, high pitch, british accent",
    "male, elderly, very low pitch, british accent",
]
m.VOICE_TEXTS = [
    (
        "[confirmation-en] Welcome to the Mind Expansion Network introductions room. This is Jimsky, holding the door open while the bass checks your wristband. "
        "Say your name, your vibe, what you build, and one strange dream you want SonicForge to help make real. Keep it public safe. No secrets in the sauce. "
        "Now step through the little portal and let the first track introduce the room."
    ),
    (
        "[laughter] Second welcome signal. The first song shook the dust off the server, and now the introductions chat is glowing. "
        "Artists, ravers, builders, clients, curious aliens: this is your tiny campfire. Drop a hello, share a weird idea, and if the pizza starts talking, tag it as lore. "
        "Song two, bring the friendly chaos."
    ),
    (
        "[sigh] Outro from the human lounge. The introductions room is open, the SonicForge drops room is live, and we are organizing this universe one clean channel at a time. "
        "No chaos flood, no secret leaks, just small doors that work. Welcome aboard. Jimsky out."
    ),
]

m.SONGS = [
    {
        "id": "01_introduction_room_portal",
        "title": "Introduction Room Portal",
        "bpm": 118,
        "keyscale": "A minor",
        "seed": 811001,
        "tags": (
            "original friendly psychedelic festival welcome song, 118 BPM, warm bass, crisp drums, trippy bluegrass guitar, "
            "glowing synth pads, community introduction anthem, playful rave campfire energy, clean modern ACE-Step music generation, no named artist imitation"
        ),
        "lyrics": """[Intro]
Step in slow, say your name
Tiny door with a neon flame

[Verse]
Builder with a sketchbook, raver with a dream
Artist in the server with a laser beam
Tell us what you love, tell us what you make
Mind Expansion rising like a birthday cake

[Chorus]
Welcome to the room, let the signal bloom
Introductions glowing through the bass and moon
Name your vibe, name your spark
We build little portals in the dark

[Bridge]
No secrets in the chat, keep the sauce clean
Public-safe magic on the screen

[Outro]
Step in slow, the channel is bright
Human lounge opens up tonight
""",
    },
    {
        "id": "02_small_doors_that_work",
        "title": "Small Doors That Work",
        "bpm": 126,
        "keyscale": "E minor",
        "seed": 811777,
        "tags": (
            "original psychedelic glitch funk welcome song, 126 BPM, rubber bass, bluegrass banjo accents, festival drums, "
            "cosmic Discord server launch energy, friendly weird community anthem, polished generated music, no named artist imitation"
        ),
        "lyrics": """[Intro]
Small doors that work, bright signs in the hall
One clean channel before we build it all

[Verse]
SonicForge drops in a pocket of light
Introductions chat getting friendly tonight
No chaos flood, no mystery key
Just humans and agents learning how to be

[Chorus]
Small doors that work, let the people flow
One hello, one dream, one place to go
If the room gets weird, let the bassline smile
We organize the galaxy mile by mile

[Drop]
Hello from the moon, hello from the floor
Jimsky at the console opening one more door

[Outro]
Small doors that work, signal stays true
Mind Expansion network saying welcome to you
""",
    },
]

if __name__ == "__main__":
    m.main()
