"""Claude API-based summarization for podcast transcripts."""

import json
import logging
import time
from dataclasses import dataclass, field
from typing import Optional

import anthropic

logger = logging.getLogger(__name__)


@dataclass
class SummaryResult:
    """Result of podcast summarization."""
    success: bool

    # Structured sections
    executive_summary: str = ""
    models_and_research: str = ""
    tooling: str = ""
    business_applications: str = ""
    policy_and_ethics: str = ""
    industry_news: str = ""
    key_takeaways: str = ""

    # Tags extracted
    tags: list[tuple[str, float, str]] = field(default_factory=list)  # (name, relevance, category)

    # Full JSON response
    full_response: dict = field(default_factory=dict)

    # Cost tracking
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0
    model_used: str = ""

    error: Optional[str] = None

    def to_markdown(self) -> str:
        """Convert summary to markdown format."""
        sections = []

        sections.append(f"# Podcast Samenvatting\n")

        if self.executive_summary:
            sections.append(f"## Samenvatting\n\n{self.executive_summary}\n")

        if self.models_and_research:
            sections.append(f"## Models & Research\n\n{self.models_and_research}\n")

        if self.tooling:
            sections.append(f"## Tooling\n\n{self.tooling}\n")

        if self.business_applications:
            sections.append(f"## Business Applications\n\n{self.business_applications}\n")

        if self.policy_and_ethics:
            sections.append(f"## Policy & Ethics\n\n{self.policy_and_ethics}\n")

        if self.industry_news:
            sections.append(f"## Industry News\n\n{self.industry_news}\n")

        if self.key_takeaways:
            sections.append(f"## Key Takeaways\n\n{self.key_takeaways}\n")

        if self.tags:
            tag_list = ", ".join([f"`{tag[0]}`" for tag in self.tags[:15]])
            sections.append(f"## Tags\n\n{tag_list}\n")

        # Add cost info
        sections.append(f"\n---\n*Tokens: {self.input_tokens} in / {self.output_tokens} out | Cost: ${self.cost_usd:.4f} | Model: {self.model_used}*")

        return "\n".join(sections)


