"""Live command-line runner for the Always-On AI Coworker.

Watch the conversation unfold in real time:

    user audio --> [Speechmatics ASR] --> text
              --> [Rasa CALM + Nebius] --> reply
              --> [Rime TTS]           --> spoken reply

Rasa is the brain; the client just calls its REST API. Spinners show each stage
(listening / transcribing / thinking / speaking) and colored panels show the
transcript as it streams.

Usage:
    python -m voice.demo                    # full voice loop (run `make generate-audio` first)
    python -m voice.demo --tts speechmatics # use a Speechmatics voice for the agent reply
    python -m voice.demo --text             # no audio: type to the coworker live
    python -m voice.demo --text --auto      # scripted run, no audio (screen text only)
    python -m voice.demo --presentation     # full 2-act story WITH spoken audio (default)
    python -m voice.demo --text --presentation  # same story, text only (no TTS)
"""

from __future__ import annotations

import argparse
import asyncio
import uuid
from datetime import datetime, timezone
from pathlib import Path

import aiohttp
from dotenv import load_dotenv
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from voice.audio_io import play_wav_bytes
from voice.script import PRESENTATION_ACTS, USER_TURNS
from voice.speechmatics_service import SpeechmaticsService
from voice.speech_util import pick_coworker_reply, sanitize_for_speech

load_dotenv()

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"
AUDIO_DIR = Path("voice/audio")
console = Console()


def banner() -> None:
    console.print(
        Panel(
            Text("Always-On AI Coworker  —  live demo\n", style="bold white", justify="center")
            + Text("Speechmatics (ears)  ·  Rasa CALM + Nebius (brain)  ·  Rime (voice)",
                   style="dim", justify="center"),
            border_style="magenta", box=box.DOUBLE, padding=(0, 2),
        )
    )


def bubble(speaker: str, text: str, *, who: str) -> None:
    style = {"user": "cyan", "coworker": "green", "system": "yellow"}[who]
    title = {"user": "\U0001F464  You", "coworker": "\U0001F916  Coworker",
             "system": "\u2139  System"}[who]
    console.print(
        Panel(Text(text or "(silence)", style="white"),
              title=f"[bold]{title}[/bold]", border_style=style,
              box=box.ROUNDED, padding=(0, 2)),
        justify="left" if who == "user" else "right",
    )


async def send_to_rasa(
    session: aiohttp.ClientSession,
    sender: str,
    text: str,
    *,
    single_reply: bool = False,
) -> str:
    async with session.post(
        RASA_URL, json={"sender": sender, "message": text},
        timeout=aiohttp.ClientTimeout(total=90),
    ) as resp:
        resp.raise_for_status()
        msgs = await resp.json()
    texts = [m["text"] for m in msgs if m.get("text")]
    if not texts:
        return ""
    if single_reply:
        return pick_coworker_reply(texts)
    return "  ".join(texts)


async def restart_rasa_session(session: aiohttp.ClientSession, sender: str) -> None:
    """Clear in-memory tracker so the next act starts fresh."""
    async with session.post(
        RASA_URL, json={"sender": sender, "message": "/restart"},
        timeout=aiohttp.ClientTimeout(total=30),
    ) as resp:
        resp.raise_for_status()


def prepare_presentation_demo() -> None:
    from actions.tickets import reset_demo_tickets

    reset_demo_tickets()
    console.print(
        "[dim]Cleared .data/tickets.json — Act 1 starts on a clean shift.[/dim]\n"
    )


