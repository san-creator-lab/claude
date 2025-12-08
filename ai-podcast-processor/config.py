"""Configuration management for AI Podcast Processor."""

import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


@dataclass
class PodcastConfig:
    """Podcast-specific configuration."""
    name: str = "AI Report"
    rss_feed_url: str = "https://api.substack.com/feed/podcast/2351791.rss"
    spotify_url: str = "https://open.spotify.com/show/5Hpc8qDcawOEf4ulCouPau"
    language: str = "nl"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    type: str = field(default_factory=lambda: os.getenv("DB_TYPE", "sqlite"))
    sqlite_path: str = field(default_factory=lambda: os.getenv("SQLITE_PATH", "data/podcast.db"))

    # PostgreSQL settings (if using PostgreSQL)
    pg_host: str = field(default_factory=lambda: os.getenv("PG_HOST", "localhost"))
    pg_port: int = field(default_factory=lambda: int(os.getenv("PG_PORT", "5432")))
    pg_database: str = field(default_factory=lambda: os.getenv("PG_DATABASE", "podcast_processor"))
    pg_user: str = field(default_factory=lambda: os.getenv("PG_USER", "postgres"))
    pg_password: str = field(default_factory=lambda: os.getenv("PG_PASSWORD", ""))

    @property
    def connection_string(self) -> str:
        if self.type == "sqlite":
            return f"sqlite:///{self.sqlite_path}"
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_database}"


@dataclass
class TranscriptionConfig:
    """Transcription service configuration."""
    # Service selection: 'whisper' (OpenAI) or 'assemblyai'
    service: str = field(default_factory=lambda: os.getenv("TRANSCRIPTION_SERVICE", "whisper"))

    # OpenAI Whisper settings
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    whisper_model: str = field(default_factory=lambda: os.getenv("WHISPER_MODEL", "whisper-1"))

    # AssemblyAI settings (better for speaker diarization)
    assemblyai_api_key: str = field(default_factory=lambda: os.getenv("ASSEMBLYAI_API_KEY", ""))
    assemblyai_speaker_labels: bool = True
    assemblyai_language_code: str = "nl"  # Dutch

    # Cost per minute (USD) for tracking
    whisper_cost_per_minute: float = 0.006  # $0.006/minute
    assemblyai_cost_per_hour: float = 0.37  # $0.37/hour for standard tier


@dataclass
class SummarizerConfig:
    """Claude API configuration for summarization."""
    anthropic_api_key: str = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514"))
    max_tokens: int = 8192

    # Cost per 1M tokens (USD) - Claude 3.5 Sonnet pricing
    input_cost_per_million: float = 3.00
    output_cost_per_million: float = 15.00


@dataclass
class SchedulerConfig:
    """Scheduler configuration."""
    enabled: bool = field(default_factory=lambda: os.getenv("SCHEDULER_ENABLED", "true").lower() == "true")
    check_interval_hours: int = field(default_factory=lambda: int(os.getenv("CHECK_INTERVAL_HOURS", "24")))
    cron_expression: str = field(default_factory=lambda: os.getenv("CRON_EXPRESSION", "0 8 * * MON"))  # Monday 8 AM


@dataclass
class StorageConfig:
    """File storage configuration."""
    base_dir: Path = field(default_factory=lambda: Path(os.getenv("STORAGE_DIR", "data")))

    @property
    def audio_dir(self) -> Path:
        return self.base_dir / "audio"

    @property
    def transcripts_dir(self) -> Path:
        return self.base_dir / "transcripts"

    @property
    def summaries_dir(self) -> Path:
        return self.base_dir / "summaries"

    def ensure_dirs(self):
        """Create all necessary directories."""
        for dir_path in [self.audio_dir, self.transcripts_dir, self.summaries_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


@dataclass
class NotificationConfig:
    """Notification settings."""
    email_enabled: bool = field(default_factory=lambda: os.getenv("EMAIL_ENABLED", "false").lower() == "true")
    email_smtp_host: str = field(default_factory=lambda: os.getenv("SMTP_HOST", ""))
    email_smtp_port: int = field(default_factory=lambda: int(os.getenv("SMTP_PORT", "587")))
    email_from: str = field(default_factory=lambda: os.getenv("EMAIL_FROM", ""))
    email_to: str = field(default_factory=lambda: os.getenv("EMAIL_TO", ""))
    email_password: str = field(default_factory=lambda: os.getenv("EMAIL_PASSWORD", ""))


@dataclass
class Config:
    """Main configuration class."""
    podcast: PodcastConfig = field(default_factory=PodcastConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    transcription: TranscriptionConfig = field(default_factory=TranscriptionConfig)
    summarizer: SummarizerConfig = field(default_factory=SummarizerConfig)
    scheduler: SchedulerConfig = field(default_factory=SchedulerConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    notification: NotificationConfig = field(default_factory=NotificationConfig)

    # Debug mode
    debug: bool = field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors = []

        if self.transcription.service == "whisper" and not self.transcription.openai_api_key:
            errors.append("OPENAI_API_KEY is required when using Whisper transcription")

        if self.transcription.service == "assemblyai" and not self.transcription.assemblyai_api_key:
            errors.append("ASSEMBLYAI_API_KEY is required when using AssemblyAI transcription")

        if not self.summarizer.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required for summarization")

        return errors


# Global config instance
config = Config()
