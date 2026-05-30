<div align="center">

<h1>🤖 RxTwin — Pharmaceutical Compliance AI Coworker</h1>

<h3>Boston Tech Week 2026 · Team RXtwin</h3>

<p>
  <b>TL;DR: RxTwin automates pharmaceutical compliance by letting pharmacists log and resolve incidents through natural voice, with persistent memory across shifts.</b>
</p>

<p>
  An always-on AI coworker for pharmaceutical compliance workflows. RxTwin helps pharmacists log clinical exceptions, track incidents across shifts, and maintain regulatory compliance — with persistent memory and voice interaction.
</p>

> [!NOTE]
> **Why it matters:**
> - Reduces compliance errors
> - Lowers regulatory risk
> - Saves pharmacist time

<p>
  <a href="#-problem">Problem</a> ·
  <a href="#-solution">Solution</a> ·
  <a href="#-architecture">Architecture</a> ·
  <a href="#-demo">Demo</a> ·
  <a href="#-quickstart">Quickstart</a>
</p>

</div>

<hr/>

<a id="-problem"></a>

## 🎯 The Problem

Pharmacies face strict regulatory requirements for logging clinical exceptions, but existing systems are:

- **Manual and error-prone** — paper-based or fragmented digital workflows
- **Context-blind** — no memory across shift changes
- **Slow** — documentation delays increase regulatory risk
- **Cognitively demanding** — pharmacists juggle compliance tasks during busy operations

**Impact:** Inconsistent reporting, increased audit exposure, and potential patient safety risks from missed temperature excursions or storage issues.

<a id="-solution"></a>

## 💡 The Solution: RxTwin

RxTwin is a hands-free, voice-driven AI coworker that:

- **Logs incidents instantly** through natural speech — no typing required
- **Guides pharmacists** through required regulatory steps deterministically
- **Maintains persistent memory** across shifts — recalls active incidents automatically
- **Generates audit-ready documentation** with timestamps and notifications
- **Reduces cognitive load** during busy operations by handling compliance workflows

**Key Differentiators:**
- ✅ **Cross-shift memory** — remembers incidents across shift changes
- ✅ **Deterministic flows** — no hallucinations in compliance-critical scenarios
- ✅ **Voice-first interaction** — hands-free logging while handling medications
- ✅ **Real-world workflow fit** — designed for actual pharmacy operations

## 💬 Sample Conversation

**Act 1 — Logging a Compliance Ticket**

```
👤 Pharmacist Divya: "Hello RxTwin, this is Pharmacist Divya."
🤖 RxTwin: "Hi Pharmacist Divya! All sensors are green."

👤 Pharmacist Divya: "I need to log a compliance ticket please."
🤖 RxTwin: "I can log that compliance ticket for you. What is the active exception or issue in the lab?"

👤 Pharmacist Divya: "Fridge B temperature alarm. It dropped to minus one Celsius."
🤖 RxTwin: "Understood. How urgent is this clinical exception — low, medium, high, or urgent?"

👤 Pharmacist Divya: "urgent"
🤖 RxTwin: "What's the best email address to send compliance notifications to?"

👤 Pharmacist Divya: "divya@rxlab.com"
🤖 RxTwin: "Done — I've logged incident TCK-7508 as a urgent-priority temperature exception.
          Shift updates will go to divya@rxlab.com."
```

**Act 2 — Shift Resume (Cross-Session Memory)**

```
👤 Pharmacist Divya: "Hey RxTwin, Pharmacist Divya is back on shift."
🤖 RxTwin: "Welcome back, Pharmacist Divya! I see we have an active Fridge B temperature excursion
          (incident TCK-7508: Fridge B temperature alarm."

👤 Pharmacist Divya: "Yes, we moved all the Shingrix vials to Fridge A safely."
🤖 RxTwin: "Perfect. I've marked incident TCK-7508 as resolved and logged the Shingrix transfer to Fridge A."

👤 Pharmacist Divya: "That is all for now. Thanks RxTwin."
🤖 RxTwin: "Thanks for working with me — I'll be right here whenever you need me."
```

This demonstrates **persistence** (remembering incidents across shifts), **resilience** (deterministic ticket logging), and a **real enterprise workflow** (pharmaceutical compliance).

<a id="-architecture"></a>

## 🏗️ Architecture

RxTwin is built on the Rasa CALM framework with a voice-first architecture:

```
            ears                   brain                  voice
 user  ──▶  Speechmatics ASR  ──▶  Rasa CALM (agent)  ──▶  Rime TTS  ──▶  user
                                        │
                                        ├── Nebius Token Factory  (LLM inference)
                                        └── Persistent ticket store (.data/tickets.json)
```

### Core Components