def save_transcript(path: Path, lines: list[tuple[str, str]], *, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body = [f"# {title}", "", f"*Recorded {stamp}*", ""]
    for who, text in lines:
        label = "Pharmacist" if who == "user" else "RxTwin"
        body.append(f"**{label}:** {text}")
        body.append("")
    path.write_text("\n".join(body), encoding="utf-8")


async def run_turns(
    session: aiohttp.ClientSession,
    sender: str,
    turns: list[str],
    *,
    pause: float,
    transcript: list[tuple[str, str]],
) -> None:
    for turn in turns:
        bubble("You", turn, who="user")
        transcript.append(("user", turn))
        await asyncio.sleep(min(pause, 1.0))
        with console.status("[green]Thinking (Rasa + Nebius)…", spinner="dots"):
            reply = await send_to_rasa(session, sender, turn, single_reply=True)
        reply = sanitize_for_speech(reply)
        bubble("Coworker", reply, who="coworker")
        transcript.append(("coworker", reply))
        if pause > 0:
            await asyncio.sleep(pause)


async def run_text_auto(
    *,
    turns: list[str],
    pause: float,
    transcript_path: Path | None,
    acts: list[dict] | None = None,
) -> None:
    prepare_presentation_demo()
    banner()
    console.print(
        Panel(
            Text("Presentation mode — scripted demo\n", style="bold white", justify="center")
            + Text("Start screen recording now (Win+G or OBS), then watch the story unfold.",
                   style="dim", justify="center"),
            border_style="yellow", box=box.DOUBLE, padding=(0, 2),
        )
    )
    transcript: list[tuple[str, str]] = []
    sender = f"demo-{uuid.uuid4().hex[:8]}"
    async with aiohttp.ClientSession() as session:
        if acts:
            for i, act in enumerate(acts):
                if i > 0:
                    console.print(
                        Panel(
                            Text(act["title"], style="bold white", justify="center"),
                            border_style="magenta", box=box.ROUNDED,
                        )
                    )
                if act.get("new_session"):
                    sender = f"demo-{uuid.uuid4().hex[:8]}"
                    await restart_rasa_session(session, sender)
                    console.print("[dim]— new session (simulated shift return) —[/dim]\n")
                await run_turns(
                    session, sender, act["turns"],
                    pause=pause, transcript=transcript,
                )
        else:
            await run_turns(
                session, sender, turns,
                pause=pause, transcript=transcript,
            )

    console.print(
        Panel(
            Text("Demo complete. Share the transcript file or your screen recording.",
                 style="white"),
            border_style="green", box=box.ROUNDED,
        )
    )
    if transcript_path:
        save_transcript(transcript_path, transcript, title="MyTwinAgent (RxTwin) Demo")
        console.print(f"[green]Transcript saved:[/green] {transcript_path}")


async def run_presentation_voice(
    agent_tts: str,
    *,
    pause: float,
    transcript_path: Path | None,
) -> None:
    prepare_presentation_demo()
    banner()
    console.print(
        Panel(
            Text("Presentation mode — spoken demo\n", style="bold white", justify="center")
            + Text("Pharmacist + RxTwin voices play through your speakers. "
                   "Record with Win+G or OBS and enable system audio.",
                   style="dim", justify="center"),
            border_style="yellow", box=box.DOUBLE, padding=(0, 2),
        )
    )

    asr = SpeechmaticsService()
    if agent_tts == "rime":
        from voice.rime_service import RimeTTS
        rime = RimeTTS()
        speak = rime.synthesize
        voice_label = "Rime"
    else:
        async def speak(text: str) -> bytes:  # type: ignore[misc]
            return await asr.synthesize(text, role="agent")
        voice_label = "Speechmatics"

    transcript: list[tuple[str, str]] = []
    sender = f"demo-{uuid.uuid4().hex[:8]}"
    clip_index = 0

    async with aiohttp.ClientSession() as session:
        for i, act in enumerate(PRESENTATION_ACTS):
            if i > 0:
                console.print(
                    Panel(
                        Text(act["title"], style="bold white", justify="center"),
                        border_style="magenta", box=box.ROUNDED,
                    )
                )
            if act.get("new_session"):
                sender = f"demo-{uuid.uuid4().hex[:8]}"
                await restart_rasa_session(session, sender)
                console.print("[dim]— new session (simulated shift return) —[/dim]\n")

            for turn in act["turns"]:
                clip_index += 1
                clip_path = AUDIO_DIR / f"user_{clip_index}.wav"
                if clip_path.exists():
                    user_audio = clip_path.read_bytes()
                else:
                    with console.status("[cyan]Synthesizing pharmacist voice…", spinner="earth"):
                        user_audio = await asr.synthesize(turn, role="user")

                with console.status(f"[cyan]Pharmacist speaking… (user_{clip_index}.wav)", spinner="dots"):
                    play_wav_bytes(user_audio)
                bubble("You", turn, who="user")
                transcript.append(("user", turn))

                with console.status("[green]Thinking (Rasa + Nebius)…", spinner="dots"):
                    reply = await send_to_rasa(session, sender, turn, single_reply=True)
                reply = sanitize_for_speech(reply)
                bubble("Coworker", reply, who="coworker")
                transcript.append(("coworker", reply))

                if reply:
                    with console.status(f"[green]RxTwin speaking ({voice_label})…", spinner="dots"):
                        try:
                            spoken = await speak(reply)
                        except Exception as exc:
                            console.print(f"[yellow]TTS skipped: {exc}[/yellow]")
                        else:
                            play_wav_bytes(spoken)

                if pause > 0:
                    await asyncio.sleep(pause)

    console.print(
        Panel(
            Text("Demo complete. Share your screen recording and the transcript file.",
                 style="white"),
            border_style="green", box=box.ROUNDED,
        )
    )
    if transcript_path:
        save_transcript(transcript_path, transcript, title="MyTwinAgent (RxTwin) Demo")
        console.print(f"[green]Transcript saved:[/green] {transcript_path}")


async def run_text() -> None:
    banner()
    console.print("[dim]Text mode. Type a message (or 'quit'). "
                  'Try: "I need to open a support ticket."[/dim]\n')
    sender = f"demo-{uuid.uuid4().hex[:8]}"
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                text = console.input("[bold cyan]you ›[/bold cyan] ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if text.lower() in {"quit", "exit"}:
                break
            if not text:
                continue
            with console.status("[green]Thinking (Rasa + Nebius)…", spinner="dots"):
                reply = await send_to_rasa(session, sender, text)
            bubble("Coworker", reply, who="coworker")
    console.print("\n[dim]Bye. Tickets persisted to .data/tickets.json.[/dim]")


async def run_voice(agent_tts: str) -> None:
    banner()
    sender = f"demo-{uuid.uuid4().hex[:8]}"
    asr = SpeechmaticsService()

    if agent_tts == "rime":
        from voice.rime_service import RimeTTS
        rime = RimeTTS()
        speak = rime.synthesize
        voice_label = "Rime"
    else:
        async def speak(text: str) -> bytes:  # type: ignore[misc]
            return await asr.synthesize(text, role="agent")
        voice_label = "Speechmatics"

    clips = [AUDIO_DIR / f"user_{i}.wav" for i in range(1, len(USER_TURNS) + 1)]
    missing = [c.name for c in clips if not c.exists()]
    if missing:
        console.print(f"[red]Missing audio: {', '.join(missing)}. "
                      f"Run: make generate-audio[/red]")
        raise SystemExit(1)

    async with aiohttp.ClientSession() as session:
        for clip in clips:
            audio = clip.read_bytes()
            with console.status(f"[cyan]Listening… ({clip.name})", spinner="dots"):
                play_wav_bytes(audio)
            with console.status("[cyan]Transcribing (Speechmatics)…", spinner="earth"):
                transcript = await asr.transcribe(audio) or ""
            bubble("You", transcript, who="user")

            with console.status("[green]Thinking (Rasa + Nebius)…", spinner="dots"):
                reply = await send_to_rasa(session, sender, transcript)
            bubble("Coworker", reply, who="coworker")

            if reply:
                with console.status(f"[green]Speaking ({voice_label})…", spinner="dots"):
                    spoken = await speak(reply)
                play_wav_bytes(spoken)

    console.print(
        Panel(
            Text("Demo complete. Tickets were saved to .data/tickets.json — restart and ask "
                 "for the ticket status to watch the coworker remember across sessions.",
                 style="white"),
            border_style="green", box=box.ROUNDED,
        )
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="Live runner for the Rasa AI coworker.")
    ap.add_argument("--text", action="store_true", help="No audio; type messages live.")
    ap.add_argument("--auto", action="store_true",
                    help="Play USER_TURNS automatically (use with --text).")
    ap.add_argument("--presentation", action="store_true",
                    help="Full 2-act pharmacy story (spoken by default; add --text for silent).")
    ap.add_argument("--pause", type=float, default=3.0,
                    help="Seconds between turns in auto/presentation mode (default: 3).")
    ap.add_argument("--transcript", type=Path, metavar="FILE",
                    help="Save a shareable Markdown transcript to this path.")
    ap.add_argument("--tts", choices=["rime", "speechmatics"], default="rime",
                    help="Engine for the agent's voice (default: rime).")
    args = ap.parse_args()
    try:
        if args.presentation:
            if args.text:
                asyncio.run(run_text_auto(
                    turns=USER_TURNS,
                    pause=args.pause,
                    transcript_path=args.transcript,
                    acts=PRESENTATION_ACTS,
                ))
            else:
                asyncio.run(run_presentation_voice(
                    args.tts,
                    pause=args.pause,
                    transcript_path=args.transcript,
                ))
        elif args.auto:
            if not args.text:
                console.print("[red]--auto requires --text.[/red]")
                raise SystemExit(1)
            asyncio.run(run_text_auto(
                turns=USER_TURNS,
                pause=args.pause,
                transcript_path=args.transcript,
                acts=None,
            ))
        elif args.text:
            asyncio.run(run_text())
        else:
            asyncio.run(run_voice(args.tts))
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted.[/yellow]")


if __name__ == "__main__":
    main()
