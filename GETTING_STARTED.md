# DQDA - Getting Started Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repo-url>
cd dqda

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Demo Analysis

```bash
# Run demo with sample data
python examples/demo_analysis.py
```

This will:
- Load sample founder, market, and tokenomics data
- Run comprehensive DQDA analysis
- Print results to console
- Save detailed results to `analysis_result.json`

### 3. Start API Server

```bash
# Start FastAPI server
python -m src.api.main

# API will be available at http://localhost:8000
# Interactive docs at http://localhost:8000/docs
```

## Core Components

### DQDA Agent (Orchestrator)

The main agent that coordinates all analysis modules:

```python
from src.core.agent import DQDAAgent

# Create agent
agent = DQDAAgent()

# Run comprehensive analysis
result = agent.analyze({
    "name": "Company Name",
    "founder": {...},
    "market": {...},
    "competition": {...},
    "tokenomics": {...},
    "technical": {...}
})

# Access results
print(result.overall_deal_quality_score)
print(result.investment_recommendation)
print(result.executive_summary)
```

### Individual Analyzers

You can also use individual analyzers:

```python
from src.core.analyzers import (
    FounderAnalyzer,
    MarketAnalyzer,
    CompetitionAnalyzer,
    TokenomicsAnalyzer,
    TechnicalAnalyzer,
    InvestorFitAnalyzer,
)

# Founder analysis
founder_analyzer = FounderAnalyzer()
founder_result = founder_analyzer.analyze({
    "name": "Jane Founder",
    "previous_experience": [...],
    "team_composition": [...]
})

# Market analysis
market_analyzer = MarketAnalyzer()
market_result = market_analyzer.analyze({
    "total_addressable_market": 500_000_000,
    "growth_rate": 45,
    ...
})
```

## Input Data Structure

### Founder Data

```python
founder_data = {
    "name": str,
    "background": str,
    "previous_experience": [
        {
            "company": str,
            "role": str,
            "years": int,
            "domain": str
        }
    ],
    "previous_exits": [
        {
            "company": str,
            "outcome": str,
            "exit_value": int
        }
    ],
    "team_composition": [
        {
            "name": str,
            "role_type": str,  # "technical", "business", "product", "operations"
            "background": str,
            "previous_experience": [...]
        }
    ],
    "domain_expertise": str,  # "High", "Medium", "Low"
    "achievements": [str]
}
```

### Market Data

```python
market_data = {
    "target_market": str,
    "total_addressable_market": float,
    "serviceable_addressable_market": float,
    "serviceable_obtainable_market": float,
    "market_stage": str,  # "emerging", "growing", "mature"
    "growth_rate": float,  # percentage
    "target_segments": [str],
    "market_trends": [str],
    "regulatory_environment": str
}
```

### Competition Data

```python
competition_data = {
    "company_name": str,
    "competitive_advantage": str,
    "unique_positioning": str,
    "direct_competitors": [
        {
            "name": str,
            "positioning": str,
            "strengths": [str],
            "weaknesses": [str],
            "funding_stage": str,
            "market_share": float
        }
    ],
    "indirect_competitors": [...],
    "potential_new_entrants": [str],
    "competitive_advantage_defensibility": str
}
```

### Tokenomics Data

```python
tokenomics_data = {
    "token_name": str,
    "ticker": str,
    "total_supply": float,
    "circulating_supply": float,
    "max_supply": float,
    "utility_description": str,
    "is_governance_token": bool,
    "is_fee_token": bool,
    "distribution": [
        {
            "recipient": str,
            "percentage": float,
            "vesting_months": int,
            "lock_months": int
        }
    ],
    "team_allocation": float,
    "investor_allocation": float,
    "community_allocation": float,
    "vesting_schedule": dict
}
```

### Technical Assessment Data

