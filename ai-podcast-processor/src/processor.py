"""Main podcast processor that orchestrates fetching, transcription, and summarization."""

import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from .database import Database, get_db, Episode, Transcript, Summary, ProcessingLog
from .database.models import TranscriptSegment as DBTranscriptSegment, Speaker
from .fetcher import RSSParser, AudioDownloader
from .transcriber import get_transcriber, TranscriptionResult
from .summarizer import ClaudeSummarizer, SummaryResult

logger = logging.getLogger(__name__)


class PodcastProcessor:
    """Main processor for podcast episodes."""

    def __init__(
        self,
        db: Database,
        storage_dir: Path,
        rss_url: str,
        # Transcription config
        transcription_service: str = "whisper",
        openai_api_key: Optional[str] = None,
        assemblyai_api_key: Optional[str] = None,
        # Summarization config
        anthropic_api_key: Optional[str] = None,
        claude_model: str = "claude-sonnet-4-20250514",
        # Options
        language: str = "nl",
        cleanup_audio: bool = False
    ):
        self.db = db
        self.storage_dir = Path(storage_dir)
        self.rss_url = rss_url
        self.cleanup_audio = cleanup_audio

        # Initialize components
        self.rss_parser = RSSParser(rss_url)
        self.downloader = AudioDownloader(self.storage_dir / "audio")

        # Transcriber
        self.transcriber = get_transcriber(
            service=transcription_service,
            openai_api_key=openai_api_key,
            assemblyai_api_key=assemblyai_api_key,
            language=language
        )

        # Summarizer
        if anthropic_api_key:
            self.summarizer = ClaudeSummarizer(
                api_key=anthropic_api_key,
                model=claude_model
            )
        else:
            self.summarizer = None
            logger.warning("No Anthropic API key - summarization disabled")

        # Ensure directories exist
        (self.storage_dir / "audio").mkdir(parents=True, exist_ok=True)
        (self.storage_dir / "transcripts").mkdir(parents=True, exist_ok=True)
        (self.storage_dir / "summaries").mkdir(parents=True, exist_ok=True)

    def check_for_new_episodes(self) -> list[Episode]:
        """Check RSS feed for new episodes and add them to database."""
        logger.info("Checking for new episodes...")

        # Get existing GUIDs from database
        existing_episodes = self.db.get_latest_episodes(limit=1000)
        existing_guids = {ep.guid for ep in existing_episodes}

        # Fetch and parse RSS
        new_episode_infos = self.rss_parser.get_new_episodes(existing_guids)

        if not new_episode_infos:
            logger.info("No new episodes found")
            return []

        logger.info(f"Found {len(new_episode_infos)} new episodes")

        # Get or create podcast entry
        podcast = self.db.get_podcast_by_rss(self.rss_url)
        if not podcast:
            podcast_info = self.rss_parser.get_podcast_info()
            if podcast_info:
                from .database.models import Podcast as PodcastModel
                podcast_model = PodcastModel(
                    title=podcast_info.title,
                    description=podcast_info.description,
                    rss_feed_url=podcast_info.rss_feed_url,
                    website_url=podcast_info.link,
                    language=podcast_info.language or "nl",
                    author=podcast_info.author,
                    image_url=podcast_info.image_url
                )
                podcast_id = self.db.create_podcast(podcast_model)
            else:
                podcast_id = 1
        else:
            podcast_id = podcast.id

        # Add episodes to database
        new_episodes = []
        for ep_info in new_episode_infos:
            episode = Episode(
                podcast_id=podcast_id,
                guid=ep_info.guid,
                title=ep_info.title,
                description=ep_info.description,
                published_at=ep_info.published_at,
                duration_seconds=ep_info.duration_seconds,
                audio_url=ep_info.audio_url,
                audio_size_bytes=ep_info.audio_size_bytes,
                audio_type=ep_info.audio_type,
                episode_url=ep_info.episode_url
            )
            episode.id = self.db.create_episode(episode)
            new_episodes.append(episode)
            logger.info(f"Added episode: {episode.title}")

        return new_episodes

    def process_episode(
        self,
        episode: Episode,
        skip_download: bool = False,
        skip_transcription: bool = False,
        skip_summarization: bool = False
    ) -> dict:
        """
        Process a single episode through the full pipeline.

        Returns dict with processing results and costs.
        """
        logger.info(f"Processing episode: {episode.title}")
        results = {
            "episode_id": episode.id,
            "title": episode.title,
            "steps": {},
            "total_cost": 0.0
        }

        # Step 1: Download audio
        if not skip_download and not episode.is_downloaded:
            download_result = self._download_episode(episode)
            results["steps"]["download"] = download_result
            if not download_result["success"]:
                return results

        # Step 2: Transcribe
        if not skip_transcription and not episode.is_transcribed:
            transcription_result = self._transcribe_episode(episode)
            results["steps"]["transcription"] = transcription_result
            results["total_cost"] += transcription_result.get("cost", 0)
            if not transcription_result["success"]:
                return results

        # Step 3: Summarize
        if not skip_summarization and not episode.is_summarized and self.summarizer:
            summary_result = self._summarize_episode(episode)
            results["steps"]["summarization"] = summary_result
            results["total_cost"] += summary_result.get("cost", 0)

        # Cleanup audio if requested
        if self.cleanup_audio and episode.audio_file_path:
            audio_path = Path(episode.audio_file_path)
            if audio_path.exists():
                self.downloader.cleanup_file(audio_path)
                episode.audio_file_path = None
                self.db.update_episode(episode)

        logger.info(f"Finished processing: {episode.title} (cost: ${results['total_cost']:.4f})")
        return results

    def _download_episode(self, episode: Episode) -> dict:
        """Download episode audio."""
        logger.info(f"Downloading: {episode.title}")
        start_time = time.time()

        self.db.log_processing(episode.id, "download", "started")

        result = self.downloader.download(
            url=episode.audio_url,
            title=episode.title
        )

        duration = time.time() - start_time

        if result.success:
            episode.is_downloaded = True
            episode.audio_file_path = str(result.file_path)
            self.db.update_episode(episode)
            self.db.log_processing(
                episode.id, "download", "completed",
                duration=duration,
                metadata={"file_size_bytes": result.file_size_bytes}
            )
            return {"success": True, "file_path": str(result.file_path)}
        else:
            self.db.log_processing(
                episode.id, "download", "failed",
                error=result.error, duration=duration
            )
            return {"success": False, "error": result.error}

    def _transcribe_episode(self, episode: Episode) -> dict:
        """Transcribe episode audio."""
        logger.info(f"Transcribing: {episode.title}")
        start_time = time.time()

        if not episode.audio_file_path:
            return {"success": False, "error": "No audio file available"}

        audio_path = Path(episode.audio_file_path)
        if not audio_path.exists():
            return {"success": False, "error": f"Audio file not found: {audio_path}"}

        self.db.log_processing(episode.id, "transcribe", "started")

        result = self.transcriber.transcribe(audio_path)
        duration = time.time() - start_time

        if result.success:
            # Save transcript to database
            transcript = Transcript(
                episode_id=episode.id,
                full_text=result.full_text,
                transcription_service=result.service,
                language_detected=result.language_detected,
                confidence_score=result.confidence_score,
                word_count=result.word_count,
                audio_duration_seconds=int(result.audio_duration_seconds),
                cost_usd=result.cost_usd
            )
            transcript_id = self.db.create_transcript(transcript)

            # Save segments if available
            if result.segments:
                db_segments = [
                    DBTranscriptSegment(
                        transcript_id=transcript_id,
                        segment_index=i,
                        start_time_ms=seg.start_time_ms,
                        end_time_ms=seg.end_time_ms,
                        text=seg.text,
                        speaker=seg.speaker,
                        confidence=seg.confidence
                    )
                    for i, seg in enumerate(result.segments)
                ]
                self.db.create_transcript_segments(db_segments)

            # Save speakers if available
            if result.speakers:
                db_speakers = [
                    Speaker(
                        episode_id=episode.id,
                        speaker_label=spk.label,
                        display_name=spk.display_name,
                        speaking_time_seconds=spk.speaking_time_ms // 1000,
                        word_count=spk.word_count
                    )
                    for spk in result.speakers
                ]
                self.db.create_speakers(db_speakers)

            # Save transcript to file
            transcript_path = self.storage_dir / "transcripts" / f"{episode.id}.txt"
            transcript_path.write_text(result.full_text, encoding="utf-8")

            # Also save with timestamps
            timestamp_path = self.storage_dir / "transcripts" / f"{episode.id}_timestamps.txt"
            timestamp_path.write_text(result.to_text_with_timestamps(), encoding="utf-8")

            # Update episode
            episode.is_transcribed = True
            episode.transcript_file_path = str(transcript_path)
            self.db.update_episode(episode)

            self.db.log_processing(
                episode.id, "transcribe", "completed",
                duration=duration, cost=result.cost_usd,
                metadata={
                    "word_count": result.word_count,
                    "audio_duration": result.audio_duration_seconds,
                    "service": result.service
                }
            )

            return {
                "success": True,
                "word_count": result.word_count,
                "cost": result.cost_usd,
                "service": result.service
            }
        else:
            self.db.log_processing(
                episode.id, "transcribe", "failed",
                error=result.error, duration=duration
            )
            return {"success": False, "error": result.error}

    def _summarize_episode(self, episode: Episode) -> dict:
        """Generate summary for episode."""
        logger.info(f"Summarizing: {episode.title}")
        start_time = time.time()

        # Get transcript
        transcript = self.db.get_transcript(episode.id)
        if not transcript:
            return {"success": False, "error": "No transcript available"}

        self.db.log_processing(episode.id, "summarize", "started")

        # Generate summary
        result = self.summarizer.summarize(
            transcript=transcript.full_text,
            title=episode.title,
            date=episode.published_at.strftime("%Y-%m-%d") if episode.published_at else "",
            duration=f"{episode.duration_seconds // 60}:{episode.duration_seconds % 60:02d}" if episode.duration_seconds else ""
        )

        duration = time.time() - start_time

        if result.success:
            # Save summary to database
            import json
            summary = Summary(
                episode_id=episode.id,
                executive_summary=result.executive_summary,
                models_and_research=result.models_and_research,
                tooling=result.tooling,
                business_applications=result.business_applications,
                policy_and_ethics=result.policy_and_ethics,
                industry_news=result.industry_news,
                key_takeaways=result.key_takeaways,
                full_summary_json=json.dumps(result.full_response, ensure_ascii=False),
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                cost_usd=result.cost_usd,
                model_used=result.model_used
            )
            self.db.create_summary(summary)

            # Save tags
            if result.tags:
                self.db.add_episode_tags(episode.id, result.tags)

            # Save summary to file
            summary_path = self.storage_dir / "summaries" / f"{episode.id}.md"
            summary_path.write_text(result.to_markdown(), encoding="utf-8")

            # Update episode
            episode.is_summarized = True
            episode.summary_file_path = str(summary_path)
            self.db.update_episode(episode)

            self.db.log_processing(
                episode.id, "summarize", "completed",
                duration=duration, cost=result.cost_usd,
                metadata={
                    "input_tokens": result.input_tokens,
                    "output_tokens": result.output_tokens,
                    "model": result.model_used,
                    "tag_count": len(result.tags)
                }
            )

            return {
                "success": True,
                "cost": result.cost_usd,
                "tokens": {"input": result.input_tokens, "output": result.output_tokens}
            }
        else:
            self.db.log_processing(
                episode.id, "summarize", "failed",
                error=result.error, duration=duration
            )
            return {"success": False, "error": result.error}

    def process_all_pending(self) -> list[dict]:
        """Process all episodes that haven't been fully processed."""
        episodes = self.db.get_unprocessed_episodes()
        results = []

        for episode in episodes:
            result = self.process_episode(episode)
            results.append(result)

        return results

    def get_cost_report(self) -> dict:
        """Generate cost report for all processed episodes."""
        return self.db.get_total_costs()
