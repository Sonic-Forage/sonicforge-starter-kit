# Resource / Safety Policy

Default behavior:

- No GPU starts.
- No paid API calls.
- No public stream publishing.
- No hidden recording.
- No voice cloning.
- No secret commits.

External backends require both env flags and human approval:

- GPU or cloud generation: `SONICFORGE_ALLOW_GPU=true` + explicit approval.
- Paid API: `SONICFORGE_ALLOW_PAID_API=true` + explicit approval.
- Public stream/RTMP: `SONICFORGE_ALLOW_PUBLIC_STREAM=true` + exact target confirmation.

TTS policy:

- Text talk-breaks are safe defaults.
- Voice output only when explicitly requested.
- Real-person voice cloning requires consent.
