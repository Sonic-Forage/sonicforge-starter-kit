# Create Your Own SonicForge

SonicForge is a pattern, not just one project.

Think of it as three layers:

1. **Engine** - Hermes/automation, FastAPI cockpit, local scripts, verification.
2. **Payload** - your performer/persona, voice direction, safety boundaries, workflow bindings, show formats, and lore.
3. **Workflows** - ComfyUI/ACE-Step/OmniVoice/other creative backends that generate voices, music, images, or clips when you approve them.

## Creator loop

1. Fork this starter kit.
2. Copy `.env.example` to `.env` and add your own keys privately.
3. Fill out `payloads/sonicforge-creator-template/agents/template-agent/manifest.json`.
4. Bind workflows in `payloads/sonicforge-creator-template/workflows/registry.json`.
5. Run `python3 scripts/verify_starter_kit.py`.
6. Start the launch cockpit and inspect `/launch` and `/setup`.
7. Generate/cache voices and tracks only after flipping your own local gates.
8. Mix offline with a timeline manifest first.

## Replace to make it yours

Project name, performer name, host personas, show format, safety rules, workflow registry cards, visual identity, setup copy, and deployment domain.

Do **not** replace safety with vibes. Keep the gates.

## Recommended first demo

Use a tiny intro -> song -> bridge -> song -> outro format.

Acceptance checks: no voice-over-voice overlap, no accidental full-song overlap, timeline manifest exists before render, final duration is close to expected duration, no private endpoint/token printed in logs, and assets stay local/private until approved.
