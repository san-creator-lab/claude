#!/usr/bin/env python3
"""
Simple web UI for browsing podcast summaries.

Usage:
    python web_ui.py

Then open http://localhost:5000 in your browser.
"""

from flask import Flask, render_template_string, request, jsonify
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config import config
from src.database import get_db

app = Flask(__name__)
db = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Report Podcast - Samenvattingen</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 20px;
            margin-bottom: 30px;
        }
        header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        header p {
            opacity: 0.9;
        }
        .search-box {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        .search-box input {
            width: 100%;
            padding: 15px;
            font-size: 1rem;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            outline: none;
            transition: border-color 0.3s;
        }
        .search-box input:focus {
            border-color: #667eea;
        }
        .episodes {
            display: grid;
            gap: 20px;
        }
        .episode-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .episode-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        }
        .episode-header {
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }
        .episode-header h2 {
            font-size: 1.3rem;
            margin-bottom: 5px;
            color: #333;
        }
        .episode-meta {
            color: #666;
            font-size: 0.9rem;
        }
        .episode-content {
            padding: 20px;
        }
        .episode-summary {
            margin-bottom: 20px;
        }
        .episode-summary h3 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 1rem;
        }
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        .tag {
            background: #e8eaf6;
            color: #5c6bc0;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
        }
        .tag.company { background: #e3f2fd; color: #1976d2; }
        .tag.technology { background: #f3e5f5; color: #7b1fa2; }
        .tag.topic { background: #e8f5e9; color: #388e3c; }
        .section {
            margin-bottom: 20px;
            padding: 15px;
            background: #fafafa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        .section h4 {
            margin-bottom: 10px;
            color: #555;
        }
        .costs {
            background: #fff3e0;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .costs h3 {
            color: #e65100;
            margin-bottom: 10px;
        }
        .expand-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 0.9rem;
        }
        .expand-btn:hover {
            background: #5a6fd6;
        }
        .hidden { display: none; }
        footer {
            text-align: center;
            padding: 30px;
            color: #666;
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>AI Report Podcast</h1>
            <p>Samenvattingen van de podcast van Alexander Klöpping en Wietse Hage</p>
        </div>
    </header>

    <div class="container">
        <div class="search-box">
            <input type="text" id="search" placeholder="Zoek in transcripties..." onkeyup="search(this.value)">
        </div>

        <div class="episodes" id="episodes">
            {% for ep in episodes %}
            <div class="episode-card">
                <div class="episode-header">
                    <h2>{{ ep.title }}</h2>
                    <div class="episode-meta">
                        {{ ep.date }} | {{ ep.duration }} minuten |
                        {% if ep.is_summarized %}
                        <span style="color: #4caf50;">✓ Samenvatting beschikbaar</span>
                        {% else %}
                        <span style="color: #f44336;">✗ Nog niet verwerkt</span>
                        {% endif %}
                    </div>
                </div>
                {% if ep.summary %}
                <div class="episode-content">
                    <div class="episode-summary">
                        <h3>Samenvatting</h3>
                        <p>{{ ep.summary.executive_summary }}</p>
                    </div>

                    <div class="tags">
                        {% for tag in ep.tags[:10] %}
                        <span class="tag {{ tag.category }}">{{ tag.name }}</span>
                        {% endfor %}
                    </div>

                    <button class="expand-btn" onclick="toggleDetails({{ ep.id }})">
                        Toon volledige samenvatting
                    </button>

                    <div id="details-{{ ep.id }}" class="hidden" style="margin-top: 20px;">
                        {% if ep.summary.key_takeaways %}
                        <div class="section">
                            <h4>Key Takeaways</h4>
                            <p>{{ ep.summary.key_takeaways }}</p>
                        </div>
                        {% endif %}

                        {% if ep.summary.models_and_research %}
                        <div class="section">
                            <h4>Models & Research</h4>
                            <p>{{ ep.summary.models_and_research }}</p>
                        </div>
                        {% endif %}

                        {% if ep.summary.tooling %}
                        <div class="section">
                            <h4>Tooling</h4>
                            <p>{{ ep.summary.tooling }}</p>
                        </div>
                        {% endif %}

                        {% if ep.summary.business_applications %}
                        <div class="section">
                            <h4>Business Applications</h4>
                            <p>{{ ep.summary.business_applications }}</p>
                        </div>
                        {% endif %}

                        {% if ep.summary.policy_and_ethics %}
                        <div class="section">
                            <h4>Policy & Ethics</h4>
                            <p>{{ ep.summary.policy_and_ethics }}</p>
                        </div>
                        {% endif %}

                        {% if ep.summary.industry_news %}
                        <div class="section">
                            <h4>Industry News</h4>
                            <p>{{ ep.summary.industry_news }}</p>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% endif %}
            </div>
            {% endfor %}
        </div>

        {% if costs %}
        <div class="costs">
            <h3>Kosten Overzicht</h3>
            <p>Totaal verwerkte afleveringen: {{ costs.episode_count }}</p>
            <p>Transcriptie kosten: ${{ "%.4f"|format(costs.total_transcription_cost) }}</p>
            <p>Samenvatting kosten: ${{ "%.4f"|format(costs.total_summarization_cost) }}</p>
            <p><strong>Totale kosten: ${{ "%.4f"|format(costs.total_cost) }}</strong></p>
        </div>
        {% endif %}
    </div>

    <footer>
        <p>AI Podcast Processor | RSS: api.substack.com/feed/podcast/2351791.rss</p>
    </footer>

    <script>
        function toggleDetails(id) {
            const details = document.getElementById('details-' + id);
            details.classList.toggle('hidden');
        }

        async function search(query) {
            if (query.length < 2) {
                location.reload();
                return;
            }

            const response = await fetch('/search?q=' + encodeURIComponent(query));
            const data = await response.json();

            // Update UI with search results
            console.log('Search results:', data);
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main page showing episodes and summaries."""
    global db
    if not db:
        db = get_db(config.database.sqlite_path)

    episodes = db.get_latest_episodes(limit=50)
    costs = db.get_total_costs()

    # Enrich episodes with summaries and tags
    enriched = []
    for ep in episodes:
        summary = db.get_summary(ep.id) if ep.is_summarized else None
        tags_data = db.get_episode_tags(ep.id) if ep.is_summarized else []

        tags = [{'name': t.name, 'category': t.category or 'topic'} for t, _ in tags_data]

        enriched.append({
            'id': ep.id,
            'title': ep.title,
            'date': ep.published_at.strftime('%Y-%m-%d') if ep.published_at else 'Unknown',
            'duration': ep.duration_seconds // 60 if ep.duration_seconds else 0,
            'is_summarized': ep.is_summarized,
            'summary': summary,
            'tags': tags
        })

    return render_template_string(HTML_TEMPLATE, episodes=enriched, costs=costs)


@app.route('/search')
def search():
    """Search transcripts endpoint."""
    global db
    if not db:
        db = get_db(config.database.sqlite_path)

    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify([])

    results = db.search_transcripts(query, limit=10)
    return jsonify([
        {
            'id': ep.id,
            'title': ep.title,
            'date': ep.published_at.strftime('%Y-%m-%d') if ep.published_at else 'Unknown',
            'snippet': snippet
        }
        for ep, snippet in results
    ])


@app.route('/episode/<int:episode_id>')
def episode_detail(episode_id):
    """Get episode details as JSON."""
    global db
    if not db:
        db = get_db(config.database.sqlite_path)

    episode = db.get_episode(episode_id)
    if not episode:
        return jsonify({'error': 'Episode not found'}), 404

    summary = db.get_summary(episode_id)
    tags = db.get_episode_tags(episode_id)
    transcript = db.get_transcript(episode_id)

    return jsonify({
        'id': episode.id,
        'title': episode.title,
        'date': episode.published_at.isoformat() if episode.published_at else None,
        'duration_seconds': episode.duration_seconds,
        'summary': {
            'executive_summary': summary.executive_summary if summary else None,
            'key_takeaways': summary.key_takeaways if summary else None,
            'models_and_research': summary.models_and_research if summary else None,
            'tooling': summary.tooling if summary else None,
            'business_applications': summary.business_applications if summary else None,
            'policy_and_ethics': summary.policy_and_ethics if summary else None,
            'industry_news': summary.industry_news if summary else None,
        } if summary else None,
        'tags': [{'name': t.name, 'category': t.category, 'relevance': score}
                 for t, score in tags],
        'has_transcript': transcript is not None,
        'word_count': transcript.word_count if transcript else 0
    })


if __name__ == '__main__':
    print("Starting AI Podcast Processor Web UI...")
    print("Open http://localhost:5000 in your browser")

    # Ensure data directory exists
    config.storage.ensure_dirs()

    app.run(debug=config.debug, port=5000)
