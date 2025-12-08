"""Base classes for transcription."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class TranscriptionSegment:
    """A segment of transcribed text with timing."""
    start_time_ms: int
    end_time_ms: int
    text: str
    speaker: Optional[str] = None
    confidence: Optional[float] = None

    @property
    def start_seconds(self) -> float:
        return self.start_time_ms / 1000

    @property
    def end_seconds(self) -> float:
        return self.end_time_ms / 1000

    @property
    def duration_seconds(self) -> float:
        return (self.end_time_ms - self.start_time_ms) / 1000

    def to_srt_timestamp(self, ms: int) -> str:
        """Convert milliseconds to SRT timestamp format."""
        hours = ms // 3600000
        minutes = (ms % 3600000) // 60000
        seconds = (ms % 60000) // 1000
        millis = ms % 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"

    def to_srt_entry(self, index: int) -> str:
        """Convert to SRT subtitle entry."""
        return f"""{index}
{self.to_srt_timestamp(self.start_time_ms)} --> {self.to_srt_timestamp(self.end_time_ms)}
{self.text}

"""


@dataclass
class SpeakerInfo:
    """Information about a speaker."""
    label: str
    display_name: Optional[str] = None
    speaking_time_ms: int = 0
    word_count: int = 0


@dataclass
class TranscriptionResult:
    """Result of transcription."""
    success: bool
    full_text: str = ""
    segments: list[TranscriptionSegment] = field(default_factory=list)
    speakers: list[SpeakerInfo] = field(default_factory=list)
    language_detected: Optional[str] = None
    confidence_score: Optional[float] = None
    audio_duration_seconds: float = 0
    cost_usd: float = 0
    service: str = ""
    error: Optional[str] = None

    @property
    def word_count(self) -> int:
        return len(self.full_text.split())

    def to_plain_text(self) -> str:
        """Get plain text transcript."""
        return self.full_text

    def to_text_with_timestamps(self) -> str:
        """Get transcript with timestamps."""
        lines = []
        for seg in self.segments:
            timestamp = f"[{seg.start_seconds:.1f}s]"
            speaker = f"{seg.speaker}: " if seg.speaker else ""
            lines.append(f"{timestamp} {speaker}{seg.text}")
        return "\n".join(lines)

    def to_srt(self) -> str:
        """Convert to SRT subtitle format."""
        entries = []
        for i, seg in enumerate(self.segments, 1):
            entries.append(seg.to_srt_entry(i))
        return "".join(entries)

    def to_vtt(self) -> str:
        """Convert to WebVTT subtitle format."""
        lines = ["WEBVTT", ""]
        for seg in self.segments:
            start = seg.to_srt_timestamp(seg.start_time_ms).replace(',', '.')
            end = seg.to_srt_timestamp(seg.end_time_ms).replace(',', '.')
            speaker = f"<v {seg.speaker}>" if seg.speaker else ""
            lines.append(f"{start} --> {end}")
            lines.append(f"{speaker}{seg.text}")
            lines.append("")
        return "\n".join(lines)


class BaseTranscriber(ABC):
    """Abstract base class for transcription services."""

    @abstractmethod
    def transcribe(self, audio_path: Path) -> TranscriptionResult:
        """
        Transcribe audio file.

        Args:
            audio_path: Path to audio file

        Returns:
            TranscriptionResult with transcript and metadata
        """
        pass

    @abstractmethod
    def estimate_cost(self, duration_seconds: float) -> float:
        """Estimate cost for transcribing given duration."""
        pass

    def _calculate_speaker_stats(
        self, segments: list[TranscriptionSegment]
    ) -> list[SpeakerInfo]:
        """Calculate statistics for each speaker."""
        speaker_data: dict[str, SpeakerInfo] = {}

        for seg in segments:
            if seg.speaker:
                if seg.speaker not in speaker_data:
                    speaker_data[seg.speaker] = SpeakerInfo(label=seg.speaker)

                speaker_data[seg.speaker].speaking_time_ms += (
                    seg.end_time_ms - seg.start_time_ms
                )
                speaker_data[seg.speaker].word_count += len(seg.text.split())

        return list(speaker_data.values())
