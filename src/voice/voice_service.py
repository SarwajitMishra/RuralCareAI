"""
voice_service.py

Speech-to-text using Faster-Whisper.

Author:
Sarwajit Kumar Mishra
"""

from __future__ import annotations

from faster_whisper import WhisperModel


class VoiceService:

    _model = None

    def __init__(self):

        if VoiceService._model is None:

            VoiceService._model = WhisperModel(
                "base",
                device="cpu",
                compute_type="int8",
            )

    # --------------------------------------------

    def transcribe(self, audio_path: str):

        segments, info = VoiceService._model.transcribe(
            audio_path,
            beam_size=5,
        )

        text = ""

        for segment in segments:

            text += segment.text + " "

        return {

            "language": info.language,

            "transcript": text.strip(),

        }