```python
technical_data = {
    "product_stage": str,  # "idea", "alpha", "beta", "launched"
    "product_market_fit": bool,
    "technology_stack": [str],
    "scalability_concerns": [str],
    "security_concerns": [str],
    "technical_assessment": {
        "architecture_assessment": str,
        "has_automated_testing": bool,
        "documentation_exists": bool
    },
    "gtm_clarity": str,
    "customer_acquisition": str,
    "market_messaging": str,
    "competitive_positioning": str,
    "revenue_model": str,
    "customer_validation": bool,
    "pitch_deck_quality": str
}
```

## API Endpoints

### Health Check

```
GET /health

Response:
{
    "status": "ok",
    "version": "0.1.0"
}
```

### Single Analysis

```
POST /analyze

Request Body:
{
    "name": "Company Name",
    "founder": {...},
    "market": {...},
    "competition": {...},
    "tokenomics": {...},
    "technical": {...}
}

Response: Complete AnalysisResult object
```

### Batch Analysis

```
POST /analyze-batch

Request Body: Array of analysis requests

Response:
{
    "successful": int,
    "failed": int,
    "results": [...],
    "errors": [...]
}
```

## Output Format

All analyses return a structured `AnalysisResult` with:

- **overall_deal_quality_score** (0-100): Composite quality score
- **investment_recommendation**: Go/Pass decision
- **founder_readiness**: Founder analysis with component scores
- **market_analysis**: Market opportunity assessment
- **competition_analysis**: Competitive landscape analysis
- **token_utility_analysis**: Tokenomics evaluation
- **weakness_analysis**: Technical and narrative weaknesses
- **investor_fit**: Fit predictions for investor types
- **executive_summary**: 2-3 paragraph summary
- **key_strengths**: Top deal strengths
- **key_concerns**: Key issues to address

## Scoring Guide

### Overall Deal Quality Score

- **80-100**: Strong Pass - Excellent deal quality
- **70-79**: Pass - Good fundamentals
- **60-69**: Borderline - Address key concerns
- **50-59**: Weak Pass - Significant work needed
- **0-49**: Pass - Do not advance

### Component Scores

Each component is scored 0-100 and weighted into overall score:

- Founder Readiness (25% weight)
- Market Analysis (25% weight)
- Competition (15% weight)
- Tokenomics (15% weight)
- Weaknesses (15% weight, negative)
- Investor Fit (5% weight)

## Configuration

Configuration is loaded from `config/settings.yaml`:

```yaml
analysis:
  founder_weight: 0.25
  market_weight: 0.25
  # ... other weights

scoring:
  excellent_threshold: 80
  good_threshold: 65
  # ... other thresholds
```

## Testing

Run unit tests:

```bash
python tests/test_analyzers.py
```

## Extending DQDA

### Adding a New Analyzer

1. Create new analyzer in `src/core/analyzers/new_analyzer.py`
2. Inherit from base analyzer pattern
3. Implement `analyze()` method
4. Add to `src/core/analyzers/__init__.py`
5. Integrate into `DQDAAgent.analyze()`

### Adding LLM Provider Integration

1. Create provider in `src/core/llm/provider_name.py`
2. Implement LLM interface
3. Update config to specify provider
4. Pass to analyzer constructors

## Troubleshooting

### ImportError when running demo

Make sure you're in the project root directory:
```bash
cd /path/to/dqda
python examples/demo_analysis.py
```

### Module not found errors

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API server won't start

Check if port 8000 is available:
```bash
# Use different port
python -m src.api.main --port 8001
```

## Next Steps

1. **Integrate document extractors** for PDF pitch decks and whitepapers
2. **Add LLM providers** (OpenAI, Anthropic, etc.) for enhanced analysis
3. **Build web UI** for dashboard and reporting
4. **Create investor database** for better fit matching
5. **Implement historical analysis** tracking for performance monitoring

## Documentation

- **Architecture**: See code structure in README.md
- **API Documentation**: Start API server and visit `/docs`
- **Configuration**: Edit `config/settings.yaml`
- **Examples**: See `examples/` directory

## Support

For issues or questions, refer to the repository README and example files.
