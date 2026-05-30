# Record a shareable presentation



Use this guide to produce a **video with spoken audio** and a **written transcript** you can share with judges.



## Fastest path (recommended)



1. Open File Explorer → go to the `starter` folder.

2. Right-click **`DEMO_PRESENTATION.ps1`** → **Run with PowerShell**.

3. Before pressing Enter, start recording:

   - **Windows built-in:** press **Win + G** → Capture → Record.

   - **Higher quality:** [OBS Studio](https://obsproject.com/) → Window Capture on **Demo — Presentation**.

4. **Important:** enable **system / application audio** in your recorder (see below).

5. Press **Enter** — servers start, voice clips generate if needed, then the spoken demo runs.

6. Stop the recorder when the demo finishes.



### What you get



| File | Location |

|------|----------|

| Shareable transcript (Markdown) | `starter/recordings/presentation_YYYYMMDD-HHMMSS.md` |

| Console log | `starter/recordings/presentation_YYYYMMDD-HHMMSS.log` |

| Your video | e.g. `Videos/Captures/` (Game Bar) or OBS output folder |



---



## Why was voice muted?



Two common causes:



### 1. Text-only mode (fixed)



Earlier versions of `DEMO_PRESENTATION.ps1` ran `--text --presentation`, which **never plays audio** — only text panels in the terminal.



The script now runs **`--presentation` with spoken audio** (pharmacist + RxTwin voices). Re-run the updated script.



### 2. Screen recorder not capturing system audio



**Xbox Game Bar (Win + G)** often records **microphone only**, not speaker output. Your demo may be playing audio, but the recording is silent.



**Fix for Game Bar:**

1. Open **Settings → Gaming → Captures**.

2. Turn on **Record audio when I record a game**.

3. Set audio to capture **Game** or **All** (wording varies by Windows version).

4. In the Game Bar widget, open capture settings and ensure **Audio** is enabled.



**Fix for OBS (recommended for presentations):**

1. Add **Window Capture** → select **Demo — Presentation**.

2. Settings → **Audio** → Desktop Audio: **Default** (captures speaker output).

3. Optional: add **Mic/Aux** for live narration.



### 3. ffmpeg missing (audio never plays on your PC)



If you see `[WARNING] Audio playback failed` in the terminal, install ffmpeg:



```powershell

winget install Gyan.FFmpeg

```



Close and reopen PowerShell, then re-run the demo. Verify:



```powershell

ffmpeg -version

```



---



## What the demo shows (~90 seconds)



**Act 1 — Report temperature excursion**

- Pharmacist (Speechmatics voice) greets RxTwin and reports Fridge B alarm.

- RxTwin (Rime voice) opens an urgent ticket and can query SOPs via MCP.



**Act 2 — Shift resume**

- New session; RxTwin remembers the open ticket from `.data/tickets.json`.



---



## Manual commands



```powershell

Set-Location D:\RASAHack\MyTwinAgent-rasa-bos-hackathon-2026\starter

.\.venv\Scripts\Activate.ps1



# Generate pharmacist clips once (needs SPEECHMATICS_API_KEY)

python -m voice.generate_audio



# Spoken 2-act presentation + transcript

python -m voice.demo --presentation --pause 4 --transcript recordings\my_demo.md



# Text only (no audio — for quick dry runs)

python -m voice.demo --text --presentation --pause 4 --transcript recordings\my_demo.md

```



---



## Troubleshooting



| Problem | Fix |

|---------|-----|

| Video has no voice but you heard it live | Enable system/desktop audio in Game Bar or OBS |

| No sound at all during demo | Install ffmpeg; check volume; see warning in terminal |

| `SPEECHMATICS_API_KEY is not set` | Copy `.env.example` → `.env` and add keys |

| Rime voice fails | Add `RIME_API_KEY` to `.env` or use `--tts speechmatics` |

| Blank or slow replies | Wait for Rasa to finish loading; script uses `endpoints.light.yml` |

| "Sorry, I am having trouble with that" | **Restart the Rasa terminal** (Ctrl+C, re-run). LLM model id was wrong — now fixed in `endpoints.light.yml` |

| Transcript empty | Check `recordings/` folder after demo completes |


