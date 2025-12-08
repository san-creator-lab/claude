"""OpenAI Whisper transcription service."""

import logging
import time
from pathlib import Path
from typing import Optional

from openai import OpenAI

from .base import BaseTranscriber, TranscriptionResult, TranscriptionSegment

logger = logging.getLogger(__name__)


class WhisperTranscriber(BaseTranscriber):
    """Transcribe audio using OpenAI Whisper API."""

    # Whisper pricing: $0.006 per minute
    COST_PER_MINUTE = 0.006
    MAX_FILE_SIZE_MB = 25

    def __init__(
        self,
        api_key: str,
        model: str = "whisper-1",
        language: Optional[str] = None  # None for auto-detect
    ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.language = language

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """
        Transcribe audio file using Whisper API.

        Args:
            audio_path: Path to audio file (mp3, mp4, mpeg, mpga, m4a, wav, webm)

        Returns:
            TranscriptionResult with transcript
        """
        if not audio_path.exists():
            return TranscriptionResult(
                success=False,
                error=f"Audio file not found: {audio_path}",
                service="whisper"
            )

        # Check file size
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            logger.warning(f"File size {file_size_mb:.1f}MB exceeds limit. Consider chunking.")

        logger.info(f"Transcribing with Whisper: {audio_path}")
        start_time = time.time()

        try:
            with open(audio_path, "rb") as audio_file:
                # Use verbose_json to get timestamps
                response = self.client.audio.transcriptions.create(
                    model=self.model,
                    file=audio_file,
                    response_format="verbose_json",
                    language=self.language,
                    timestamp_granularities=["segment"]
                )

            duration = time.time() - start_time
            logger.info(f"Transcription completed in {duration:.1f}s")

            # Parse response
            full_text = response.text
            segments = []

            # Parse segments if available
            if hasattr(response, 'segments') and response.segments:
                for seg in response.segments:
                    segments.append(TranscriptionSegment(
                        start_time_ms=int(seg.get('start', 0) * 1000),
                        end_time_ms=int(seg.get('end', 0) * 1000),
                        text=seg.get('text', '').strip(),
                        confidence=seg.get('avg_logprob')
                    ))

            # Calculate cost based on audio duration
            audio_duration = response.duration if hasattr(response, 'duration') else 0
            cost = self.estimate_cost(audio_duration)

            return TranscriptionResult(
                success=True,
                full_text=full_text,
                segments=segments,
                language_detected=response.language if hasattr(response, 'language') else self.language,
                audio_duration_seconds=audio_duration,
                cost_usd=cost,
                service="whisper"
            )

        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            return TranscriptionResult(
                success=False,
                error=str(e),
                service="whisper"
            )

    def estimate_cost(self, duration_seconds: float) -> float:
        """Estimate cost for transcribing given duration."""
        minutes = duration_seconds / 60
        return minutes * self.COST_PER_MINUTE

    def transcribe_with_chunks(
        self,
        audio_path: Path,
        chunk_duration_minutes: int = 20
    ) -> TranscriptionResult:
        """
        Transcribe large audio files by chunking.

        Note: Requires pydub and ffmpeg for audio processing.
        """
        try:
            from pydub import AudioSegment
        except ImportError:
            logger.warning("pydub not installed. Using single-file transcription.")
            return self.transcribe(audio_path)

        logger.info(f"Loading audio for chunking: {audio_path}")
        audio = AudioSegment.from_file(str(audio_path))
        duration_ms = len(audio)
        chunk_ms = chunk_duration_minutes * 60 * 1000

        if duration_ms <= chunk_ms:
            return self.transcribe(audio_path)

        logger.info(f"Splitting {duration_ms/1000/60:.1f} min audio into chunks")

        all_segments = []
        all_text = []
        total_cost = 0
        offset_ms = 0

        chunk_index = 0
        while offset_ms < duration_ms:
            chunk_end = min(offset_ms + chunk_ms, duration_ms)
            chunk = audio[offset_ms:chunk_end]

            # Export chunk to temp file
            chunk_path = audio_path.with_suffix(f'.chunk{chunk_index}.mp3')
            chunk.export(str(chunk_path), format="mp3")

            try:
                result = self.transcribe(chunk_path)

                if result.success:
                    all_text.append(result.full_text)
                    total_cost += result.cost_usd

                    # Adjust segment timestamps
                    for seg in result.segments:
                        seg.start_time_ms += offset_ms
                        seg.end_time_ms += offset_ms
                        all_segments.append(seg)
            finally:
                # Clean up chunk file
                chunk_path.unlink(missing_ok=True)

            offset_ms = chunk_end
            chunk_index += 1

        return TranscriptionResult(
            success=True,
            full_text=" ".join(all_text),
            segments=all_segments,
            audio_duration_seconds=duration_ms / 1000,
            cost_usd=total_cost,
            service="whisper"
        )
