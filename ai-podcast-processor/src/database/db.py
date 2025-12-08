"""Database connection and operations for AI Podcast Processor."""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from contextlib import contextmanager

from .models import (
    Podcast, Episode, Transcript, TranscriptSegment,
    Speaker, Summary, Tag, EpisodeTag, ProcessingLog, CostSummary
)


class Database:
    """SQLite database manager."""

    def __init__(self, db_path: str = "data/podcast.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _init_schema(self):
        """Initialize database schema."""
        schema_path = Path(__file__).parent.parent.parent / "schema.sql"
        if schema_path.exists():
            with open(schema_path) as f:
                schema = f.read()
            with self._get_connection() as conn:
                conn.executescript(schema)

    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager."""
        conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    # Podcast operations
    def get_podcast(self, podcast_id: int = 1) -> Optional[Podcast]:
        """Get podcast by ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM podcasts WHERE id = ?", (podcast_id,)
            ).fetchone()
            if row:
                return Podcast(**dict(row))
        return None

    def get_podcast_by_rss(self, rss_url: str) -> Optional[Podcast]:
        """Get podcast by RSS feed URL."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM podcasts WHERE rss_feed_url = ?", (rss_url,)
            ).fetchone()
            if row:
                return Podcast(**dict(row))
        return None

    def create_podcast(self, podcast: Podcast) -> int:
        """Create new podcast entry."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO podcasts (title, description, rss_feed_url, website_url, language, author, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (podcast.title, podcast.description, podcast.rss_feed_url,
                  podcast.website_url, podcast.language, podcast.author, podcast.image_url))
            return cursor.lastrowid

    # Episode operations
    def get_episode_by_guid(self, guid: str) -> Optional[Episode]:
        """Get episode by GUID (for duplicate detection)."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM episodes WHERE guid = ?", (guid,)
            ).fetchone()
            if row:
                return Episode(**dict(row))
        return None

    def get_episode(self, episode_id: int) -> Optional[Episode]:
        """Get episode by ID."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM episodes WHERE id = ?", (episode_id,)
            ).fetchone()
            if row:
                return Episode(**dict(row))
        return None

    def get_latest_episodes(self, podcast_id: int = 1, limit: int = 10) -> list[Episode]:
        """Get latest episodes for a podcast."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM episodes
                WHERE podcast_id = ?
                ORDER BY published_at DESC
                LIMIT ?
            """, (podcast_id, limit)).fetchall()
            return [Episode(**dict(row)) for row in rows]

    def get_unprocessed_episodes(self, podcast_id: int = 1) -> list[Episode]:
        """Get episodes that haven't been fully processed."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM episodes
                WHERE podcast_id = ?
                AND (is_transcribed = 0 OR is_summarized = 0)
                ORDER BY published_at DESC
            """, (podcast_id,)).fetchall()
            return [Episode(**dict(row)) for row in rows]

    def create_episode(self, episode: Episode) -> int:
        """Create new episode entry."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO episodes (
                    podcast_id, guid, title, description, published_at,
                    duration_seconds, audio_url, audio_size_bytes, audio_type, episode_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (episode.podcast_id, episode.guid, episode.title, episode.description,
                  episode.published_at, episode.duration_seconds, episode.audio_url,
                  episode.audio_size_bytes, episode.audio_type, episode.episode_url))
            return cursor.lastrowid

    def update_episode(self, episode: Episode):
        """Update episode entry."""
        with self._get_connection() as conn:
            conn.execute("""
                UPDATE episodes SET
                    is_downloaded = ?,
                    is_transcribed = ?,
                    is_summarized = ?,
                    audio_file_path = ?,
                    transcript_file_path = ?,
                    summary_file_path = ?,
                    updated_at = ?
                WHERE id = ?
            """, (episode.is_downloaded, episode.is_transcribed, episode.is_summarized,
                  episode.audio_file_path, episode.transcript_file_path, episode.summary_file_path,
                  datetime.now(), episode.id))

    def episode_exists(self, guid: str) -> bool:
        """Check if episode already exists by GUID."""
        return self.get_episode_by_guid(guid) is not None

    # Transcript operations
    def create_transcript(self, transcript: Transcript) -> int:
        """Create transcript entry."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO transcripts (
                    episode_id, full_text, transcription_service, language_detected,
                    confidence_score, word_count, audio_duration_seconds, cost_usd
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (transcript.episode_id, transcript.full_text, transcript.transcription_service,
                  transcript.language_detected, transcript.confidence_score, transcript.word_count,
                  transcript.audio_duration_seconds, transcript.cost_usd))
            return cursor.lastrowid

    def get_transcript(self, episode_id: int) -> Optional[Transcript]:
        """Get transcript for episode."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM transcripts WHERE episode_id = ?", (episode_id,)
            ).fetchone()
            if row:
                return Transcript(**dict(row))
        return None

    def create_transcript_segments(self, segments: list[TranscriptSegment]):
        """Create multiple transcript segments."""
        with self._get_connection() as conn:
            conn.executemany("""
                INSERT INTO transcript_segments (
                    transcript_id, segment_index, start_time_ms, end_time_ms,
                    text, speaker, confidence
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [(s.transcript_id, s.segment_index, s.start_time_ms, s.end_time_ms,
                   s.text, s.speaker, s.confidence) for s in segments])

    def get_transcript_segments(self, transcript_id: int) -> list[TranscriptSegment]:
        """Get all segments for a transcript."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM transcript_segments
                WHERE transcript_id = ?
                ORDER BY segment_index
            """, (transcript_id,)).fetchall()
            return [TranscriptSegment(**dict(row)) for row in rows]

    # Speaker operations
    def create_speakers(self, speakers: list[Speaker]):
        """Create speaker entries."""
        with self._get_connection() as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO speakers (
                    episode_id, speaker_label, display_name,
                    speaking_time_seconds, word_count
                ) VALUES (?, ?, ?, ?, ?)
            """, [(s.episode_id, s.speaker_label, s.display_name,
                   s.speaking_time_seconds, s.word_count) for s in speakers])

    def get_speakers(self, episode_id: int) -> list[Speaker]:
        """Get speakers for episode."""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM speakers WHERE episode_id = ?", (episode_id,)
            ).fetchall()
            return [Speaker(**dict(row)) for row in rows]

    # Summary operations
    def create_summary(self, summary: Summary) -> int:
        """Create summary entry."""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO summaries (
                    episode_id, executive_summary, models_and_research, tooling,
                    business_applications, policy_and_ethics, industry_news,
                    key_takeaways, full_summary_json, input_tokens, output_tokens,
                    cost_usd, model_used
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (summary.episode_id, summary.executive_summary, summary.models_and_research,
                  summary.tooling, summary.business_applications, summary.policy_and_ethics,
                  summary.industry_news, summary.key_takeaways, summary.full_summary_json,
                  summary.input_tokens, summary.output_tokens, summary.cost_usd, summary.model_used))
            return cursor.lastrowid

    def get_summary(self, episode_id: int) -> Optional[Summary]:
        """Get summary for episode."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM summaries WHERE episode_id = ?", (episode_id,)
            ).fetchone()
            if row:
                return Summary(**dict(row))
        return None

    # Tag operations
    def get_or_create_tag(self, name: str, category: Optional[str] = None) -> int:
        """Get existing tag or create new one."""
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT id FROM tags WHERE name = ?", (name,)
            ).fetchone()
            if row:
                return row["id"]

            cursor = conn.execute(
                "INSERT INTO tags (name, category) VALUES (?, ?)",
                (name, category)
            )
            return cursor.lastrowid

    def get_all_tags(self) -> list[Tag]:
        """Get all tags."""
        with self._get_connection() as conn:
            rows = conn.execute("SELECT * FROM tags ORDER BY name").fetchall()
            return [Tag(**dict(row)) for row in rows]

    def add_episode_tags(self, episode_id: int, tags: list[tuple[str, float, Optional[str]]]):
        """Add tags to episode. Tags format: [(name, relevance_score, category), ...]"""
        with self._get_connection() as conn:
            for name, relevance, category in tags:
                tag_id = self.get_or_create_tag(name, category)
                conn.execute("""
                    INSERT OR REPLACE INTO episode_tags (episode_id, tag_id, relevance_score)
                    VALUES (?, ?, ?)
                """, (episode_id, tag_id, relevance))

    def get_episode_tags(self, episode_id: int) -> list[tuple[Tag, float]]:
        """Get tags for episode with relevance scores."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT t.*, et.relevance_score
                FROM tags t
                JOIN episode_tags et ON t.id = et.tag_id
                WHERE et.episode_id = ?
                ORDER BY et.relevance_score DESC
            """, (episode_id,)).fetchall()
            return [(Tag(**{k: row[k] for k in row.keys() if k != 'relevance_score'}),
                     row['relevance_score']) for row in rows]

    def search_episodes_by_tag(self, tag_name: str, limit: int = 20) -> list[Episode]:
        """Search episodes by tag name."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT e.* FROM episodes e
                JOIN episode_tags et ON e.id = et.episode_id
                JOIN tags t ON et.tag_id = t.id
                WHERE t.name LIKE ?
                ORDER BY e.published_at DESC
                LIMIT ?
            """, (f"%{tag_name}%", limit)).fetchall()
            return [Episode(**dict(row)) for row in rows]

    # Processing log operations
    def log_processing(self, episode_id: int, step: str, status: str,
                       error: Optional[str] = None, duration: Optional[float] = None,
                       cost: Optional[float] = None, metadata: Optional[dict] = None):
        """Log processing step."""
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO processing_log (
                    episode_id, step, status, error_message,
                    duration_seconds, cost_usd, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (episode_id, step, status, error, duration, cost,
                  json.dumps(metadata) if metadata else None))

    def get_processing_logs(self, episode_id: int) -> list[ProcessingLog]:
        """Get processing logs for episode."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM processing_log
                WHERE episode_id = ?
                ORDER BY created_at
            """, (episode_id,)).fetchall()
            return [ProcessingLog(**dict(row)) for row in rows]

    # Cost tracking
    def get_cost_summary(self, episode_id: int) -> Optional[CostSummary]:
        """Get cost summary for episode."""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT
                    e.id as episode_id,
                    e.title as episode_title,
                    COALESCE(t.cost_usd, 0) as transcription_cost,
                    COALESCE(s.cost_usd, 0) as summarization_cost,
                    COALESCE(t.cost_usd, 0) + COALESCE(s.cost_usd, 0) as total_cost,
                    t.transcription_service,
                    s.model_used as summarization_model
                FROM episodes e
                LEFT JOIN transcripts t ON e.id = t.episode_id
                LEFT JOIN summaries s ON e.id = s.episode_id
                WHERE e.id = ?
            """, (episode_id,)).fetchone()
            if row:
                return CostSummary(**dict(row))
        return None

    def get_total_costs(self, podcast_id: int = 1) -> dict:
        """Get total costs for all episodes."""
        with self._get_connection() as conn:
            row = conn.execute("""
                SELECT
                    COUNT(DISTINCT e.id) as episode_count,
                    COALESCE(SUM(t.cost_usd), 0) as total_transcription_cost,
                    COALESCE(SUM(s.cost_usd), 0) as total_summarization_cost,
                    COALESCE(SUM(t.cost_usd), 0) + COALESCE(SUM(s.cost_usd), 0) as total_cost
                FROM episodes e
                LEFT JOIN transcripts t ON e.id = t.episode_id
                LEFT JOIN summaries s ON e.id = s.episode_id
                WHERE e.podcast_id = ?
            """, (podcast_id,)).fetchone()
            return dict(row) if row else {}

    # Search
    def search_transcripts(self, query: str, limit: int = 10) -> list[tuple[Episode, str]]:
        """Search transcripts for keyword."""
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT e.*, t.full_text
                FROM episodes e
                JOIN transcripts t ON e.id = t.episode_id
                WHERE t.full_text LIKE ?
                ORDER BY e.published_at DESC
                LIMIT ?
            """, (f"%{query}%", limit)).fetchall()

            results = []
            for row in rows:
                episode_data = {k: row[k] for k in row.keys() if k != 'full_text'}
                episode = Episode(**episode_data)

                # Extract relevant snippet
                text = row['full_text']
                idx = text.lower().find(query.lower())
                if idx >= 0:
                    start = max(0, idx - 100)
                    end = min(len(text), idx + len(query) + 100)
                    snippet = "..." + text[start:end] + "..."
                else:
                    snippet = text[:200] + "..."

                results.append((episode, snippet))

            return results


# Global database instance
_db: Optional[Database] = None


def get_db(db_path: str = "data/podcast.db") -> Database:
    """Get or create database instance."""
    global _db
    if _db is None:
        _db = Database(db_path)
    return _db
