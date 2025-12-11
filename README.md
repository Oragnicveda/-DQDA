# DQDA - Deal Qualification & Due Diligence Agent

A comprehensive AI-powered system for qualifying founders and evaluating deals before investor introductions.

## Overview

DQDA is a multi-module analysis system that reads pitch decks, tokenomics, whitepapers, and websites to generate actionable intelligence on:

- **Founder Readiness Score** - Experience, track record, execution capability
- **Market Size Analysis** - TAM/SAM/SOM sizing and market opportunity
- **Competition Mapping** - Competitive landscape and differentiation
- **Token Utility Analysis** - Tokenomics validation and utility assessment
- **Technical Weaknesses** - Architecture, tech debt, scalability issues
- **Narrative Weaknesses** - GTM gaps, positioning, messaging problems
- **Investor-Fit Prediction** - Likelihood of closing with specific investor types

## Architecture

```
DQDA/
├── src/
│   ├── core/
│   │   ├── agent.py              # Main orchestrator
│   │   ├── analyzers/            # Analysis modules
│   │   │   ├── founder.py
│   │   │   ├── market.py
│   │   │   ├── competition.py
│   │   │   ├── tokenomics.py
│   │   │   ├── technical.py
│   │   │   └── investor_fit.py
│   │   ├── models/               # Data models
│   │   │   ├── schemas.py
│   │   │   └── enums.py
│   │   ├── extractors/           # Document extraction
│   │   │   ├── pitch_deck.py
│   │   │   ├── whitepaper.py
│   │   │   ├── tokenomics.py
│   │   │   └── website.py
│   │   ├── llm/                  # LLM integrations
│   │   │   ├── base.py
│   │   │   ├── openai.py
│   │   │   └── prompts.py
│   │   └── utils/
│   │       ├── formatting.py
│   │       ├── logging.py
│   │       └── config.py
│   └── api/
│       ├── routes.py             # API endpoints
│       └── main.py               # FastAPI app
├── tests/
│   ├── test_analyzers.py
│   ├── test_extractors.py
│   └── fixtures/
├── examples/
│   ├── demo_analysis.py
│   └── sample_data/
├── config/
│   ├── settings.yaml
│   └── prompts/
├── requirements.txt
└── README.md
```

## Key Features

- **Multi-Source Analysis** - Integrates data from pitch decks, tokenomics, whitepapers, websites
- **Scoring System** - Quantitative and qualitative scoring for all dimensions
- **Weakness Identification** - Automated detection of red flags and gaps
- **Investor Matching** - Predicts fit with different investor types/theses
- **Extensible Design** - Easy to add new analyzers and data sources

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### As a Python Module

```python
from src.core.agent import DQDAAgent

agent = DQDAAgent()
result = agent.analyze(
    pitch_deck_path="path/to/deck.pdf",
    whitepaper_path="path/to/whitepaper.pdf",
    website_url="https://example.com",
    tokenomics_data={...}
)

print(result.founder_readiness_score)
print(result.market_analysis)
print(result.competition_analysis)
print(result.token_utility_analysis)
print(result.technical_weaknesses)
print(result.narrative_weaknesses)
print(result.investor_fit_predictions)
```

### As an API

```bash
python -m src.api.main
```

Then POST to `/analyze` with analysis parameters.

## Output Format

All analyses return structured data with:
- **Score** (0-100): Quantitative assessment
- **Summary**: Executive summary
- **Details**: Detailed findings
- **Weaknesses**: Key issues identified
- **Recommendations**: Suggested improvements

## Investor Types

- Growth Stage VCs
- Seed Stage VCs
- Crypto/Web3 Specialists
- Strategic Corporates
- Angel Investors
- Token Funds
