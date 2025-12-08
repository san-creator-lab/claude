"""Tests for RSS parser."""

import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.fetcher.rss_parser import RSSParser, PodcastInfo, EpisodeInfo


class TestRSSParser:
    """Test RSS parser functionality."""

    @pytest.fixture
    def sample_rss_content(self):
        """Sample RSS feed content."""
        return """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
          <channel>
            <title>AI Report</title>
            <description>AI nieuws van Alexander en Wietse</description>
            <link>https://aireport.email</link>
            <language>nl</language>
            <itunes:author>Alexander Klöpping en Wietse Hage</itunes:author>
            <itunes:image href="https://example.com/image.jpg"/>
            <item>
              <title>Episode 1: GPT-5 komt eraan</title>
              <guid>episode-1</guid>
              <pubDate>Mon, 01 Jan 2024 08:00:00 +0000</pubDate>
              <description>In deze aflevering bespreken we GPT-5</description>
              <itunes:duration>45:30</itunes:duration>
              <enclosure url="https://example.com/ep1.mp3" type="audio/mpeg" length="12345678"/>
              <link>https://aireport.email/episode-1</link>
            </item>
            <item>
              <title>Episode 2: Claude vs ChatGPT</title>
              <guid>episode-2</guid>
              <pubDate>Mon, 08 Jan 2024 08:00:00 +0000</pubDate>
              <description>We vergelijken Claude met ChatGPT</description>
              <itunes:duration>1:02:15</itunes:duration>
              <enclosure url="https://example.com/ep2.mp3" type="audio/mpeg" length="23456789"/>
            </item>
          </channel>
        </rss>
        """

    def test_parse_podcast_info(self, sample_rss_content):
        """Test parsing podcast metadata."""
        parser = RSSParser("https://example.com/feed.rss")

        with patch.object(parser, 'fetch') as mock_fetch:
            mock_fetch.return_value = True
            import xml.etree.ElementTree as ET
            parser._root = ET.fromstring(sample_rss_content)

            info = parser.get_podcast_info()

            assert info is not None
            assert info.title == "AI Report"
            assert "Alexander" in (info.author or "")
            assert info.language == "nl"
            assert info.image_url == "https://example.com/image.jpg"

    def test_parse_episodes(self, sample_rss_content):
        """Test parsing episodes."""
        parser = RSSParser("https://example.com/feed.rss")

        with patch.object(parser, 'fetch') as mock_fetch:
            mock_fetch.return_value = True
            import xml.etree.ElementTree as ET
            parser._root = ET.fromstring(sample_rss_content)

            episodes = parser.get_episodes()

            assert len(episodes) == 2

            # Check first episode
            ep1 = episodes[0]
            assert ep1.title == "Episode 1: GPT-5 komt eraan"
            assert ep1.guid == "episode-1"
            assert ep1.audio_url == "https://example.com/ep1.mp3"
            assert ep1.duration_seconds == 45 * 60 + 30  # 45:30

            # Check second episode
            ep2 = episodes[1]
            assert ep2.title == "Episode 2: Claude vs ChatGPT"
            assert ep2.duration_seconds == 1 * 3600 + 2 * 60 + 15  # 1:02:15

    def test_parse_duration(self, sample_rss_content):
        """Test duration parsing."""
        parser = RSSParser("https://example.com/feed.rss")

        # Test various duration formats
        assert parser._parse_duration("45:30") == 2730  # MM:SS
        assert parser._parse_duration("1:02:15") == 3735  # HH:MM:SS
        assert parser._parse_duration("3600") == 3600  # seconds
        assert parser._parse_duration(None) is None

    def test_get_new_episodes(self, sample_rss_content):
        """Test filtering new episodes."""
        parser = RSSParser("https://example.com/feed.rss")

        with patch.object(parser, 'fetch') as mock_fetch:
            mock_fetch.return_value = True
            import xml.etree.ElementTree as ET
            parser._root = ET.fromstring(sample_rss_content)

            # No existing episodes
            new = parser.get_new_episodes(set())
            assert len(new) == 2

            # One existing episode
            new = parser.get_new_episodes({"episode-1"})
            assert len(new) == 1
            assert new[0].guid == "episode-2"

            # All existing
            new = parser.get_new_episodes({"episode-1", "episode-2"})
            assert len(new) == 0

    def test_clean_html(self, sample_rss_content):
        """Test HTML cleaning."""
        parser = RSSParser("https://example.com/feed.rss")

        assert parser._clean_html("<p>Hello <b>world</b></p>") == "Hello world"
        assert parser._clean_html(None) is None
        assert parser._clean_html("") == ""
