# Voice Demo — Simple steps

This document explains how to run the voice demo for the Always‑On AI Coworker in plain steps.

Prerequisites
- Windows with Python 3.11 (venv created by the project). The repository root is the `starter` folder.
- Populate `.env` (copy `.env.example` and paste real API keys).
- Have the project's virtualenv already created (`.venv`) and packages installed.

One-click start (easiest)
1. Open File Explorer and go to the `starter` folder.
2. Right-click `DEMO_START.ps1` → **Run with PowerShell**.

This opens four windows (MCP, Actions, Rasa, Voice) and waits for servers before starting the voice demo.

For a text-only run with a saved transcript, use `DEMO_RECORDING.ps1` instead.

**Record a presentation to share:** right-click **`DEMO_PRESENTATION.ps1`** → Run with PowerShell (spoken audio + transcript).  
If your **recording** is silent but you heard audio live, enable **system audio** in Win+G or OBS — see **`RECORDING.md`**.

Manual start (PowerShell)
1. Open PowerShell and change to the `starter` folder:

```powershell
Set-Location -Path 'D:\RASAHack\MyTwinAgent-rasa-bos-hackathon-2026\starter'
```

2. Activate the virtual environment:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

3. Start three terminals (one per step) and run these commands respectively:

- Terminal 1 — Action server (keep open):
```powershell
python -m rasa run actions
```

- Terminal 2 — Rasa server with sub-agents (keep open):
```powershell
python -m rasa run --enable-api --cors "*" --sub-agents agentic/sub_agents
```

- Terminal 0 — MCP tool server (only for agentic/Level‑2 features):
```powershell
python agentic/servers/ops_mcp_server/server.py
```

- Terminal 3 — Start the demo voice loop (run after the servers are up):
```powershell
python -m voice.demo
```

Quick text-only demo (no audio):
```powershell
python -m voice.demo --text
```

Troubleshooting
- If you see "Couldn't find ffmpeg", install ffmpeg and add it to `PATH` (required for audio playback by `pydub`).
- If the demo cannot connect to Rasa, ensure the Rasa server is started and reachable on port 5005.
- If you don't have demo audio clips, run:
```powershell
python -m voice.generate_audio
```
- If the LLM is slow or you see token / context errors, use the lighter model file:
```powershell
python -m rasa run --enable-api --cors "*" --endpoints endpoints.light.yml --sub-agents agentic/sub_agents
```
  Copy the exact model id from your Nebius Token Factory console into `endpoints.light.yml` if needed.

Stopping
- Press `Ctrl+C` in order: Voice → Rasa → Actions → MCP.
