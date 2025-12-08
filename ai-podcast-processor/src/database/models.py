"""Data models for AI Podcast Processor."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json


@dataclass
class Podcast:
    """Podcast metadata."""
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    rss_feed_url: str = ""
    website_url: Optional[str] = None
    language: str = "nl"
    author: Optional[str] = None
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Episode:
    """Podcast episode."""
    id: Optional[int] = None
    podcast_id: int = 0
    guid: str = ""
    title: str = ""
    description: Optional[str] = None
    published_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    audio_url: str = ""
    audio_size_bytes: Optional[int] = None
    audio_type: str = "audio/mpeg"
    episode_url: Optional[str] = None

    # Processing status
    is_downloaded: bool = False
    is_transcribed: bool = False
    is_summarized: bool = False

    # File paths
    audio_file_path: Optional[str] = None
    transcript_file_path: Optional[str] = None
    summary_file_path: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Transcript:
    """Episode transcript."""
    id: Optional[int] = None
    episode_id: int = 0
    full_text: str = ""
    transcription_service: str = "whisper"
    language_detected: Optional[str] = None
    confidence_score: Optional[float] = None
    word_count: Optional[int] = None

    # Cost tracking
    audio_duration_seconds: Optional[int] = None
    cost_usd: Optional[float] = None

    created_at: Optional[datetime] = None


@dataclass
class TranscriptSegment:
    """Transcript segment with timestamps."""
    id: Optional[int] = None
    transcript_id: int = 0
    segment_index: int = 0
    start_time_ms: int = 0
    end_time_ms: int = 0
    text: str = ""
    speaker: Optional[str] = None
    confidence: Optional[float] = None


@dataclass
class Speaker:
    """Speaker in an episode."""
    id: Optional[int] = None
    episode_id: int = 0
    speaker_label: str = ""
    display_name: Optional[str] = None
    speaking_time_seconds: Optional[int] = None
    word_count: Optional[int] = None


@dataclass
class Summary:
    """Episode summary."""
    id: Optional[int] = None
    episode_id: int = 0

    # Main summary sections
    executive_summary: Optional[str] = None
    models_and_research: Optional[str] = None
    tooling: Optional[str] = None
    business_applications: Optional[str] = None
    policy_and_ethics: Optional[str] = None
    industry_news: Optional[str] = None
    key_takeaways: Optional[str] = None

    # Full structured summary as JSON
    full_summary_json: Optional[str] = None

    # Cost tracking
    input_tokens: Optional[int] = None
    output_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    model_used: str = "claude-sonnet-4-20250514"

    created_at: Optional[datetime] = None

    @property
    def full_summary(self) -> dict:
        """Parse full_summary_json as dict."""
        if self.full_summary_json:
            return json.loads(self.full_summary_json)
        return {}

    def to_markdown(self) -> str:
        """Convert summary to markdown format."""
        sections = []

        if self.executive_summary:
            sections.append(f"## Samenvatting\n\n{self.executive_summary}")

        if self.models_and_research:
            sections.append(f"## Models & Research\n\n{self.models_and_research}")

        if self.tooling:
            sections.append(f"## Tooling\n\n{self.tooling}")

        if self.business_applications:
            sections.append(f"## Business Applications\n\n{self.business_applications}")

        if self.policy_and_ethics:
            sections.append(f"## Policy & Ethics\n\n{self.policy_and_ethics}")

        if self.industry_news:
            sections.append(f"## Industry News\n\n{self.industry_news}")

        if self.key_takeaways:
            sections.append(f"## Key Takeaways\n\n{self.key_takeaways}")

        return "\n\n".join(sections)


@dataclass
class Tag:
    """Content tag."""
    id: Optional[int] = None
    name: str = ""
    category: Optional[str] = None  # 'topic', 'company', 'technology', 'person'
    created_at: Optional[datetime] = None


@dataclass
class EpisodeTag:
    """Episode-Tag relationship."""
    episode_id: int = 0
    tag_id: int = 0
    relevance_score: float = 1.0


@dataclass
class ProcessingLog:
    """Processing log entry."""
    id: Optional[int] = None
    episode_id: int = 0
    step: str = ""  # 'download', 'transcribe', 'summarize'
    status: str = ""  # 'started', 'completed', 'failed'
    error_message: Optional[str] = None
    duration_seconds: Optional[float] = None
    cost_usd: Optional[float] = None
    metadata_json: Optional[str] = None
    created_at: Optional[datetime] = None

    @property
    def metadata(self) -> dict:
        """Parse metadata_json as dict."""
        if self.metadata_json:
            return json.loads(self.metadata_json)
        return {}


@dataclass
class CostSummary:
    """Summary of processing costs."""
    episode_id: int
    episode_title: str
    transcription_cost: float = 0.0
    summarization_cost: float = 0.0
    total_cost: float = 0.0
    transcription_service: Optional[str] = None
    summarization_model: Optional[str] = None
