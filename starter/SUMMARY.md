# Project summary and quick references

This file gives a short, clean context of what was done, prerequisites, and copy-paste steps for running the voice demo and Rasa e2e tests.

Prerequisites
- Windows, Python 3.10/3.11, project virtualenv at `.venv` (created via `pip install -e .`).
- Populate `.env` with keys (NEBIUS_API_KEY, Speechmatics credentials, Rime credentials) — copy from `.env.example`.
- `ffmpeg` recommended for audio playback (install and add to `PATH`).

Voice demo (summary)
1. Activate venv and change to `starter`:

```powershell
Set-Location -Path 'D:\RASAHack\MyTwinAgent-rasa-bos-hackathon-2026\starter'
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

2. Start the required services (three terminals):

```powershell
# MCP (optional - Level 2/agentic)
python agentic/servers/ops_mcp_server/server.py

# Actions
python -m rasa run actions

# Rasa with sub-agents
python -m rasa run --enable-api --cors "*" --sub-agents agentic/sub_agents
```

3. Run demo (voice) after servers are ready:

```powershell
python -m voice.demo
# or text-only (easier to record):
python -m voice.demo --text
```

One-click scripts
- `DEMO_START.ps1` — opens MCP, Actions, Rasa, and Voice in separate windows (voice demo).
- `DEMO_RECORDING.ps1` — same servers plus a text demo that saves `demo_recording_YYYYMMDD-HHMMSS.log`.
- `DEMO_PRESENTATION.ps1` — full 2-act judge demo + Markdown transcript in `recordings/` (see `RECORDING.md`).

Switching LLM models / token limits
- Do NOT modify Python source files. Use an `endpoints` file that points to the desired Nebius model id.
- **Token max / slow responses:** use `endpoints.light.yml` (Gemma 3 27B fast, `max_tokens: 2048`):
```powershell
python -m rasa run --enable-api --cors "*" --endpoints endpoints.light.yml --sub-agents agentic/sub_agents
```
- For any other model, copy `endpoints.yml` to e.g. `endpoints.custom.yml`, replace the `model:` field, and pass `--endpoints endpoints.custom.yml`.

Rasa e2e tests
- Run the e2e tests and save results (PowerShell):

```powershell
# $env:RASA_PRO_BETA_STUB_CUSTOM_ACTION = 'true'
python -m rasa test e2e tests/e2e -v
```

Presentation recording notes
- For video/audio capture (screen + system audio), use OBS Studio — easiest and highest quality.
- `DEMO_RECORDING.ps1` records console transcripts only. To capture spoken audio, either (a) record system audio via OBS or (b) configure ffmpeg with a loopback device (advanced).

UI recommendation
- For a short demo, the local CLI (voice or text) is fine and fast to present.
- If you want a more polished demo for non-technical audiences, add a minimal web UI: a single-page app (HTML+JS) that posts to Rasa webhook and plays returned audio. This can be done later as an optional enhancement.

Files added in this pass
- `DEMO_START.ps1`, `DEMO_RECORDING.ps1` (fixed), `endpoints.light.yml`, `DEMO.md`, `SUMMARY.md`.
