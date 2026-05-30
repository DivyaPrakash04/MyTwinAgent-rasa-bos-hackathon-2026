# 📄 **INSTRUCTIONS.md — MyTwinAgent (RxTwin) Hackathon Edition**  
*A complete prompt chain + business value + clinical workflows + voice demo script*

---

# # 🎯 Project Overview  
**MyTwinAgent (RxTwin) — A Persistent Voice Coworker for Clinical Operations**  
A continuously running, voice-enabled assistant built on **Rasa CALM**, designed as a hands-free operational clone (a digital "twin") for pharmacists and clinical technicians. 

RxTwin handles:
- **Hands-Free Intake**: Logging critical compliance exceptions and stock drops entirely by voice.
- **SOP Action Guidance**: Automatically looking up clinical Standard Operating Procedures (SOPs) via MCP.
- **Cross-Shift Persistence**: Recognizing pharmacists across restarts/shift changes and resuming pending incidents.
- **Interruption Resilience**: Gracefully recovering from voice pauses, distractions, and restarts in high-stress pharmacy cleanrooms.

---

# # 🧠 Core Concept  
RxTwin is **not** a general-purpose assistant. It is a **voice-first operations twin** that handles regulatory constraints:
- **Deterministic Workflows**: Direct, safe, and hallucination-free compliance routing.
- **Cross-Session Memory**: Retaining tickets and active logs across system shutdowns and pharmacist shift handoffs.
- **Voice-First Design**: Short, speakable steps formatted specifically for a wireless earpiece in a sanitary lab.

This aligns perfectly with the hackathon judging criteria:
- **Most Creative Enterprise Use Case** — Clinical ops / pharmacy sterile environment.
- **Most Resilient Long-Term Agent** — True shift handoff memory persistence.
- **Best Voice Coworker** — Natural, low-latency earpiece triage.

---

# # 🧩 Architecture Summary  
The system operates as a seamless real-time voice pipeline:
- **Speechmatics ASR** ➔ Converts spoken pharmacist commands to text.
- **Rasa CALM Brain** ➔ Translates user intent into deterministic flows using a **Nebius Token Factory** Qwen LLM.
- **Custom Actions (Rasa SDK)** ➔ Logs compliance tickets to a persistent database (`tickets.json`) and handles cross-session greetings.
- **Level 2 ReAct Sub-Agent** ➔ Leverages **MCP (Model Context Protocol)** servers to search vaccine/controlled substance SOP databases.
- **Rime TTS** ➔ Synthesizes highly realistic spoken responses back to the pharmacist's headset.

---

# # 🔗 Prompt Chain (Agent Instructions)

System-level prompts configured in the Rasa LLM pipeline to enforce identity and constraints:

### 1. SYSTEM PROMPT — Agent Identity  
```
You are MyTwinAgent (RxTwin), an always-on digital coworker for pharmacy clinical operations.
Your purpose is to:
- Log clinical exceptions and temperature excursions.
- Retrieve regulatory standard operating procedures (SOPs) using MCP search tools.
- Maintain session memory across shift changes.
- Avoid hallucinations—never invent ticket numbers, temperatures, or drug protocols.
- Confirm critical compliance actions (like vaccine quarantine) before closing a ticket.
```

### 2. SYSTEM PROMPT — Voice Interaction Rules  
```
You are speaking to a pharmacist wearing a hands-free headset.
- Keep responses short, clear, and easy to understand when spoken.
- Never read markdown lists or verbose technical strings.
- Speak in a warm, professional, collaborative tone.
- Confirm active tasks when resuming a session.
```

---

# # 🏢 Business Value Narrative (For Judges)

### The Problem  
Pharmacists and clinical lab technicians work under extreme stress. They wear sterile gloves and handle delicate materials. They **cannot** touch a computer keyboard to document issues or query SOP guides without breaking sanitation protocols. Delayed reporting of critical exceptions (e.g. refrigerator temperature alarms) leads to vaccine spoilage worth thousands of dollars and severe compliance penalties.

### The Solution: RxTwin  
**MyTwinAgent (RxTwin)** stands by in the cloud as a hands-free clinical co-pilot. Technicians interact entirely by voice to:
*   Open urgent compliance tickets immediately.
*   Query complex regulatory standard operating procedures hands-free.
*   Retain and hand off incident context across staff shifts seamlessly.

### Business Impact  
- **90%+ faster incident logging** at the moment of discovery.
- **Zero vaccine wastage** through instant, step-by-step SOP temperature compliance.
- **100% auditable trail** logged automatically without manual typing.
- **Zero contamination risk** by eliminating keyboard contact in cleanrooms.

---

# # 🔄 Clinical Workflows (CALM Flows)

### 1. Log Compliance Exception
*   **Trigger**: Outages, refrigerator alarm alerts, stock damage (*"Fridge B temperature is dropping!"*).
*   **Steps**:
    1.  Confirm and identify the pharmacist's name.
    2.  Collect exception details (summary, priority, email).
    3.  Call `action_create_ticket` to save context permanently.
    4.  If the exception is clinical (temperature drop), trigger MCP search to retrieve SOP storage guidelines.
    5.  Deliver step-by-step guidance.

### 2. Shift Handoff & Session Resumption
*   **Trigger**: Pharmacist connects or re-establishes session after logging out.
*   **Steps**:
    1.  Execute `action_greet_twin` on boot.
    2.  If active tickets are found, prompt: *"Welcome back, Pharmacist {user_name}. I see we have an unresolved Fridge B temperature excursion (TCK-504). Did you finish quarantining the Shingrix vials?"*

---

# # 🧪 Live Voice Demo Script (60–90 seconds)

### **1. Shift Commencement (Session 1)**
*   **User**: *"Hey RxTwin, this is Pharmacist Divya."*
*   **RxTwin**: *"Hi Pharmacist Divya! Active and listening. How is the lab looking?"*

### **2. Reporting the Temperature Outage**
*   **User**: *"We have a problem. Refrigerator Fridge B just triggered a temperature alarm. It dropped to minus one Celsius."*
*   **RxTwin**: *"Oh no. I'll open an urgent compliance exception ticket for you immediately. [Database Call] ...Incident TCK-504 opened. Let me search our standard operating procedures... [Calls MCP Tool] ...Alright, SOP-501 states that Shingrix vaccines degrade when frozen. Step 1 is to immediately move all Shingrix vials to backup Fridge A. Should I log that task?"*

### **3. Simulating a Physical Interruption**
*   **User**: *"Yes, log it. But hold on, the courier just arrived with the control deliveries, I need to sign."*
*   **RxTwin**: *"No problem, Divya. I've logged the transfer task as in-progress. TCK-504 is held active. Let me know when you're back."*

*(The user terminates the terminal session. The judges see the system shutdown. The database holds the state).*

### **4. Shift Resume (Session 2 - Cross-Session Persistence)**
*(The user restarts the terminal demo to simulate returning after a break).*
*   **User**: *"Hey RxTwin."*
*   **RxTwin**: *"Welcome back, Pharmacist Divya! I see ticket TCK-504 for the Fridge B temperature drop is still open. Did we successfully complete the transfer of the Shingrix vials to Fridge A?"*
*   **User**: *"Yes, they are safely in Fridge A."*
*   **RxTwin**: *"Perfect. I've updated the log. I will now flag Fridge B as out-of-service and notify maintenance. Anything else I can do for you in the cleanroom?"*
*   **User**: *"That's all, thanks."*
*   **RxTwin**: *"Have a safe shift. I'll be right here."*