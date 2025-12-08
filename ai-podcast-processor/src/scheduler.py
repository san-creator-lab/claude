"""Scheduler for automatic podcast processing."""

import logging
import signal
import sys
import time
from datetime import datetime
from typing import Optional, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)


class PodcastScheduler:
    """Schedule automatic podcast processing."""

    def __init__(
        self,
        process_callback: Callable[[], None],
        cron_expression: Optional[str] = None,
        interval_hours: Optional[int] = None
    ):
        """
        Initialize scheduler.

        Args:
            process_callback: Function to call when checking for new episodes
            cron_expression: Cron expression (e.g., "0 8 * * MON" for Monday 8 AM)
            interval_hours: Alternative: check every N hours
        """
        self.process_callback = process_callback
        self.cron_expression = cron_expression
        self.interval_hours = interval_hours
        self.scheduler = BackgroundScheduler()
        self._running = False

    def start(self):
        """Start the scheduler."""
        if self._running:
            logger.warning("Scheduler already running")
            return

        # Add job based on configuration
        if self.cron_expression:
            self.scheduler.add_job(
                self._run_job,
                CronTrigger.from_crontab(self.cron_expression),
                id="podcast_check",
                name="Check for new podcast episodes",
                replace_existing=True
            )
            logger.info(f"Scheduled job with cron: {self.cron_expression}")
        elif self.interval_hours:
            self.scheduler.add_job(
                self._run_job,
                IntervalTrigger(hours=self.interval_hours),
                id="podcast_check",
                name="Check for new podcast episodes",
                replace_existing=True
            )
            logger.info(f"Scheduled job every {self.interval_hours} hours")
        else:
            raise ValueError("Either cron_expression or interval_hours must be specified")

        self.scheduler.start()
        self._running = True

        # Handle shutdown gracefully
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

        logger.info("Scheduler started")

    def stop(self):
        """Stop the scheduler."""
        if self._running:
            self.scheduler.shutdown()
            self._running = False
            logger.info("Scheduler stopped")

    def _run_job(self):
        """Execute the processing job."""
        logger.info(f"Starting scheduled job at {datetime.now()}")
        try:
            self.process_callback()
            logger.info("Scheduled job completed successfully")
        except Exception as e:
            logger.error(f"Scheduled job failed: {e}")

    def _shutdown(self, signum, frame):
        """Handle shutdown signals."""
        logger.info("Received shutdown signal")
        self.stop()
        sys.exit(0)

    def run_now(self):
        """Run the job immediately (for testing)."""
        logger.info("Running job immediately")
        self._run_job()

    def get_next_run_time(self) -> Optional[datetime]:
        """Get the next scheduled run time."""
        job = self.scheduler.get_job("podcast_check")
        if job:
            return job.next_run_time
        return None

    def run_forever(self):
        """Run scheduler and block until shutdown."""
        self.start()
        try:
            while self._running:
                time.sleep(60)
        except (KeyboardInterrupt, SystemExit):
            self.stop()


def create_scheduler_from_config(
    process_callback: Callable[[], None],
    enabled: bool = True,
    cron_expression: str = "0 8 * * MON",
    interval_hours: Optional[int] = None
) -> Optional[PodcastScheduler]:
    """
    Create scheduler from configuration.

    Args:
        process_callback: Function to call
        enabled: Whether scheduler is enabled
        cron_expression: Cron expression for scheduling
        interval_hours: Optional interval in hours (overrides cron)

    Returns:
        Configured scheduler or None if disabled
    """
    if not enabled:
        logger.info("Scheduler disabled in configuration")
        return None

    if interval_hours:
        return PodcastScheduler(
            process_callback=process_callback,
            interval_hours=interval_hours
        )
    else:
        return PodcastScheduler(
            process_callback=process_callback,
            cron_expression=cron_expression
        )
