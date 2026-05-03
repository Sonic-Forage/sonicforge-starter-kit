from __future__ import annotations


def build_ecosystem_status() -> dict:
    """Forkable SonicForge universe / Intergalactic DJs collective map.

    This is a read-only product/ecosystem contract for the launch UI. It does not
    publish, upload, train, call providers, start GPUs, or create accounts.
    """
    builder_paths = [
        {
            'id': 'clone_station',
            'label': 'Clone a party station',
            'who': 'DJs, VJs, party hosts, scene builders',
            'first_safe_action': 'Fork repo, copy .env.example, run local verifier, keep providers closed.',
            'shareable_artifact': 'agent payload + workflow registry + local setup notes',
        },
        {
            'id': 'build_agent',
            'label': 'Build a new DJ/VJ agent',
            'who': 'performer personas and collectives',
            'first_safe_action': 'Start from agents/template-agent and write manifest/persona/safety notes.',
            'shareable_artifact': 'agent pack with prompt contract, visual identity, crate memory, safety copy',
        },
        {
            'id': 'skill_plugin',
            'label': 'Create skills and plugins',
            'who': 'Hermes operators and workflow builders',
            'first_safe_action': 'Add docs-only skill/plugin card before wiring real APIs.',
            'shareable_artifact': 'Hermes skill, workflow card, adapter contract, verifier needles',
        },
        {
            'id': 'custom_model_training',
            'label': 'Customize models later',
            'who': 'model trainers and scene archivists',
            'first_safe_action': 'Create dataset card, consent/rights notes, eval plan, and no-go approval packet first.',
            'shareable_artifact': 'dataset review pack, eval harness, model card draft; no training until approval',
        },
    ]
    team_roles = [
        {'name': 'Intergalactic DJs', 'role': 'collective / show layer', 'claim': 'the visible team and movement people can join'},
        {'name': 'DJ VANTA', 'role': 'first canonical autonomous performer', 'claim': 'the first clone, not the whole product'},
        {'name': 'SonicForge Live', 'role': 'runtime / universe / local Party AI OS', 'claim': 'the forkable operating system people build on'},
        {'name': 'Hermes', 'role': 'agent home / skill and command layer', 'claim': 'memory, tools, skills, verification, autonomy'},
        {'name': 'ComfyUI', 'role': 'visual workflow engine', 'claim': 'operator-armed visual spells and workflow cards'},
    ]
    return {
        'ok': True,
        'status': 'forkable_collective_ecosystem_map_read_only',
        'positioning': 'Intergalactic DJs is the team/collective first; SonicForge Live is the universe/runtime behind it; DJ VANTA is the first clone.',
        'launch_line': 'The elite AI party is invite-only. The builder party is forkable.',
        'team_roles': team_roles,
        'builder_paths': builder_paths,
        'share_model': {
            'agents': 'share agent payloads, crate memories, lore sheets, safety notes',
            'skills': 'share Hermes skills and plugin recipes',
            'workflows': 'share ComfyUI workflow cards and model ledgers, not secrets',
            'models': 'share dataset/model cards and eval results only after consent, license, and human approval',
        },
        'closed_gates': ['no dataset upload', 'no model training', 'no public deploy', 'no paid GPU', 'no provider calls', 'no outreach/payment automation without explicit approval'],
        'starts_gpu': False,
        'starts_paid_api': False,
        'publishes_stream': False,
        'records_audio': False,
        'uploads_private_media': False,
        'trains_models': False,
        'requires_human_approval': True,
    }