| Component | Role | Technology |
| :-- | :-- | :-- |
| **ASR** | Speech-to-text (ears) | Speechmatics |
| **Agent Brain** | Conversational reasoning | Rasa CALM |
| **LLM Inference** | Command generation | Nebius Token Factory |
| **TTS** | Text-to-speech (voice) | Rime |
| **Memory** | Cross-session persistence | JSON ticket store |
| **Flows** | Deterministic compliance workflows | Custom Rasa CALM flows |

### Custom Flows

- **`log_compliance_ticket`** — Guides pharmacists through incident logging with validation
- **`greet_and_resume`** — Shift resume with active incident recall
- **`resolve_incident`** — Incident resolution with audit trail
- **`end_shift`** — Shift handoff summary

### Why This Architecture Matters

- **Deterministic flows** prevent hallucination in compliance-critical scenarios
- **Persistent memory** ensures continuity across shift changes
- **Voice-first design** enables hands-free operation during medication handling
- **Modular stack** allows swapping components (ASR/TTS/LLM) without re-engineering

<hr/>

<a id="-demo"></a>

## 🎥 Demo

**Watch the 2-minute voice demo:**

[https://github.com/DivyaPrakash04/MyTwinAgent-rasa-bos-hackathon-2026/blob/main/Working_VoiceDemo_2026-05-30%20152317.mp4](https://github.com/DivyaPrakash04/MyTwinAgent-rasa-bos-hackathon-2026/blob/main/Working_VoiceDemo_2026-05-30%20152317.mp4)

**Demo highlights:**
- Real-time ASR (Speechmatics) transcribing pharmacist speech
- Rasa CALM reasoning through compliance flows
- Automated ticket creation with incident ID TCK-7508
- Cross-shift memory recall on session resume
- Rime TTS providing natural voice responses

<a id="-quickstart"></a>

## 🚀 Quickstart

Run RxTwin locally with voice interaction:

```bash
cd starter
cp .env.example .env      # Add your API keys (Rasa, Nebius, Speechmatics, Rime)
make install
make verify               # Pre-flight check
make train
```

**Start the system (3 terminals):**

```bash
# Terminal 1: Action server
make run-actions

# Terminal 2: Rasa server
make run-rasa

# Terminal 3: Voice demo
make demo
```

**For text-only demo:**
```bash
make demo-text
```

**One-click PowerShell scripts (Windows):**
- `DEMO_START.ps1` — Start all servers + voice demo
- `DEMO_PRESENTATION.ps1` — Record presentation mode
- `DEMO_RECORDING.ps1` — Text-only with transcript

📖 **Full setup guide:** [`starter/README.md`](starter/README.md)

## 🧪 Testing

RxTwin includes end-to-end tests for pharmaceutical compliance flows.

**Test Results:**
```
Accuracy By Assertion Type
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Assertion Type  ┃ Accuracy ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│  flow_started   │ 100.00%  │
│ action_executed │ 100.00%  │
│   bot_uttered   │ 100.00%  │
└─────────────────┴──────────┘
0 failed, 1 passed
```

**Run E2E Tests:**
```bash
cd starter
.venv\Scripts\Activate.ps1
$env:RASA_PRO_BETA_STUB_CUSTOM_ACTION="true"
rasa test e2e tests/e2e
```

The test covers the core compliance ticket logging flow with temperature excursion scenarios.

<hr/>

## 🏆 Hackathon Alignment

RxTwin addresses the **Most Creative Enterprise Use Case** prize by:

- ✅ Solving a genuine pharmaceutical compliance problem
- ✅ Implementing persistent memory across sessions
- ✅ Using deterministic flows to prevent hallucination
- ✅ Providing voice-first interaction for hands-free operation
- ✅ Built entirely on the Rasa CALM framework

**Key capabilities for judging:**
- **🧠 Persistence** — Remembers incidents across shift changes
- **🛡️ Resilience** — Deterministic flows prevent hallucination
- **🏢 Real workflow fit** — Designed for actual pharmacy operations
- **⚙️ Rasa-native** — Built on Rasa CALM with custom flows

<hr/>

## 📦 Project Structure

```
README.md                    ← Project overview and documentation
starter/                     ← Main application code
  ├─ actions/                ← Custom actions for compliance workflows
  ├─ data/flows/             ← Rasa CALM flows (log_ticket, greet_resume, resolve)
  ├─ domain/                  ← Slots, responses, and domain configuration
  ├─ voice/                   ← Speechmatics ASR + Rime TTS integration
  ├─ agentic/                ← Optional: ReAct sub-agent + MCP tools
  └─ .data/tickets.json      ← Persistent ticket storage
```

## 🤝 Contributing

This is a hackathon project. For questions or collaboration:
- **GitHub:** https://github.com/DivyaPrakash04/MyTwinAgent-rasa-bos-hackathon-2026
- **Team:** RXtwin

## 📄 License

See LICENSE file for details.

---

<div align="center">

**Built for Boston Tech Week 2026 · Team RXtwin**

<a href="#"><img src="https://img.shields.io/badge/⬆-Back_to_top-475569?style=for-the-badge" alt="Back to top"/></a>

</div>