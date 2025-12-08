"""Factory for creating transcription services."""

from typing import Optional
import logging

from .base import BaseTranscriber
from .whisper import WhisperTranscriber
from .assemblyai import AssemblyAITranscriber

logger = logging.getLogger(__name__)


def get_transcriber(
    service: str = "whisper",
    openai_api_key: Optional[str] = None,
    assemblyai_api_key: Optional[str] = None,
    language: str = "nl",
    speaker_labels: bool = True
) -> BaseTranscriber:
    """
    Factory function to create appropriate transcriber.

    Args:
        service: 'whisper' or 'assemblyai'
        openai_api_key: API key for OpenAI Whisper
        assemblyai_api_key: API key for AssemblyAI
        language: Language code (e.g., 'nl' for Dutch)
        speaker_labels: Enable speaker diarization (AssemblyAI only)

    Returns:
        Configured transcriber instance
    """
    service = service.lower()

    if service == "whisper":
        if not openai_api_key:
            raise ValueError("OpenAI API key required for Whisper transcription")

        logger.info("Using OpenAI Whisper for transcription")
        return WhisperTranscriber(
            api_key=openai_api_key,
            language=language if language != "auto" else None
        )

    elif service == "assemblyai":
        if not assemblyai_api_key:
            raise ValueError("AssemblyAI API key required for AssemblyAI transcription")

        logger.info("Using AssemblyAI for transcription (with speaker diarization)")
        return AssemblyAITranscriber(
            api_key=assemblyai_api_key,
            language_code=language,
            speaker_labels=speaker_labels
        )

    else:
        raise ValueError(f"Unknown transcription service: {service}. Use 'whisper' or 'assemblyai'")


def estimate_transcription_cost(
    duration_seconds: float,
    service: str = "whisper"
) -> float:
    """
    Estimate transcription cost without creating a service.

    Args:
        duration_seconds: Audio duration in seconds
        service: 'whisper' or 'assemblyai'

    Returns:
        Estimated cost in USD
    """
    if service.lower() == "whisper":
        # $0.006 per minute
        return (duration_seconds / 60) * 0.006
    elif service.lower() == "assemblyai":
        # $0.37 per hour
        return (duration_seconds / 3600) * 0.37
    else:
        raise ValueError(f"Unknown service: {service}")
