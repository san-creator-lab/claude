"""RSS feed parser for podcast episodes."""

import xml.etree.ElementTree as ET
import urllib.request
import re
import logging
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# XML namespaces used in podcast RSS feeds
NAMESPACES = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}


@dataclass
class PodcastInfo:
    """Parsed podcast metadata."""
    title: str
    description: Optional[str]
    link: Optional[str]
    language: Optional[str]
    author: Optional[str]
    image_url: Optional[str]
    rss_feed_url: str


@dataclass
class EpisodeInfo:
    """Parsed episode metadata."""
    guid: str
    title: str
    description: Optional[str]
    published_at: Optional[datetime]
    duration_seconds: Optional[int]
    audio_url: str
    audio_size_bytes: Optional[int]
    audio_type: str
    episode_url: Optional[str]


class RSSParser:
    """Parse podcast RSS feeds."""

    def __init__(self, rss_url: str, user_agent: str = "AI-Podcast-Processor/1.0"):
        self.rss_url = rss_url
        self.user_agent = user_agent
        self._feed_content: Optional[str] = None
        self._root: Optional[ET.Element] = None

    def fetch(self, timeout: int = 30) -> bool:
        """Fetch RSS feed content."""
        try:
            req = urllib.request.Request(
                self.rss_url,
                headers={'User-Agent': self.user_agent}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                self._feed_content = response.read().decode('utf-8')
            self._root = ET.fromstring(self._feed_content)
            logger.info(f"Successfully fetched RSS feed from {self.rss_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to fetch RSS feed: {e}")
            return False

    def _get_text(self, element: ET.Element, tag: str, ns: Optional[str] = None) -> Optional[str]:
        """Get text content from element with namespace support."""
        if ns:
            el = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
        else:
            el = element.find(tag)
        return el.text if el is not None and el.text else None

    def _clean_html(self, text: Optional[str]) -> Optional[str]:
        """Remove HTML tags from text."""
        if not text:
            return None
        return re.sub(r'<[^>]+>', '', text).strip()

    def _parse_duration(self, duration_str: Optional[str]) -> Optional[int]:
        """Parse duration string (HH:MM:SS or MM:SS or seconds) to seconds."""
        if not duration_str:
            return None

        # Handle "HH:MM:SS" or "MM:SS" format
        parts = duration_str.split(':')
        try:
            if len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
            elif len(parts) == 2:
                return int(parts[0]) * 60 + int(parts[1])
            else:
                return int(float(parts[0]))
        except ValueError:
            return None

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse RSS date string to datetime."""
        if not date_str:
            return None
        try:
            return parsedate_to_datetime(date_str)
        except Exception:
            return None

    def get_podcast_info(self) -> Optional[PodcastInfo]:
        """Get podcast metadata."""
        if self._root is None:
            if not self.fetch():
                return None

        channel = self._root.find('channel')
        if channel is None:
            logger.error("No channel element found in RSS feed")
            return None

        title = self._get_text(channel, 'title')
        if not title:
            logger.error("Podcast has no title")
            return None

        # Get image URL
        image_url = None
        itunes_image = channel.find(f'{{{NAMESPACES["itunes"]}}}image')
        if itunes_image is not None:
            image_url = itunes_image.get('href')
        if not image_url:
            image_el = channel.find('image')
            if image_el is not None:
                url_el = image_el.find('url')
                if url_el is not None:
                    image_url = url_el.text

        return PodcastInfo(
            title=title,
            description=self._clean_html(self._get_text(channel, 'description')),
            link=self._get_text(channel, 'link'),
            language=self._get_text(channel, 'language'),
            author=self._get_text(channel, 'author', 'itunes'),
            image_url=image_url,
            rss_feed_url=self.rss_url
        )

    def get_episodes(self, limit: Optional[int] = None) -> list[EpisodeInfo]:
        """Get all episodes from feed."""
        if self._root is None:
            if not self.fetch():
                return []

        channel = self._root.find('channel')
        if channel is None:
            return []

        items = channel.findall('item')
        if limit:
            items = items[:limit]

        episodes = []
        for item in items:
            episode = self._parse_episode(item)
            if episode:
                episodes.append(episode)

        logger.info(f"Parsed {len(episodes)} episodes from feed")
        return episodes

    def _parse_episode(self, item: ET.Element) -> Optional[EpisodeInfo]:
        """Parse a single episode item."""
        # Get GUID (required for duplicate detection)
        guid = self._get_text(item, 'guid')
        if not guid:
            # Fall back to link or audio URL
            guid = self._get_text(item, 'link')

        title = self._get_text(item, 'title')
        if not title or not guid:
            return None

        # Get audio URL from enclosure
        audio_url = None
        audio_size = None
        audio_type = 'audio/mpeg'

        enclosure = item.find('enclosure')
        if enclosure is not None:
            audio_url = enclosure.get('url')
            audio_type = enclosure.get('type', 'audio/mpeg')
            try:
                audio_size = int(enclosure.get('length', 0)) or None
            except ValueError:
                audio_size = None

        if not audio_url:
            logger.warning(f"Episode '{title}' has no audio URL")
            return None

        return EpisodeInfo(
            guid=guid,
            title=title,
            description=self._clean_html(self._get_text(item, 'description')),
            published_at=self._parse_date(self._get_text(item, 'pubDate')),
            duration_seconds=self._parse_duration(self._get_text(item, 'duration', 'itunes')),
            audio_url=audio_url,
            audio_size_bytes=audio_size,
            audio_type=audio_type,
            episode_url=self._get_text(item, 'link')
        )

    def get_latest_episode(self) -> Optional[EpisodeInfo]:
        """Get the most recent episode."""
        episodes = self.get_episodes(limit=1)
        return episodes[0] if episodes else None

    def get_new_episodes(self, existing_guids: set[str]) -> list[EpisodeInfo]:
        """Get episodes that aren't in the existing set."""
        all_episodes = self.get_episodes()
        new_episodes = [ep for ep in all_episodes if ep.guid not in existing_guids]
        logger.info(f"Found {len(new_episodes)} new episodes out of {len(all_episodes)} total")
        return new_episodes
