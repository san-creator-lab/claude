"""AssemblyAI transcription service with speaker diarization."""

import logging
import time
from pathlib import Path
from typing import Optional

import assemblyai as aai

from .base import BaseTranscriber, TranscriptionResult, TranscriptionSegment, SpeakerInfo

logger = logging.getLogger(__name__)


class AssemblyAITranscriber(BaseTranscriber):
    """
    Transcribe audio using AssemblyAI API.

    Benefits over Whisper:
    - Better speaker diarization
    - Automatic punctuation and formatting
    - Entity detection
    - Content moderation
    """

    # AssemblyAI pricing (standard tier): $0.37 per hour
    COST_PER_HOUR = 0.37

    def __init__(
        self,
        api_key: str,
        language_code: str = "nl",  # Dutch
        speaker_labels: bool = True,
        auto_chapters: bool = False,
        entity_detection: bool = False
    ):
        aai.settings.api_key = api_key
        self.language_code = language_code
        self.speaker_labels = speaker_labels
        self.auto_chapters = auto_chapters
        self.entity_detection = entity_detection

    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """
        Transcribe audio file using AssemblyAI API.

        Args:
            audio_path: Path to audio file

        Returns:
            TranscriptionResult with transcript and speaker information
        """
        if not audio_path.exists():
            return TranscriptionResult(
                success=False,
                error=f"Audio file not found: {audio_path}",
                service="assemblyai"
            )

        logger.info(f"Transcribing with AssemblyAI: {audio_path}")
        start_time = time.time()

        try:
            # Configure transcription
            config = aai.TranscriptionConfig(
                language_code=self.language_code,
                speaker_labels=self.speaker_labels,
                auto_chapters=self.auto_chapters,
                entity_detection=self.entity_detection,
                punctuate=True,
                format_text=True
            )

            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(str(audio_path), config=config)

            duration = time.time() - start_time
            logger.info(f"Transcription completed in {duration:.1f}s")

            if transcript.status == aai.TranscriptStatus.error:
                return TranscriptionResult(
                    success=False,
                    error=transcript.error,
                    service="assemblyai"
                )

            # Parse segments with speaker labels
            segments = []
            if transcript.utterances:
                for utt in transcript.utterances:
                    segments.append(TranscriptionSegment(
                        start_time_ms=utt.start,
                        end_time_ms=utt.end,
                        text=utt.text,
                        speaker=utt.speaker,
                        confidence=utt.confidence
                    ))
            elif transcript.words:
                # Fall back to word-level if no utterances
                current_text = []
                current_start = 0
                current_speaker = None

                for word in transcript.words:
                    if not current_text:
                        current_start = word.start
                        current_speaker = getattr(word, 'speaker', None)

                    # Check if speaker changed or sentence ended
                    speaker_changed = (
                        hasattr(word, 'speaker') and
                        word.speaker != current_speaker
                    )

                    if speaker_changed and current_text:
                        # Save current segment
                        segments.append(TranscriptionSegment(
                            start_time_ms=current_start,
                            end_time_ms=word.start,
                            text=" ".join(current_text),
                            speaker=current_speaker,
                            confidence=word.confidence
                        ))
                        current_text = []
                        current_start = word.start
                        current_speaker = word.speaker

                    current_text.append(word.text)

                # Don't forget last segment
                if current_text:
                    segments.append(TranscriptionSegment(
                        start_time_ms=current_start,
                        end_time_ms=transcript.words[-1].end if transcript.words else current_start,
                        text=" ".join(current_text),
                        speaker=current_speaker
                    ))

            # Calculate speaker statistics
            speakers = self._calculate_speaker_stats(segments)

            # Get audio duration and cost
            audio_duration = (transcript.audio_duration or 0)
            cost = self.estimate_cost(audio_duration)

            # Calculate confidence
            avg_confidence = None
            if transcript.confidence:
                avg_confidence = transcript.confidence

            return TranscriptionResult(
                success=True,
                full_text=transcript.text or "",
                segments=segments,
                speakers=speakers,
                language_detected=self.language_code,
                confidence_score=avg_confidence,
                audio_duration_seconds=audio_duration,
                cost_usd=cost,
                service="assemblyai"
            )

        except Exception as e:
            logger.error(f"AssemblyAI transcription failed: {e}")
            return TranscriptionResult(
                success=False,
                error=str(e),
                service="assemblyai"
            )

    def estimate_cost(self, duration_seconds: float) -> float:
        """Estimate cost for transcribing given duration."""
        hours = duration_seconds / 3600
        return hours * self.COST_PER_HOUR

    def identify_speakers(
        self,
        transcript_result: TranscriptionResult,
        known_speakers: Optional[dict[str, str]] = None
    ) -> TranscriptionResult:
        """
        Try to identify speakers based on known speaker patterns.

        Args:
            transcript_result: Transcription with speaker labels
            known_speakers: Map of speaker labels to names, e.g. {"A": "Alexander Klöpping"}

        Returns:
            Updated TranscriptionResult with speaker names
        """
        if not known_speakers:
            # Default speaker mapping for AI Report podcast
            known_speakers = {
                "A": "Alexander Klöpping",
                "B": "Wietse Hage"
            }

        # Update segments with known names
        for segment in transcript_result.segments:
            if segment.speaker and segment.speaker in known_speakers:
                segment.speaker = known_speakers[segment.speaker]

        # Update speaker info
        for speaker in transcript_result.speakers:
            if speaker.label in known_speakers:
                speaker.display_name = known_speakers[speaker.label]

        return transcript_result
