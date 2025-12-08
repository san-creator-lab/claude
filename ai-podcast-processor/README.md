# AI Podcast Processor

Automatische verwerking van de **AI Report** podcast van Alexander Klöpping en Wietse Hage. Deze applicatie haalt wekelijks nieuwe afleveringen op, transcribeert de audio, en genereert uitgebreide samenvattingen met Claude AI.

## Features

- **Automatische RSS feed monitoring** - Wekelijkse check op nieuwe afleveringen
- **Audio download** - Download podcast audio met retry-mechanisme
- **Transcriptie** - Keuze tussen OpenAI Whisper of AssemblyAI (met speaker diarization)
- **AI Samenvatting** - Gestructureerde samenvattingen via Claude API
- **Tagging** - Automatische tagging van afleveringen (LLMs, OpenAI, Ethics, etc.)
- **Kosten tracking** - Monitoring van API kosten per aflevering
- **Zoeken** - Full-text zoeken in transcripties
- **CLI interface** - Makkelijke command-line tools

## Quick Start

### 1. Installatie

```bash
# Clone of download de repository
cd ai-podcast-processor

# Maak virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# of: venv\Scripts\activate  # Windows

# Installeer dependencies
pip install -r requirements.txt
```

### 2. Configuratie

```bash
# Kopieer environment template
cp .env.example .env

# Vul je API keys in
nano .env  # of open in je editor
```

**Minimale configuratie:**
```env
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```

### 3. Test run

```bash
# Check voor nieuwe afleveringen
python main.py check

# Bekijk lijst van afleveringen
python main.py list

# Verwerk één aflevering
python main.py process --episode-id 1
```

## CLI Commando's

```bash
# Check voor nieuwe afleveringen (voegt toe aan database)
python main.py check

# Verwerk alle onverwerkte afleveringen
python main.py process

# Verwerk specifieke aflevering
python main.py process --episode-id 5

# Bekijk afleveringen
python main.py list
python main.py list --limit 50

# Bekijk samenvatting
python main.py summary 5
python main.py summary 5 --format markdown

# Zoek in transcripties
python main.py search "Claude" --limit 10

# Bekijk kosten rapport
python main.py costs

# Start scheduler (draait continu)
python main.py run

# Backfill historische afleveringen
python main.py backfill --limit 5
```

## Projectstructuur

```
ai-podcast-processor/
├── main.py                 # CLI entry point
├── config.py              # Configuratie management
├── schema.sql             # Database schema
├── requirements.txt       # Python dependencies
├── .env.example          # Environment template
│
├── src/
│   ├── database/         # Database models en operaties
│   │   ├── db.py        # SQLite/PostgreSQL connection
│   │   └── models.py    # Data models
│   │
│   ├── fetcher/          # RSS parsing en audio download
│   │   ├── rss_parser.py
│   │   └── downloader.py
│   │
│   ├── transcriber/      # Transcriptie services
│   │   ├── whisper.py   # OpenAI Whisper
│   │   ├── assemblyai.py # AssemblyAI (speaker diarization)
│   │   └── factory.py   # Service selection
│   │
│   ├── summarizer/       # Claude samenvatting
│   │   └── claude_summarizer.py
│   │
│   ├── processor.py      # Main processing pipeline
│   └── scheduler.py      # APScheduler wrapper
│
├── data/                  # Data directory (auto-generated)
│   ├── podcast.db        # SQLite database
│   ├── audio/            # Downloaded audio files
│   ├── transcripts/      # Transcript files
│   └── summaries/        # Markdown summaries
│
└── scripts/
    └── test_rss_feed.py  # Test RSS parsing
```

## Samenvatting Structuur

Elke aflevering krijgt een gestructureerde samenvatting met:

- **Executive Summary** - Beknopte samenvatting (3-4 zinnen)
- **Models & Research** - AI modellen, papers, benchmarks
- **Tooling** - Tools, frameworks, APIs
- **Business Applications** - Use cases, marktbewegingen
- **Policy & Ethics** - Regelgeving, ethische discussies
- **Industry News** - Overig nieuws uit de AI-sector
- **Key Takeaways** - Concrete actiepunten

## Kosten Indicatie

Per aflevering (~45 minuten audio):

| Service | Functie | Geschatte kosten |
|---------|---------|------------------|
| OpenAI Whisper | Transcriptie | ~$0.27 |
| AssemblyAI | Transcriptie + speakers | ~$0.28 |
| Claude Sonnet | Samenvatting | ~$0.05-0.10 |
| **Totaal** | | **~$0.35** per aflevering |

## Database Schema

De applicatie gebruikt SQLite (of PostgreSQL) met de volgende tabellen:

- `podcasts` - Podcast metadata
- `episodes` - Afleveringen met processing status
- `transcripts` - Volledige transcripties
- `transcript_segments` - Segmenten met timestamps
- `speakers` - Speaker informatie (bij diarization)
- `summaries` - Gestructureerde samenvattingen
- `tags` - Content tags
- `episode_tags` - Aflevering-tag relaties
- `processing_log` - Processing history en kosten

## Transcriptie Services

### OpenAI Whisper (standaard)
- Sneller en goedkoper
- Goede kwaliteit voor Nederlands
- Geen speaker diarization

### AssemblyAI (alternatief)
- Speaker diarization (wie zegt wat)
- Betere punctuatie
- Entity detection

Switch in `.env`:
```env
TRANSCRIPTION_SERVICE=assemblyai
ASSEMBLYAI_API_KEY=your-key
```

## Scheduler

De scheduler draait standaard elke maandag om 8:00:

```bash
# Start scheduler
python main.py run

# Of configureer andere timing in .env:
CRON_EXPRESSION=0 8 * * MON  # Maandag 8:00
CHECK_INTERVAL_HOURS=24       # Of elke 24 uur
```

## Development

```bash
# Run tests
pytest tests/

# Type checking
mypy src/

# Lint
ruff check src/
```

## Troubleshooting

### "No transcript available"
De aflevering is nog niet getranscribeerd. Run:
```bash
python main.py process --episode-id <ID>
```

### API rate limits
Bij rate limits wacht de applicatie automatisch. Voor bulk processing, gebruik:
```bash
python main.py backfill --limit 3  # Verwerk 3 afleveringen
```

### Audio download faalt
Check je internetverbinding. De downloader probeert 3x met exponential backoff.

## RSS Feed

**AI Report Podcast**
- RSS: `https://api.substack.com/feed/podcast/2351791.rss`
- Website: https://www.aireport.email
- Spotify: https://open.spotify.com/show/5Hpc8qDcawOEf4ulCouPau

## License

MIT License - gebruik vrij voor persoonlijke en commerciële projecten.
