"""Sanitize Rasa replies before display and TTS in demo/presentation mode."""

from __future__ import annotations

import re

_META_MARKERS = (
    "**Here's why",
    "Here's why this works",
    "Here are a few options",
    "rephrasing",
    "**Option 1",
    "**Option 2",
    "I think **Option",
    "Sorry, I am having trouble",
)

RIME_MAX_CHARS = 450

_JUNK_PHRASES = (
    "updating issue_",
    "set slot",
    "respectively",
    "i am afraid, i don't know",
    "not trained to help",
    "don't have access to a knowledge base",
)

# Generic wrap-up lines — never prefer these over substantive replies.
_LOW_VALUE_PHRASES = (
    "anything else i can help",
    "would you like to continue",
)

# Prefer replies that contain these (most specific first).
_PRIORITY_PHRASES = (
    "done — i've logged",
    "marked incident",
    "perfect.",
    "welcome back",
    "sensors are green",
    "thanks for working with me",
    "incident tck-",
)


def _is_low_value(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in _LOW_VALUE_PHRASES)


def pick_coworker_reply(texts: list[str]) -> str:
    """Prefer substantive bot lines over generic wrap-up prompts."""
    if not texts:
        return ""
    if len(texts) == 1:
        return texts[0]

    substantive = [
        t for t in texts
        if not _is_low_value(t) and not any(j in t.lower() for j in _JUNK_PHRASES)
    ]
    pool = substantive or list(texts)

    for phrase in _PRIORITY_PHRASES:
        for t in reversed(pool):
            if phrase in t.lower():
                return t

    for t in reversed(pool):
        lower = t.lower()
        if lower.startswith("incident tck-") and "opened" in lower and len(t) < 45:
            continue
        if "?" in t and not _is_low_value(t):
            return t
        if lower.startswith("hi ") or lower.startswith("hey"):
            return t

    for t in reversed(pool):
        if not _is_low_value(t):
            return t
    return texts[-1]


def sanitize_for_speech(text: str, *, max_chars: int = RIME_MAX_CHARS) -> str:
    """Return a short, speakable line — no markdown or LLM meta-commentary."""
    if not text or not text.strip():
        return text

    cleaned = text.strip()
    for marker in _META_MARKERS:
        idx = cleaned.find(marker)
        if idx > 0:
            cleaned = cleaned[:idx]

    cleaned = re.sub(r"\*+", "", cleaned)
    cleaned = re.sub(r"#+\s*", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    spoken = " ".join(sentences[:2]).strip() or cleaned

    if len(spoken) > max_chars:
        spoken = spoken[: max_chars - 3].rsplit(" ", 1)[0] + "..."
    return spoken