class ClaudeSummarizer:
    """Generate structured summaries using Claude API."""

    # Claude pricing per 1M tokens
    PRICING = {
        "claude-sonnet-4-20250514": {"input": 3.0, "output": 15.0},
        "claude-3-5-sonnet-20241022": {"input": 3.0, "output": 15.0},
        "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},
        "claude-3-opus-20240229": {"input": 15.0, "output": 75.0},
    }

    SYSTEM_PROMPT = """Je bent een expert AI-analist die gespecialiseerd is in het analyseren van de AI Report podcast - een Nederlandse podcast over kunstmatige intelligentie gepresenteerd door Alexander Klöpping en Wietse Hage.

Je taak is om podcast transcripties te analyseren en gestructureerde samenvattingen te maken die waardevol zijn voor AI-professionals, developers en business leads.

Je output moet in het Nederlands zijn, maar technische termen mogen in het Engels blijven."""

    SUMMARY_PROMPT = """Analyseer het volgende podcast transcript en maak een uitgebreide, gestructureerde samenvatting.

## Transcript:
{transcript}

## Episode Info:
- Titel: {title}
- Datum: {date}
- Duur: {duration}

---

Maak een gedetailleerde analyse met de volgende secties. Elke sectie moet concrete informatie bevatten - geen algemeenheden. Als een sectie niet relevant is voor deze aflevering, geef dan "Niet besproken in deze aflevering" aan.

Geef je response als JSON met exact deze structuur:

```json
{{
    "executive_summary": "Een beknopte samenvatting (3-4 zinnen) van de belangrijkste punten uit deze aflevering. Focus op de meest impactvolle nieuws en inzichten.",

    "models_and_research": "Bespreek alle AI-modellen, papers, benchmarks en technische doorbraken die genoemd werden. Noem specifieke namen, cijfers en wat dit betekent voor de praktijk. Gebruik bullet points voor elk item.",

    "tooling": "Nieuwe tools, frameworks, APIs, of developer resources die besproken werden. Wat doen ze? Waarom zijn ze relevant? Gebruik bullet points.",

    "business_applications": "Concrete business use cases, bedrijfsstrategieën, of marktbewegingen in de AI-sector. Welke bedrijven werden genoemd? Wat zijn de implicaties?",

    "policy_and_ethics": "Regelgeving, ethische discussies, privacy-concerns, of maatschappelijke impact die aan bod kwamen.",

    "industry_news": "Overig AI-nieuws: fusies, financiering, personeelswisselingen, product launches, of andere relevante ontwikkelingen.",

    "key_takeaways": "De 3-5 belangrijkste concrete actiepunten of inzichten voor luisteraars. Wat kunnen developers, product managers, of business leaders NU doen met deze informatie?",

    "tags": [
        {{"name": "tag_naam", "relevance": 0.9, "category": "technology|company|topic|person"}},
        ...
    ]
}}
```

## Tag categorieën:
- **technology**: AI-technologieën, frameworks, technieken (bijv. LLMs, RAG, fine-tuning, computer vision)
- **company**: Bedrijven (bijv. OpenAI, Anthropic, Google, Microsoft, startups)
- **topic**: Thema's (bijv. regulation, ethics, open source, enterprise AI)
- **person**: Personen die besproken worden

Geef 10-20 relevante tags met een relevance score (0.0-1.0) die aangeeft hoe centraal het onderwerp was in de aflevering.

Wees specifiek en concreet. Noem namen, cijfers, en datums waar mogelijk. Vermijd vage uitspraken."""

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 8192
    ):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def summarize(
        self,
        transcript: str,
        title: str = "",
        date: str = "",
        duration: str = ""
    ) -> SummaryResult:
        """
        Generate structured summary of podcast transcript.

        Args:
            transcript: Full transcript text
            title: Episode title
            date: Publication date
            duration: Episode duration

        Returns:
            SummaryResult with structured summary
        """
        logger.info(f"Summarizing transcript ({len(transcript)} chars) with {self.model}")
        start_time = time.time()

        # Truncate transcript if too long (Claude can handle ~100k tokens)
        max_chars = 300000  # ~75k tokens
        if len(transcript) > max_chars:
            logger.warning(f"Truncating transcript from {len(transcript)} to {max_chars} chars")
            transcript = transcript[:max_chars] + "\n\n[TRANSCRIPT TRUNCATED]"

        prompt = self.SUMMARY_PROMPT.format(
            transcript=transcript,
            title=title or "Onbekend",
            date=date or "Onbekend",
            duration=duration or "Onbekend"
        )

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=self.SYSTEM_PROMPT,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            duration = time.time() - start_time
            logger.info(f"Summarization completed in {duration:.1f}s")

            # Parse response
            content = response.content[0].text

            # Extract JSON from response
            json_str = self._extract_json(content)
            if not json_str:
                return SummaryResult(
                    success=False,
                    error="Could not parse JSON from response",
                    input_tokens=response.usage.input_tokens,
                    output_tokens=response.usage.output_tokens,
                    model_used=self.model
                )

            data = json.loads(json_str)

            # Calculate cost
            cost = self._calculate_cost(
                response.usage.input_tokens,
                response.usage.output_tokens
            )

            # Parse tags
            tags = []
            for tag in data.get("tags", []):
                if isinstance(tag, dict):
                    tags.append((
                        tag.get("name", ""),
                        tag.get("relevance", 0.5),
                        tag.get("category", "topic")
                    ))

            return SummaryResult(
                success=True,
                executive_summary=data.get("executive_summary", ""),
                models_and_research=data.get("models_and_research", ""),
                tooling=data.get("tooling", ""),
                business_applications=data.get("business_applications", ""),
                policy_and_ethics=data.get("policy_and_ethics", ""),
                industry_news=data.get("industry_news", ""),
                key_takeaways=data.get("key_takeaways", ""),
                tags=tags,
                full_response=data,
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                cost_usd=cost,
                model_used=self.model
            )

        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            return SummaryResult(
                success=False,
                error=f"JSON parsing error: {e}",
                model_used=self.model
            )
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return SummaryResult(
                success=False,
                error=str(e),
                model_used=self.model
            )

    def _extract_json(self, text: str) -> Optional[str]:
        """Extract JSON from response text."""
        # Try to find JSON block
        import re

        # Look for ```json ... ``` block
        json_match = re.search(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', text)
        if json_match:
            return json_match.group(1)

        # Try to find raw JSON object
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            return json_match.group(0)

        return None

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost based on token usage."""
        pricing = self.PRICING.get(self.model, {"input": 3.0, "output": 15.0})
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost

    def estimate_cost(self, transcript_length: int) -> float:
        """Estimate cost for summarizing transcript of given length."""
        # Rough estimate: 4 chars per token for input
        estimated_input_tokens = transcript_length // 4 + 2000  # Add prompt overhead
        # Estimate ~4000 tokens for output
        estimated_output_tokens = 4000

        return self._calculate_cost(estimated_input_tokens, estimated_output_tokens)

    def generate_trending_analysis(
        self,
        summaries: list[dict],
        weeks: int = 4
    ) -> str:
        """
        Generate trending topics analysis across multiple episodes.

        Args:
            summaries: List of summary dicts with tags
            weeks: Number of weeks to analyze

        Returns:
            Markdown analysis of trends
        """
        prompt = f"""Analyseer de volgende samenvattingen van de laatste {weeks} weken AI Report podcasts en identificeer trends:

{json.dumps(summaries, indent=2, ensure_ascii=False)}

Maak een analyse met:
1. **Opkomende trends**: Onderwerpen die vaker worden besproken
2. **Belangrijkste bedrijven**: Welke bedrijven domineren het nieuws
3. **Technologie focus**: Welke AI-technologieën zijn het meest besproken
4. **Veranderingen**: Wat is anders dan vorige periodes

Geef concrete voorbeelden en refereer naar specifieke afleveringen waar relevant."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Trend analysis failed: {e}")
            return f"Trend analyse mislukt: {e}"
