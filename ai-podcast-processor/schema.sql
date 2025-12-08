-- AI Podcast Processor - Database Schema
-- SQLite/PostgreSQL compatible

-- Podcast metadata table
CREATE TABLE IF NOT EXISTS podcasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    rss_feed_url TEXT UNIQUE NOT NULL,
    website_url TEXT,
    language TEXT DEFAULT 'nl',
    author TEXT,
    image_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Episodes table
CREATE TABLE IF NOT EXISTS episodes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    podcast_id INTEGER NOT NULL,
    guid TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    published_at TIMESTAMP,
    duration_seconds INTEGER,
    audio_url TEXT NOT NULL,
    audio_size_bytes INTEGER,
    audio_type TEXT DEFAULT 'audio/mpeg',
    episode_url TEXT,

    -- Processing status
    is_downloaded BOOLEAN DEFAULT FALSE,
    is_transcribed BOOLEAN DEFAULT FALSE,
    is_summarized BOOLEAN DEFAULT FALSE,

    -- File paths
    audio_file_path TEXT,
    transcript_file_path TEXT,
    summary_file_path TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (podcast_id) REFERENCES podcasts(id) ON DELETE CASCADE
);

-- Transcripts table
CREATE TABLE IF NOT EXISTS transcripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER UNIQUE NOT NULL,
    full_text TEXT NOT NULL,
    transcription_service TEXT NOT NULL, -- 'whisper' or 'assemblyai'
    language_detected TEXT,
    confidence_score REAL,
    word_count INTEGER,

    -- Cost tracking
    audio_duration_seconds INTEGER,
    cost_usd REAL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
);

-- Transcript segments with timestamps
CREATE TABLE IF NOT EXISTS transcript_segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transcript_id INTEGER NOT NULL,
    segment_index INTEGER NOT NULL,
    start_time_ms INTEGER NOT NULL,
    end_time_ms INTEGER NOT NULL,
    text TEXT NOT NULL,
    speaker TEXT, -- For speaker diarization
    confidence REAL,

    FOREIGN KEY (transcript_id) REFERENCES transcripts(id) ON DELETE CASCADE
);

-- Speakers table (for episodes with multiple speakers)
CREATE TABLE IF NOT EXISTS speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER NOT NULL,
    speaker_label TEXT NOT NULL, -- e.g., "SPEAKER_00", "Alexander Klöpping"
    display_name TEXT, -- Human-readable name if identified
    speaking_time_seconds INTEGER,
    word_count INTEGER,

    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    UNIQUE(episode_id, speaker_label)
);

-- Summaries table
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER UNIQUE NOT NULL,

    -- Main summary sections
    executive_summary TEXT,
    models_and_research TEXT,
    tooling TEXT,
    business_applications TEXT,
    policy_and_ethics TEXT,
    industry_news TEXT,
    key_takeaways TEXT,

    -- Full structured summary as JSON
    full_summary_json TEXT,

    -- Cost tracking
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd REAL,
    model_used TEXT DEFAULT 'claude-sonnet-4-20250514',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
);

-- Tags table
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT, -- 'topic', 'company', 'technology', 'person'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Episode-Tag relationship (many-to-many)
CREATE TABLE IF NOT EXISTS episode_tags (
    episode_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    relevance_score REAL DEFAULT 1.0, -- 0.0 to 1.0

    PRIMARY KEY (episode_id, tag_id),
    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Processing log for tracking costs and errors
CREATE TABLE IF NOT EXISTS processing_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    episode_id INTEGER NOT NULL,
    step TEXT NOT NULL, -- 'download', 'transcribe', 'summarize'
    status TEXT NOT NULL, -- 'started', 'completed', 'failed'
    error_message TEXT,
    duration_seconds REAL,
    cost_usd REAL,
    metadata_json TEXT, -- Additional metadata as JSON
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (episode_id) REFERENCES episodes(id) ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_episodes_podcast_id ON episodes(podcast_id);
CREATE INDEX IF NOT EXISTS idx_episodes_published_at ON episodes(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_episodes_guid ON episodes(guid);
CREATE INDEX IF NOT EXISTS idx_transcript_segments_transcript_id ON transcript_segments(transcript_id);
CREATE INDEX IF NOT EXISTS idx_episode_tags_episode_id ON episode_tags(episode_id);
CREATE INDEX IF NOT EXISTS idx_episode_tags_tag_id ON episode_tags(tag_id);
CREATE INDEX IF NOT EXISTS idx_processing_log_episode_id ON processing_log(episode_id);

-- Default podcast entry for AI Report
INSERT OR IGNORE INTO podcasts (title, description, rss_feed_url, website_url, language, author)
VALUES (
    'AI Report',
    'Alexander Klöpping en Wietse Hage maken AI begrijpelijk en houden je up-to-date. Eén keer per week bespreken ze niet alleen de laatste ontwikkelingen, maar vertalen ze ook grote AI-doorbraken naar praktische toepassingen.',
    'https://api.substack.com/feed/podcast/2351791.rss',
    'https://www.aireport.email',
    'nl',
    'Alexander Klöpping en Wietse Hage'
);

-- Pre-populate common AI tags
INSERT OR IGNORE INTO tags (name, category) VALUES
    ('LLMs', 'technology'),
    ('GPT', 'technology'),
    ('Claude', 'technology'),
    ('OpenAI', 'company'),
    ('Anthropic', 'company'),
    ('Google', 'company'),
    ('Microsoft', 'company'),
    ('Meta', 'company'),
    ('DeepSeek', 'company'),
    ('Computer Vision', 'technology'),
    ('NLP', 'technology'),
    ('Regulation', 'topic'),
    ('Ethics', 'topic'),
    ('Privacy', 'topic'),
    ('Open Source', 'topic'),
    ('Agents', 'technology'),
    ('RAG', 'technology'),
    ('Fine-tuning', 'technology'),
    ('Embeddings', 'technology'),
    ('Multimodal', 'technology'),
    ('Speech Recognition', 'technology'),
    ('Image Generation', 'technology'),
    ('Video Generation', 'technology'),
    ('Coding Assistants', 'topic'),
    ('Enterprise AI', 'topic'),
    ('Startups', 'topic'),
    ('Research Papers', 'topic'),
    ('Benchmarks', 'topic'),
    ('Hardware', 'technology'),
    ('Training', 'technology');
