"""Audio playback helper. Plays WAV bytes; degrades gracefully if audio libs/ffmpeg
are not available (so the demo still runs in --text mode anywhere)."""

from __future__ import annotations

import io
import logging

logger = logging.getLogger(__name__)


def play_wav_bytes(audio: bytes) -> None:
    try:
        from pydub import AudioSegment
        from pydub.playback import play

        play(AudioSegment.from_file(io.BytesIO(audio), format="wav"))
    except Exception as exc:  # noqa: BLE001
        msg = (
            f"Audio playback failed ({exc}). "
            "Install ffmpeg and add it to PATH, then re-run. "
            "See RECORDING.md for details."
        )
        logger.warning(msg)
        print(f"\n[WARNING] {msg}\n", flush=True)
