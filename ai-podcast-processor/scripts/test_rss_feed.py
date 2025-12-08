#!/usr/bin/env python3
"""Test script to parse the AI Report podcast RSS feed and display metadata."""

import xml.etree.ElementTree as ET
import urllib.request
import json
import re
from datetime import datetime
from email.utils import parsedate_to_datetime


RSS_FEED_URL = "https://api.substack.com/feed/podcast/2351791.rss"

# XML namespaces used in podcast RSS feeds
NAMESPACES = {
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom',
    'content': 'http://purl.org/rss/1.0/modules/content/',
}


def fetch_feed(url: str) -> str:
    """Fetch the RSS feed content."""
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'AI-Podcast-Processor/1.0'}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def clean_html(text: str) -> str:
    """Remove HTML tags from text."""
    if not text:
        return ""
    return re.sub(r'<[^>]+>', '', text).strip()


def parse_duration(duration_str: str) -> int:
    """Parse duration string to seconds."""
    if not duration_str:
        return 0

    parts = duration_str.split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(parts[0])
    except ValueError:
        return 0


def parse_feed():
    """Parse the RSS feed and return structured data."""
    print(f"Fetching RSS feed from: {RSS_FEED_URL}\n")

    xml_content = fetch_feed(RSS_FEED_URL)
    root = ET.fromstring(xml_content)
    channel = root.find('channel')

    if channel is None:
        print("Error: No channel found in RSS feed")
        return None

    # Helper to get text with namespace support
    def get_text(element, tag, ns=None):
        if ns:
            el = element.find(f'{{{NAMESPACES[ns]}}}{tag}')
        else:
            el = element.find(tag)
        return el.text if el is not None and el.text else None

    # Podcast metadata
    print("=" * 60)
    print("PODCAST METADATA")
    print("=" * 60)

    title = get_text(channel, 'title')
    description = get_text(channel, 'description')
    link = get_text(channel, 'link')
    language = get_text(channel, 'language')
    author = get_text(channel, 'author', 'itunes')

    print(f"Title: {title}")
    print(f"Description: {clean_html(description)[:200]}..." if description else "Description: N/A")
    print(f"Link: {link}")
    print(f"Language: {language}")
    print(f"Author: {author}")

    # iTunes category
    itunes_cat = channel.find(f'{{{NAMESPACES["itunes"]}}}category')
    if itunes_cat is not None:
        print(f"Category: {itunes_cat.get('text')}")

    # Image
    image = channel.find(f'{{{NAMESPACES["itunes"]}}}image')
    if image is not None:
        print(f"Image URL: {image.get('href')}")

    # Episodes
    items = channel.findall('item')
    print(f"\nTotal episodes found: {len(items)}")

    print("\n" + "=" * 60)
    print("RECENT EPISODES (laatste 5)")
    print("=" * 60)

    episodes = []

    for i, item in enumerate(items[:5]):
        ep_title = get_text(item, 'title')
        ep_link = get_text(item, 'link')
        ep_description = get_text(item, 'description')
        ep_pub_date = get_text(item, 'pubDate')
        ep_duration = get_text(item, 'duration', 'itunes')
        ep_guid = get_text(item, 'guid')

        # Get audio URL from enclosure
        enclosure = item.find('enclosure')
        audio_url = enclosure.get('url') if enclosure is not None else None
        audio_type = enclosure.get('type') if enclosure is not None else None
        audio_length = enclosure.get('length') if enclosure is not None else None

        # Parse publication date
        pub_datetime = None
        if ep_pub_date:
            try:
                pub_datetime = parsedate_to_datetime(ep_pub_date)
            except:
                pass

        print(f"\n--- Episode {i + 1} ---")
        print(f"Title: {ep_title}")
        print(f"Published: {pub_datetime.strftime('%Y-%m-%d %H:%M') if pub_datetime else ep_pub_date}")
        print(f"Duration: {ep_duration}")
        print(f"Summary: {clean_html(ep_description)[:300]}..." if ep_description else "Summary: N/A")
        print(f"Audio URL: {audio_url[:100]}..." if audio_url else "Audio URL: N/A")
        print(f"Audio Type: {audio_type}")
        print(f"File Size: {int(audio_length) / (1024*1024):.1f} MB" if audio_length else "File Size: N/A")
        print(f"GUID: {ep_guid}")

        episodes.append({
            'title': ep_title,
            'link': ep_link,
            'description': clean_html(ep_description) if ep_description else None,
            'pub_date': pub_datetime.isoformat() if pub_datetime else ep_pub_date,
            'duration': ep_duration,
            'duration_seconds': parse_duration(ep_duration),
            'guid': ep_guid,
            'audio_url': audio_url,
            'audio_type': audio_type,
            'audio_size_bytes': int(audio_length) if audio_length else None,
        })

    # Return structured data
    result = {
        'podcast': {
            'title': title,
            'description': clean_html(description) if description else None,
            'link': link,
            'language': language,
            'author': author,
            'rss_feed_url': RSS_FEED_URL,
        },
        'total_episodes': len(items),
        'latest_episodes': episodes,
    }

    print("\n" + "=" * 60)
    print("STRUCTURED DATA (JSON)")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


if __name__ == "__main__":
    try:
        result = parse_feed()
    except Exception as e:
        print(f"Error parsing feed: {e}")
        import traceback
        traceback.print_exc()
