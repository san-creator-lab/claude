#!/usr/bin/env python3
"""
Script om een specifieke aflevering te verwerken (test/backfill).

Gebruik:
    python scripts/backfill_episode.py [--episode-id ID] [--skip-download] [--skip-transcription]

Dit script is handig voor:
- Testen van de pipeline met één aflevering
- Opnieuw verwerken van een gefaalde aflevering
- Backfill van oude afleveringen
"""

import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from src.database import get_db
from src.processor import PodcastProcessor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Process a specific podcast episode")
    parser.add_argument("--episode-id", "-e", type=int, help="Episode ID to process")
    parser.add_argument("--latest", action="store_true", help="Process latest episode")
    parser.add_argument("--skip-download", action="store_true", help="Skip download step")
    parser.add_argument("--skip-transcription", action="store_true", help="Skip transcription")
    parser.add_argument("--skip-summarization", action="store_true", help="Skip summarization")
    parser.add_argument("--dry-run", action="store_true", help="Just show what would be done")
    args = parser.parse_args()

    # Validate config
    errors = config.validate()
    if errors and not args.dry_run:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nCheck your .env file")
        return 1

    # Ensure data directory exists
    config.storage.ensure_dirs()

    # Initialize
    db = get_db(config.database.sqlite_path)

    # Get or create episode
    if args.latest:
        # First check for new episodes
        processor = PodcastProcessor(
            db=db,
            storage_dir=config.storage.base_dir,
            rss_url=config.podcast.rss_feed_url,
            transcription_service=config.transcription.service,
            openai_api_key=config.transcription.openai_api_key,
            assemblyai_api_key=config.transcription.assemblyai_api_key,
            anthropic_api_key=config.summarizer.anthropic_api_key,
            claude_model=config.summarizer.model,
            language=config.podcast.language
        )

        new_episodes = processor.check_for_new_episodes()
        if not new_episodes:
            # Get latest from database
            episodes = db.get_latest_episodes(limit=1)
            if not episodes:
                print("No episodes found")
                return 1
            episode = episodes[0]
        else:
            episode = new_episodes[0]

    elif args.episode_id:
        episode = db.get_episode(args.episode_id)
        if not episode:
            print(f"Episode {args.episode_id} not found")
            return 1
    else:
        # Show latest episodes and ask
        episodes = db.get_latest_episodes(limit=10)
        if not episodes:
            print("No episodes in database. Run 'python main.py check' first.")
            return 1

        print("\nAvailable episodes:")
        for ep in episodes:
            status = []
            if ep.is_downloaded:
                status.append("D")
            if ep.is_transcribed:
                status.append("T")
            if ep.is_summarized:
                status.append("S")
            status_str = "/".join(status) if status else "-"
            date = ep.published_at.strftime("%Y-%m-%d") if ep.published_at else "Unknown"
            print(f"  [{ep.id}] {date} [{status_str}] {ep.title[:50]}")

        print("\nUse --episode-id <ID> or --latest to select an episode")
        return 0

    # Show episode info
    print(f"\n{'='*60}")
    print(f"Episode: {episode.title}")
    print(f"ID: {episode.id}")
    print(f"Date: {episode.published_at}")
    print(f"Duration: {episode.duration_seconds // 60}:{episode.duration_seconds % 60:02d}" if episode.duration_seconds else "Unknown")
    print(f"{'='*60}")

    print(f"\nCurrent status:")
    print(f"  Downloaded: {'Yes' if episode.is_downloaded else 'No'}")
    print(f"  Transcribed: {'Yes' if episode.is_transcribed else 'No'}")
    print(f"  Summarized: {'Yes' if episode.is_summarized else 'No'}")

    if args.dry_run:
        print(f"\n[DRY RUN] Would process episode {episode.id}")

        # Estimate costs
        duration_min = (episode.duration_seconds or 2700) / 60  # default 45 min
        whisper_cost = duration_min * 0.006
        assemblyai_cost = (duration_min / 60) * 0.37
        claude_cost = 0.08  # rough estimate

        print(f"\nEstimated costs:")
        print(f"  Transcription (Whisper): ${whisper_cost:.4f}")
        print(f"  Transcription (AssemblyAI): ${assemblyai_cost:.4f}")
        print(f"  Summarization (Claude): ~${claude_cost:.4f}")
        return 0

    # Process episode
    processor = PodcastProcessor(
        db=db,
        storage_dir=config.storage.base_dir,
        rss_url=config.podcast.rss_feed_url,
        transcription_service=config.transcription.service,
        openai_api_key=config.transcription.openai_api_key,
        assemblyai_api_key=config.transcription.assemblyai_api_key,
        anthropic_api_key=config.summarizer.anthropic_api_key,
        claude_model=config.summarizer.model,
        language=config.podcast.language
    )

    print(f"\nProcessing episode...")
    result = processor.process_episode(
        episode,
        skip_download=args.skip_download,
        skip_transcription=args.skip_transcription,
        skip_summarization=args.skip_summarization
    )

    # Show results
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")

    for step, step_result in result.get("steps", {}).items():
        status = "OK" if step_result.get("success") else "FAILED"
        print(f"{step}: {status}")
        if step_result.get("error"):
            print(f"  Error: {step_result['error']}")
        if step_result.get("cost"):
            print(f"  Cost: ${step_result['cost']:.4f}")

    print(f"\nTotal cost: ${result.get('total_cost', 0):.4f}")

    # Show summary preview if available
    if result.get("steps", {}).get("summarization", {}).get("success"):
        summary = db.get_summary(episode.id)
        if summary:
            print(f"\n{'='*60}")
            print("SUMMARY PREVIEW")
            print(f"{'='*60}")
            print(f"\n{summary.executive_summary[:500]}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
