"""Audio file downloader for podcast episodes."""

import urllib.request
import hashlib
import logging
import time
import re
from pathlib import Path
from typing import Optional, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DownloadResult:
    """Result of audio download."""
    success: bool
    file_path: Optional[Path]
    file_size_bytes: int
    duration_seconds: float
    error: Optional[str] = None


class AudioDownloader:
    """Download podcast audio files."""

    def __init__(self, storage_dir: Path, user_agent: str = "AI-Podcast-Processor/1.0"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.user_agent = user_agent

    def _generate_filename(self, url: str, title: str) -> str:
        """Generate a safe filename for the audio file."""
        # Create a safe filename from title
        safe_title = re.sub(r'[^\w\s-]', '', title)
        safe_title = re.sub(r'[-\s]+', '-', safe_title).strip('-')
        safe_title = safe_title[:50]  # Limit length

        # Add hash of URL for uniqueness
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]

        # Get extension from URL or default to .mp3
        ext = '.mp3'
        url_path = url.split('?')[0]
        if '.' in url_path.split('/')[-1]:
            ext = '.' + url_path.split('.')[-1]
            if ext not in ['.mp3', '.m4a', '.wav', '.ogg', '.flac']:
                ext = '.mp3'

        return f"{safe_title}_{url_hash}{ext}"

    def download(
        self,
        url: str,
        title: str,
        timeout: int = 300,
        max_retries: int = 3,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> DownloadResult:
        """
        Download audio file from URL.

        Args:
            url: Audio file URL
            title: Episode title (used for filename)
            timeout: Download timeout in seconds
            max_retries: Number of retry attempts
            progress_callback: Optional callback(downloaded_bytes, total_bytes)

        Returns:
            DownloadResult with file path and metadata
        """
        filename = self._generate_filename(url, title)
        file_path = self.storage_dir / filename

        # Skip if already downloaded
        if file_path.exists():
            logger.info(f"File already exists: {file_path}")
            return DownloadResult(
                success=True,
                file_path=file_path,
                file_size_bytes=file_path.stat().st_size,
                duration_seconds=0
            )

        start_time = time.time()
        last_error = None

        for attempt in range(max_retries):
            try:
                logger.info(f"Downloading (attempt {attempt + 1}/{max_retries}): {url[:100]}...")

                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': self.user_agent}
                )

                with urllib.request.urlopen(req, timeout=timeout) as response:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    block_size = 8192

                    # Download to temporary file first
                    temp_path = file_path.with_suffix('.tmp')

                    with open(temp_path, 'wb') as f:
                        while True:
                            block = response.read(block_size)
                            if not block:
                                break
                            f.write(block)
                            downloaded += len(block)

                            if progress_callback and total_size > 0:
                                progress_callback(downloaded, total_size)

                    # Move temp file to final location
                    temp_path.rename(file_path)

                duration = time.time() - start_time
                logger.info(f"Downloaded {downloaded / (1024*1024):.1f} MB in {duration:.1f}s: {file_path}")

                return DownloadResult(
                    success=True,
                    file_path=file_path,
                    file_size_bytes=downloaded,
                    duration_seconds=duration
                )

            except Exception as e:
                last_error = str(e)
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

        # All retries failed
        logger.error(f"Failed to download after {max_retries} attempts: {last_error}")
        return DownloadResult(
            success=False,
            file_path=None,
            file_size_bytes=0,
            duration_seconds=time.time() - start_time,
            error=last_error
        )

    def get_audio_duration(self, file_path: Path) -> Optional[float]:
        """
        Get audio duration using ffprobe if available.
        Returns duration in seconds or None if unavailable.
        """
        import subprocess

        try:
            result = subprocess.run(
                ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                 '-of', 'csv=p=0', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0 and result.stdout.strip():
                return float(result.stdout.strip())
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        return None

    def cleanup_file(self, file_path: Path) -> bool:
        """Delete audio file after processing."""
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted audio file: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete file {file_path}: {e}")
        return False

    def get_storage_usage(self) -> dict:
        """Get storage usage statistics."""
        total_size = 0
        file_count = 0

        for file in self.storage_dir.glob('*'):
            if file.is_file():
                total_size += file.stat().st_size
                file_count += 1

        return {
            'total_size_bytes': total_size,
            'total_size_mb': total_size / (1024 * 1024),
            'file_count': file_count,
            'storage_dir': str(self.storage_dir)
        }
