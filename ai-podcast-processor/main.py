#!/usr/bin/env python3
"""Main entry point for AI Podcast Processor."""

import argparse
import logging
import sys
from pathlib import Path

from config import config
from src.database import get_db
from src.processor import PodcastProcessor
from src.scheduler import create_scheduler_from_config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data/podcast_processor.log")
    ]
)
logger = logging.getLogger(__name__)


def create_processor() -> PodcastProcessor:
    """Create configured podcast processor."""
    config.storage.ensure_dirs()

    db = get_db(config.database.sqlite_path)

    return PodcastProcessor(
        db=db,
        storage_dir=config.storage.base_dir,
        rss_url=config.podcast.rss_feed_url,
        transcription_service=config.transcription.service,
        openai_api_key=config.transcription.openai_api_key,
        assemblyai_api_key=config.transcription.assemblyai_api_key,
        anthropic_api_key=config.summarizer.anthropic_api_key,
        claude_model=config.summarizer.model,
        language=config.podcast.language,
        cleanup_audio=False
    )


def cmd_check(args):
    """Check for new episodes."""
    processor = create_processor()
    new_episodes = processor.check_for_new_episodes()

    if new_episodes:
        print(f"\nFound {len(new_episodes)} new episodes:")
        for ep in new_episodes:
            print(f"  - {ep.title} ({ep.published_at})")
    else:
        print("No new episodes found.")


def cmd_process(args):
    """Process pending episodes."""
    processor = create_processor()

    if args.episode_id:
        # Process specific episode
        episode = processor.db.get_episode(args.episode_id)
        if not episode:
            print(f"Episode {args.episode_id} not found")
            return 1

        result = processor.process_episode(
            episode,
            skip_download=args.skip_download,
            skip_transcription=args.skip_transcription,
            skip_summarization=args.skip_summarization
        )
        print(f"\nProcessed: {result['title']}")
        print(f"Total cost: ${result['total_cost']:.4f}")
    else:
        # Process all pending
        results = processor.process_all_pending()
        total_cost = sum(r.get('total_cost', 0) for r in results)
        print(f"\nProcessed {len(results)} episodes")
        print(f"Total cost: ${total_cost:.4f}")

    return 0


def cmd_run(args):
    """Run the scheduler."""
    processor = create_processor()

    def process_new():
        new_episodes = processor.check_for_new_episodes()
        for episode in new_episodes:
            processor.process_episode(episode)

    # Validate config
    errors = config.validate()
    if errors:
        print("Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    scheduler = create_scheduler_from_config(
        process_callback=process_new,
        enabled=config.scheduler.enabled,
        cron_expression=config.scheduler.cron_expression,
        interval_hours=config.scheduler.check_interval_hours if not config.scheduler.cron_expression else None
    )

    if scheduler:
        print(f"Starting scheduler...")
        print(f"Next run: {scheduler.get_next_run_time()}")
        scheduler.run_forever()
    else:
        print("Scheduler is disabled")
        return 1


def cmd_list(args):
    """List episodes."""
    db = get_db(config.database.sqlite_path)
    episodes = db.get_latest_episodes(limit=args.limit)

    print(f"\nLatest {len(episodes)} episodes:\n")
    print(f"{'ID':<5} {'Date':<12} {'Status':<15} {'Title'}")
    print("-" * 80)

    for ep in episodes:
        date = ep.published_at.strftime("%Y-%m-%d") if ep.published_at else "Unknown"
        status = []
        if ep.is_downloaded:
            status.append("D")
        if ep.is_transcribed:
            status.append("T")
        if ep.is_summarized:
            status.append("S")
        status_str = "/".join(status) if status else "-"
        print(f"{ep.id:<5} {date:<12} {status_str:<15} {ep.title[:45]}")


