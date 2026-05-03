const log = document.getElementById('log');
function add(msg){ log.textContent = `[${new Date().toLocaleTimeString()}] ${msg}\n` + log.textContent; }
function setText(id, text){ const el = document.getElementById(id); if(el) el.textContent = text || ''; }
function renderCrateCache(crate){
  const el = document.getElementById('crateCacheList');
  if(!el) return;
  const entries = (crate.entries || []).slice(0, 6);
  el.innerHTML = entries.map(e => `<article><b>${e.name}</b><span>${e.id} · ${e.mode} · ${e.bpm} BPM · energy ${e.energy}</span><small>${(e.genre_tags || []).join(' / ')}<br>${e.visual_spell_text || ''}<br>${e.lineage_note || ''}</small></article>`).join('') || 'No prompt crate entries found.';
}
function renderEcosystem(status){
  if(!status || !status.ok) return;
  const rolesEl = document.getElementById('ecosystemRoleList');
  setText('ecosystemPositioning', `${status.positioning} ${status.launch_line}`);
  if(rolesEl){
    rolesEl.innerHTML = (status.team_roles || []).map(role => `<article><b>${role.name}</b><span>${role.role}</span><small>${role.claim}</small></article>`).join('') || 'No ecosystem roles found.';
  }
  const paths = (status.builder_paths || []).map(path => `${path.label}: ${path.shareable_artifact}`).join(' · ');
  setText('ecosystemShareModel', `${paths} · closed gates: ${(status.closed_gates || []).join(' · ')} · trains_models=${status.trains_models}`);
}
function summarizePromptStack(stack){
  if(!Array.isArray(stack) || !stack.length) return 'No prompt stack yet.';
  return stack.map(s => String(s).replace(/\s+/g, ' ').slice(0, 110)).join(' // ');
}
function renderDeckCards(payload){
  const deckA = payload.deck_a || {};
  const deckB = payload.deck_b || {};
  const crate = payload.crate_selection || {};
  const spell = payload.visual_spell || deckB.visual_spell || {};
  const safetyA = Array.isArray(deckA.safety_notes) ? deckA.safety_notes.join(' ') : 'Mock/local state only.';
  const safetyB = Array.isArray(deckB.safety_notes) ? deckB.safety_notes.join(' ') : 'Deck B remains dry-run until explicitly approved.';
  setText('deckATitle', deckA.name || 'Deck A / current groove');
  setText('deckAStatus', `Status: ${deckA.status || 'waiting'} · role=${deckA.role || 'A'} · artifact=${deckA.artifact_path || 'none/local mock pending'}`);
  setText('deckAMeta', `${deckA.bpm || '—'} BPM · ${deckA.key || 'key TBD'} · energy ${deckA.energy ?? '—'} · gain ${deckA.gain ?? '—'}`);
  setText('deckAPrompt', summarizePromptStack(deckA.prompt_stack));
  setText('deckASafety', safetyA);
  setText('deckBTitle', deckB.name || 'Deck B / incoming portal');
  setText('deckBStatus', `Status: ${deckB.status || 'incoming'} · role=${deckB.role || 'B'} · artifact=${deckB.artifact_path || 'mock artifact not rendered yet'}`);
  setText('deckBMeta', `${deckB.bpm || '—'} BPM · ${deckB.key || 'key TBD'} · energy ${deckB.energy ?? '—'} · gain ${deckB.gain ?? '—'}`);
  setText('deckBCrate', crate.id ? `${crate.name} (${crate.id}) · ${crate.mode} · ${(crate.genre_tags || []).join(' / ')} · ${crate.starts_gpu === false ? 'GPU closed' : 'closed gate'}` : safetyB);
  setText('deckBSpell', `${spell.scene || spell.workflow || 'visual spell'} · mode=${spell.mode || 'dry_run'} · ${spell.text || 'PHRASE_LOCK / BASS_SWAP / SURVIVAL_PING'}`);
}
function renderDjBrainState(brain){
  if(!brain || !brain.ok) return;
  const deckB = brain.deck_b || {};
  const phrase = brain.phrase_count || {};
  const eq = brain.eq_move || {};
  const crowd = brain.crowd_signal || {};
  const beat = brain.beatmatch || {};
  setText('brainBpmKeyEnergy', `${brain.bpm || deckB.bpm || '—'} BPM · Deck B key ${deckB.key || 'TBD'} · energy ${brain.energy ?? deckB.energy ?? '—'} · mode ${brain.mode || 'build'}`);
  setText('brainPhraseCount', `intro ${phrase.intro_bars || 16} bars · mix-in ${phrase.mix_in_bar || 1} · bass swap ${phrase.bass_swap_bar || 17} · release ${phrase.drop_release_bar || 33} · outro ${phrase.outro_bars || 16}`);
  setText('brainEqMove', `bar ${eq.bar || 1}: LOW ${eq.low_db ?? '—'} dB · MID ${eq.mid_db ?? '—'} dB · HIGH ${eq.high_db ?? '—'} dB · ${eq.filter || 'filter TBD'} · ${eq.note || 'metadata-only EQ move'}`);
  setText('brainCrowdSignal', `${crowd.synthetic_state || crowd.response || 'synthetic'} · care=${crowd.care_intervention || 'none'} · energy ${crowd.energy ?? '—'} · density ${crowd.density ?? '—'} · palette ${crowd.visual_palette_hint || 'browser-safe'} · ${crowd.operator_note || crowd.observed_signal || 'synthetic crowd state only; no hidden mic/crowd recording'}`);
  setText('brainBeatmatch', `${beat.current_bpm || brain.bpm || '—'}→${beat.next_bpm || deckB.bpm || '—'} BPM · shift ${beat.tempo_shift_percent ?? 0}% · compatible=${beat.compatible ?? true}`);
  setText('brainSafetyStatus', `${brain.honest_status || 'read_only_preview_no_generation_no_continuous_mixer'} · starts_gpu=${brain.starts_gpu} · starts_paid_api=${brain.starts_paid_api} · records_audio=${brain.records_audio} · ${brain.human_override || 'human override visible'}`);
}
function renderSegment(j){
  const payload = j.payload || {};
  const survival = payload.survival_kit || {};
  const culture = payload.culture_cue || {};
  const deckA = payload.deck_a || {};
  const deckB = payload.deck_b || {};
  const visualSpell = payload.visual_spell || {};
  const comfySpell = payload.comfyui_visual_spell || {};
  const crate = payload.crate_selection || {};
  const crossfader = payload.transition?.crossfader || payload.mix?.crossfader_curve || {};
  const manifest = payload.set_manifest || {};
  if(survival.message){
    setText('survivalMessage', `${survival.mode || 'survival'}: ${survival.message} Human override: ${survival.human_override || 'ask sober humans/venue staff when needed.'}`);
    setText('survivalChecklist', Array.isArray(survival.checklist) ? survival.checklist.join(' · ') : 'water · earplugs · buddy check · exits · chill zone · human override');
  }
  if(culture.message){
    setText('cultureMessage', `${culture.mode || 'culture'}: ${culture.message}`);
    setText('cultureLineage', `${culture.lineage || 'dance-music lineage'} · ${culture.respect_note || 'AI is a guest in the room.'}`);
  }
  if(payload.mc_break){
    renderMcBreakPreview({ ok: true, modes: { [payload.mc_break.mode || 'planned']: payload.mc_break }, status: 'planned_segment_mc_break_text_first' });
  }
  if(deckA.role || deckB.role){
    renderDeckCards(payload);
    setText('deckStatus', `${deckA.name || 'Deck A'} (${deckA.status || 'current'}) → ${deckB.name || 'Deck B'} (${deckB.status || 'incoming'}). ${payload.transition?.summary || 'Dry-run handoff metadata only.'}`);
    setText('visualSpellStatus', `${visualSpell.workflow || 'visual spell'} · mode=${visualSpell.mode || 'dry_run'} · targets=${(visualSpell.route_targets || ['browser']).join(', ')}`);
    if(comfySpell.workflow){
      const input = comfySpell.input || {};
      setText('comfySpellStatus', `${comfySpell.client_route || 'COMFYUI_DRY_RUN'} · ${comfySpell.workflow} · prompt_id=${(comfySpell.output || {}).prompt_id || 'none'} · seed=${input.seed || 'local'} · starts_gpu=${comfySpell.starts_gpu} · starts_paid_api=${comfySpell.starts_paid_api} · ${comfySpell.safety || 'dry-run only'}`);
    }
    if(crate.id){
      setText('crateSelectionStatus', `Selected crate for Deck B: ${crate.name} (${crate.id}) · ${crate.mode} · ${crate.bpm} BPM · ${crate.survival_ping || 'survival ping'} · provider-closed local seed`);
    }
    if(crossfader.curve || crossfader.formula){
      const points = Array.isArray(crossfader.automation) ? crossfader.automation.map(p => `${p.value}:${p.gain_a}/${p.gain_b}`).join(' · ') : (crossfader.automation_bars || []).join('/');
      setText('crossfaderStatus', `Equal-power crossfader: ${crossfader.formula || 'gainA/gainB cosine-sine curve'} · ${points}`);
    }
    const eqSchedule = payload.mix?.eq_move_schedule || {};
    if(eqSchedule.status){
      const moves = Array.isArray(eqSchedule.automation) ? eqSchedule.automation.map(step => `bar ${step.bar}: LOW ${step.low_db} / MID ${step.mid_db} / HIGH ${step.high_db}`).join(' · ') : 'automation pending';
      setText('eqMoveScheduleStatus', `EQ move schedule: ${eqSchedule.status} · ${eqSchedule.low_swap || 'low swap'} · ${eqSchedule.mid_carve || 'mid carve'} · ${eqSchedule.high_shimmer || 'high shimmer'} · ${moves} · records_audio=${eqSchedule.records_audio} · requires_human_approval=${eqSchedule.requires_human_approval}`);
    }
    const duckPlan = payload.mix?.talk_over_intro_ducking_plan || {};
    if(duckPlan.status){
      const steps = Array.isArray(duckPlan.automation) ? duckPlan.automation.map(step => `${step.at_seconds}s/bar ${step.bar}: music ${step.music_gain_db}dB`).join(' · ') : 'automation pending';
      setText('talkDuckingStatus', `Talk-over-intro ducking plan: ${duckPlan.status} · talk ${duckPlan.talk_over_intro_seconds}s · duck ${duckPlan.duck_music_db}dB · clear before bar ${duckPlan.target_clear_before_bar} · ${steps} · records_audio=${duckPlan.records_audio} · publishes_stream=${duckPlan.publishes_stream}`);
    }
    if(manifest.manifest_path){
      setText('setManifestStatus', `Local Set Manifest Writer: ${manifest.manifest_path} · segments=${manifest.segment_count || 0} · records_audio=${manifest.records_audio} · publishes_stream=${manifest.publishes_stream} · ${manifest.note || 'metadata only'}`);
    }
    if(payload.program_status){
      renderProgramStatus(payload.program_status);
    }
    if(payload.program_manifest){
      renderProgramManifest(payload.program_manifest);
    }
  }
}
let latestMcBreakPreview = null;
function renderMcBreakPreview(preview){
  const el = document.getElementById('mcBreakPreview');
  if(!el || !preview) return;
  latestMcBreakPreview = preview;
  const modes = preview.modes || {};
  const selected = document.getElementById('cultureModeSelect')?.value;
  const entries = selected && modes[selected] ? [[selected, modes[selected]]] : Object.entries(modes);
  const rows = entries.map(([mode, item]) => {
    const talk = item.talk || {};
    return `<article><b>${mode}</b><span>${item.label || 'text-first MC break'} · ${item.tts_status || 'text_first_no_audio_output'}</span><small>${item.text || talk.text || ''}<br>${item.visual_spell || 'VISUAL_SPELL'} · sends_voice_message=${item.sends_voice_message} · records_audio=${item.records_audio}</small></article>`;
  });
  el.innerHTML = rows.join('') || 'No MC break preview modes available.';
  setText('mcBreakStatus', `${preview.status || 'text_first_mc_break_generator_fail_closed'} · culture_mode_selector_fail_closed · /api/mc-breaks/preview · starts_gpu=${preview.starts_gpu ?? false} · starts_paid_api=${preview.starts_paid_api ?? false} · publishes_stream=${preview.publishes_stream ?? false}`);
}
function applyCultureModeSelector(){
  if(!latestMcBreakPreview) return;
  const selected = document.getElementById('cultureModeSelect')?.value || 'history';
  renderMcBreakPreview(latestMcBreakPreview);
  const item = latestMcBreakPreview.modes?.[selected] || {};
  const talkText = item.text || item.talk?.text || '';
  const talkEl = document.getElementById('talk');
  if(talkText && talkEl) talkEl.value = talkText;
  setText('cultureMessage', `${selected}: ${talkText || 'Text-first culture mode preview only.'}`);
  setText('cultureLineage', `${item.visual_spell || 'LINEAGE_SIGNAL'} · selector preview only · no voice/provider/recording/stream`);
  add(`culture mode selector preview: ${selected} · text-first only · no external lane opened`);
}
function renderSamplePad(j){
  const p = j.payload || {};
  setText('samplePadStatus', `${p.pad || 'PAD'} · ${p.label || 'ritual cue'} · ${p.talk_break_mode || 'dry_run'} · ${p.visual_spell || 'VISUAL_SPELL'} · ${p.safe_scope || 'safe local cue only'}`);
  if((p.visual_spell || '').includes('SURVIVAL_PING')){
    setText('survivalMessage', `${p.label || 'survival'}: ${p.message || ''} Human override: ${p.human_override || 'sober operator can stop the set.'}`);
  }
  setText('visualSpellStatus', `${p.visual_spell || 'sample pad visual spell'} · targets=${(p.route_targets || ['browser']).join(', ')} · mode=${p.mode || 'dry_run'}`);
}
function renderProgramStatus(status){
  if(!status || !status.ok) return;
  const lanes = status.lanes || {};
  const mock = lanes.mock_audio_sketch || {};
  const real = lanes.real_generated_audio || {};
  const rendered = lanes.rendered_program_mix || {};
  const rec = lanes.recording_and_stream || {};
  const mix = status.mix_metadata || {};
  setText('mockAudioStatus', `${mock.state || 'pending'} · artifact=${mock.artifact_path || mix.latest_track_file || 'none yet'} · adapter=${mock.adapter || 'mock'} · ${mock.claim || 'local sketch only'}`);
  setText('realGeneratedAudioStatus', `${real.state || 'closed_until_human_approval'} · ${(real.adapters || []).join(' / ') || 'provider contracts only'} · ${real.claim || 'no provider started'}`);
  setText('renderedProgramStatus', `${rendered.state || 'not_rendered'} · artifact=${rendered.artifact_path || 'none'} · ${rendered.claim || 'no continuous mix renderer verified'}`);
  setText('recordingStreamStatus', `${rec.state || 'closed_until_human_approval'} · ${rec.claim || 'no recording/upload/stream started'}`);
  setText('programStatusSummary', `${status.status || 'honest_program_status_mock_audio_no_rendered_program'} · segments=${mix.segment_count || 0} · crossfade=${mix.crossfade_seconds ?? 'metadata pending'}s · duck=${mix.duck_music_db ?? 'pending'}dB · target_lufs=${mix.target_lufs ?? 'pending'} · starts_gpu=${status.starts_gpu} · records_audio=${status.records_audio} · publishes_stream=${status.publishes_stream}`);
}
function renderProgramManifest(manifest){
  const el = document.getElementById('programManifestList');
  if(!el || !manifest) return;
  const rows = manifest.segments || [];
  el.innerHTML = rows.map(row => `<article><b>${row.segment_id}</b><span>${row.duration_seconds || 0}s · crossfade ${row.crossfade_seconds || 0}s · duck ${row.duck_music_db ?? 'pending'} dB · target LUFS ${row.target_lufs ?? 'pending'}</span><small>${row.crossfader || 'equal_power metadata pending'}<br>EQ bar ${row.eq_move_schedule?.bar ?? '—'} · LOW ${row.eq_move_schedule?.low_db ?? '—'} / MID ${row.eq_move_schedule?.mid_db ?? '—'} / HIGH ${row.eq_move_schedule?.high_db ?? '—'} · ${row.eq_move_schedule?.note || 'metadata-only EQ move'}<br>${row.survival_ping || 'SURVIVAL_PING pending'} · ${row.culture_cue || 'culture cue pending'} · ${row.honest_status}</small></article>`).join('') || 'No local set segments yet. Press Plan Next Continuous Segment to append metadata first.';
  setText('programManifestSummary', `${manifest.status || 'local_program_manifest_renderer_metadata_only'} · /api/program-manifest · segments=${manifest.segment_count || 0} · estimated=${manifest.estimated_program_seconds || 0}s · target_lufs=${manifest.target_lufs ?? 'pending'} · renders_program_audio=${manifest.renders_program_audio} · records_audio=${manifest.records_audio} · publishes_stream=${manifest.publishes_stream}`);
}
function renderBackendStatus(status){
  const el = document.getElementById('backendStatusList');
  if(!el || !status) return;
  const lanes = status.lanes || [];
  el.innerHTML = lanes.map(lane => {
    const blocked = (lane.blocked_without_approval || []).slice(0, 4).join(' · ');
    const routes = (lane.routes_when_enabled || []).slice(0, 6).join(' ');
    return `<article><b>${lane.label}</b><span>${lane.lane} · ${lane.state} · env ${lane.enabled_env}=${lane.enabled}</span><small>${lane.purpose}<br>First safe action: ${lane.first_safe_action}<br>blocked action: ${blocked}<br>${routes}</small></article>`;
  }).join('') || 'No backend lanes found.';
  setText('backendStatusSummary', `${status.status || 'backend_status_card_fail_closed_no_provider_calls'} · ${status.summary || 'provider lanes closed'} · starts_gpu=${status.starts_gpu} · starts_paid_api=${status.starts_paid_api} · publishes_stream=${status.publishes_stream} · records_audio=${status.records_audio} · uploads_private_media=${status.uploads_private_media} · requires_human_approval=${status.requires_human_approval}`);
}
function renderTimeline(timeline){
  const el = document.getElementById('timelinePreview');
  if(!el || !timeline) return;
  const plans = timeline.plans || [];
  el.innerHTML = plans.map(plan => {
    const first = (plan.segments || [])[0] || {};
    const last = (plan.segments || [])[Math.max(0, (plan.segments || []).length - 1)] || first;
    return `<article><b>${plan.id}</b><span>${plan.minutes} minutes · ${plan.segment_count} segments · ${timeline.status}</span><small>First: ${first.track_title || 'Signal 01'} · ${first.visual_spell_text || 'visual spell pending'}<br>Final: ${last.mode || 'comedown'} · ${last.survival_ping || 'SURVIVAL_PING'} · ${last.culture_mode || 'culture'}<br>${timeline.operator_rule || 'human approval required before live providers'}</small></article>`;
  }).join('') || 'No timeline plans found.';
  setText('autopilotStatus', `${timeline.status || 'local_plan_only_fail_closed'} · starts_gpu=${timeline.starts_gpu} · records_audio=${timeline.records_audio} · publishes_stream=${timeline.publishes_stream} · no live scheduler`);
}
async function loadTimeline(method='GET'){
  const r = await fetch('/api/timeline' + (method === 'POST' ? '/build' : ''), { method });
  const j = await r.json();
  renderTimeline(j);
  add(`timeline ${method === 'POST' ? 'built' : 'loaded'}: ${(j.plans || []).map(p => p.id).join(', ')}`);
  return j;
}
function setAutopilotPreview(active){
  const mode = active ? 'DRY-RUN AUTOPILOT PREVIEW ARMED' : 'DRY-RUN AUTOPILOT PREVIEW STOPPED';
  setText('autopilotStatus', `${mode} · browser-side rehearsal marker only · timeline_plan_only_no_generation_no_continuous_mixer · starts_gpu=false · records_audio=false · publishes_stream=false`);
  add(`${mode}: no timer, no mixer, no provider, no recording, no stream started`);
}
async function post(url, body){ const r = await fetch(url,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)}); const j=await r.json(); if(url==='/api/next-segment') renderSegment(j); add(JSON.stringify(j,null,2)); return j; }
const ws = new WebSocket(`${location.protocol==='https:'?'wss':'ws'}://${location.host}/ws/control`);
ws.onmessage = ev => add(ev.data); ws.onopen = () => add('socket open'); ws.onerror = () => add('socket error');
document.getElementById('sendGuide').onclick = () => post('/api/guide',{guide:guide.value, bpm:+bpm.value});
document.getElementById('genTrack').onclick = () => post('/api/generate-track',{title:title.value,bpm:+bpm.value,style:style.value,duration_seconds:12,prompt:guide.value});
document.getElementById('queueTalk').onclick = () => post('/api/talk-break',{text:talk.value,seconds:8,duck_music_db:-8});
document.getElementById('visual').onclick = () => post('/api/visual',{scene:scene.value,palette:'black, cyan, magenta, ultraviolet',intensity:8,output_mode:'browser_window'});
document.getElementById('nextSegment').onclick = () => post('/api/next-segment',{});
document.getElementById('buildTimeline').onclick = () => loadTimeline('POST');
document.getElementById('loadTimeline').onclick = () => loadTimeline('GET');
document.getElementById('startDryRunAutopilot').onclick = () => setAutopilotPreview(true);
document.getElementById('stopDryRunAutopilot').onclick = () => setAutopilotPreview(false);
document.getElementById('applyCultureMode').onclick = () => applyCultureModeSelector();
document.getElementById('cultureModeSelect').onchange = () => applyCultureModeSelector();
document.querySelectorAll('.pad-button').forEach(btn => btn.onclick = () => post('/api/sample-pad',{pad:btn.dataset.pad}).then(renderSamplePad));
fetch('/health').then(r=>r.json()).then(j=>add('health '+JSON.stringify(j,null,2)));
fetch('/api/dj-brain/state').then(r=>r.json()).then(j=>{ renderDjBrainState(j); add(`DJ brain read-only preview loaded: ${j.honest_status}`); }).catch(()=>add('DJ brain preview unavailable'));
fetch('/api/program-status').then(r=>r.json()).then(j=>{ renderProgramStatus(j); add(`program status loaded: ${j.status}`); }).catch(()=>add('program status unavailable'));
fetch('/api/program-manifest').then(r=>r.json()).then(j=>{ renderProgramManifest(j); add(`program manifest renderer loaded: ${j.status}`); }).catch(()=>add('program manifest renderer unavailable'));
fetch('/api/backends').then(r=>r.json()).then(j=>{ renderBackendStatus(j); add(`backend status loaded: ${j.status}`); }).catch(()=>add('backend status unavailable'));
fetch('/api/ecosystem').then(r=>r.json()).then(j=>{ renderEcosystem(j); add(`ecosystem map loaded: ${j.status}`); }).catch(()=>add('ecosystem map unavailable'));
fetch('/api/mc-breaks/preview').then(r=>r.json()).then(j=>{ renderMcBreakPreview(j); add(`MC break preview loaded: ${j.status}`); }).catch(()=>add('MC break preview unavailable'));
fetch('/api/crate-cache').then(r=>r.json()).then(j=>{ renderCrateCache(j); add(`crate cache loaded: ${(j.entries || []).length} local prompt packs`); }).catch(()=>add('crate cache unavailable'));
