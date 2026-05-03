# RTMP / OBS / Resolume / Spout Routing Notes

## Easiest live setup

1. Run SonicForge Live locally.
2. Open `/visualizer` in a separate browser window.
3. Capture the browser window in OBS or Resolume.
4. Route audio from the clean-mix output or DAW into OBS.
5. Stream from OBS to RTMP.

## Direct RTMP later

FFmpeg shape:

```bash
ffmpeg -re -i clean_mix.wav -f x11grab -i :0.0 -c:v libx264 -preset veryfast -c:a aac -f flv "$RTMP_TARGET"
```

This repo should generate commands/plans first, not run public stream pushes by default.

## Resolume

Options:

- Browser source/window capture.
- NDI from OBS into Resolume.
- TouchDesigner Spout/Syphon output into Resolume.

## TouchDesigner / Spout

TD can read SonicForge state via WebSocket/HTTP and output Spout. Hermes twozero MCP can build the TD patch if TouchDesigner is running locally with MCP enabled.