def cmd_summary(args):
    """Show episode summary."""
    db = get_db(config.database.sqlite_path)
    summary = db.get_summary(args.episode_id)

    if not summary:
        print(f"No summary found for episode {args.episode_id}")
        return 1

    episode = db.get_episode(args.episode_id)

    if args.format == "markdown":
        print(summary.to_markdown())
    else:
        print(f"\n{'='*60}")
        print(f"Episode: {episode.title if episode else args.episode_id}")
        print(f"{'='*60}")
        print(f"\n## Samenvatting\n{summary.executive_summary}")
        print(f"\n## Key Takeaways\n{summary.key_takeaways}")
        print(f"\n## Tags")
        tags = db.get_episode_tags(args.episode_id)
        for tag, score in tags[:10]:
            print(f"  - {tag.name} ({tag.category}) [{score:.1f}]")


def cmd_costs(args):
    """Show cost report."""
    db = get_db(config.database.sqlite_path)
    costs = db.get_total_costs()

    print(f"\n{'='*40}")
    print("COST REPORT")
    print(f"{'='*40}")
    print(f"Episodes processed: {costs.get('episode_count', 0)}")
    print(f"Transcription cost: ${costs.get('total_transcription_cost', 0):.4f}")
    print(f"Summarization cost: ${costs.get('total_summarization_cost', 0):.4f}")
    print(f"{'='*40}")
    print(f"TOTAL COST: ${costs.get('total_cost', 0):.4f}")


def cmd_search(args):
    """Search transcripts."""
    db = get_db(config.database.sqlite_path)
    results = db.search_transcripts(args.query, limit=args.limit)

    print(f"\nSearch results for '{args.query}':\n")

    for episode, snippet in results:
        date = episode.published_at.strftime("%Y-%m-%d") if episode.published_at else "Unknown"
        print(f"[{episode.id}] {date} - {episode.title}")
        print(f"    ...{snippet}...")
        print()


def cmd_backfill(args):
    """Process historical episodes."""
    processor = create_processor()

    # First check for all episodes
    processor.check_for_new_episodes()

    # Get unprocessed episodes
    episodes = processor.db.get_unprocessed_episodes()

    if args.limit:
        episodes = episodes[:args.limit]

    print(f"Processing {len(episodes)} episodes...")

    for episode in episodes:
        print(f"\nProcessing: {episode.title}")
        result = processor.process_episode(episode)
        print(f"  Cost: ${result.get('total_cost', 0):.4f}")

        if args.dry_run:
            print("  (dry run - skipping)")
            break


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Podcast Processor - Process, transcribe, and summarize AI Report podcast"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check for new episodes")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process episodes")
    process_parser.add_argument("--episode-id", "-e", type=int, help="Process specific episode")
    process_parser.add_argument("--skip-download", action="store_true", help="Skip download step")
    process_parser.add_argument("--skip-transcription", action="store_true", help="Skip transcription")
    process_parser.add_argument("--skip-summarization", action="store_true", help="Skip summarization")

    # Run command (scheduler)
    run_parser = subparsers.add_parser("run", help="Run scheduler for automatic processing")

    # List command
    list_parser = subparsers.add_parser("list", help="List episodes")
    list_parser.add_argument("--limit", "-l", type=int, default=20, help="Number of episodes")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Show episode summary")
    summary_parser.add_argument("episode_id", type=int, help="Episode ID")
    summary_parser.add_argument("--format", "-f", choices=["text", "markdown"], default="text")

    # Costs command
    costs_parser = subparsers.add_parser("costs", help="Show cost report")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search transcripts")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")

    # Backfill command
    backfill_parser = subparsers.add_parser("backfill", help="Process historical episodes")
    backfill_parser.add_argument("--limit", "-l", type=int, help="Max episodes to process")
    backfill_parser.add_argument("--dry-run", action="store_true", help="Test run")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)

    commands = {
        "check": cmd_check,
        "process": cmd_process,
        "run": cmd_run,
        "list": cmd_list,
        "summary": cmd_summary,
        "costs": cmd_costs,
        "search": cmd_search,
        "backfill": cmd_backfill,
    }

    return commands[args.command](args) or 0


if __name__ == "__main__":
    sys.exit(main())
