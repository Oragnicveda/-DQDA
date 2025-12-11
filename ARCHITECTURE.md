# DQDA Architecture & Design

## System Overview

DQDA (Deal Qualification & Due Diligence Agent) is a modular analysis engine that evaluates startups across multiple dimensions:

```
                          ┌─────────────────────┐
                          │   DQDA Agent        │
                          │  (Orchestrator)     │
                          └──────────┬──────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
    ┌────▼─────┐             ┌──────▼──────┐           ┌────────▼───┐
    │ Founder  │             │   Market    │           │ Competition│
    │ Analyzer │             │  Analyzer   │           │ Analyzer   │
    └────┬─────┘             └──────┬──────┘           └────────┬───┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
    ┌────▼──────────┐       ┌───────▼────────┐       ┌──────────▼──┐
    │ Tokenomics   │       │   Technical    │       │ Investor Fit│
    │ Analyzer     │       │   Analyzer     │       │ Analyzer    │
    └────┬──────────┘       └───────┬────────┘       └──────────┬──┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
                          ┌──────────▼──────────┐
                          │ AnalysisResult      │
                          │ (Structured Output) │
                          └─────────────────────┘
```

## Core Components

### 1. Orchestrator (`src/core/agent.py`)

The main `DQDAAgent` class coordinates all analyzers:

```python
class DQDAAgent:
    def analyze(self, deal_data: Dict[str, Any]) -> AnalysisResult:
        # 1. Founder readiness analysis
        # 2. Market opportunity analysis
        # 3. Competitive landscape analysis
        # 4. Tokenomics evaluation
        # 5. Weakness identification
        # 6. Investor fit prediction
        # 7. Composite scoring and recommendation
        return AnalysisResult(...)
```

**Responsibilities**:
- Load and validate input data
- Invoke all analyzers sequentially
- Aggregate results
- Calculate composite scores
- Generate recommendations
- Create executive summary

### 2. Analyzer Modules

Each analyzer follows the same pattern:

```python
class XYZAnalyzer:
    def __init__(self, llm_provider=None):
        self.llm = llm_provider  # Optional LLM enhancement
    
    def analyze(self, data: Dict[str, Any]) -> XYZResult:
        # Component-specific scoring
        # Pattern recognition
        # Weakness identification
        # Result generation
        return XYZResult(...)
```

#### Founder Analyzer (`src/core/analyzers/founder.py`)

Evaluates founder readiness through:
- **Experience Score** (25% weight)
  - Years in relevant domain
  - Seniority of past roles
  - Domain expertise match
  
- **Track Record Score** (35% weight)
  - Previous exits and outcomes
  - Revenue/growth achievements
  - Demonstrated execution
  
- **Execution Capability** (30% weight)
  - Number of verified achievements
  - Evidence of shipping products
  - Scaling experience
  
- **Team Completeness** (10% weight)
  - Co-founder skills
  - Role diversity
  - Team size

**Output**: FounderReadinessScore (0-100) with component breakdowns

#### Market Analyzer (`src/core/analyzers/market.py`)

Evaluates market opportunity:
- **TAM Sizing** (30% weight)
  - Total addressable market validation
  - SAM/SOM clarity
  - Methodology assessment
  
- **Growth Potential** (35% weight)
  - Market CAGR
  - Stage of market development
  - Trend alignment
  
- **Target Segments** (20% weight)
  - Segment clarity and size
  - Addressability
  
- **Market Trends** (15% weight)
  - Macro tailwinds
  - Regulatory environment

**Output**: MarketAnalysis with TAM estimates and opportunity strength

#### Competition Analyzer (`src/core/analyzers/competition.py`)

Maps competitive landscape:
- **Competitive Advantage** (35% weight)
  - Strength and clarity
  - Defensibility assessment
  - Moat sustainability
  
- **Positioning** (30% weight)
  - Market positioning clarity
  - Differentiation specificity
  
- **Competitive Landscape** (35% weight)
  - Direct competitor count/threat
  - Market consolidation risk
  - New entrant threat

**Output**: CompetitionAnalysis with competitor profiles and threat levels

#### Tokenomics Analyzer (`src/core/analyzers/tokenomics.py`)

Evaluates token design (if applicable):
- **Utility Score** (35% weight)
  - Utility description clarity
  - Multiple use cases
  - Governance and fee capture
  
- **Distribution** (25% weight)
  - Team/investor/community balance
  - Concentration risks
  
- **Vesting** (20% weight)
  - Lock periods
  - Cliff vs linear vesting
  - Founder skin-in-the-game
  
- **Incentive Alignment** (20% weight)
  - Burn mechanisms
  - Deflationary properties
  - Supply control

**Output**: TokenUtilityAnalysis with health classification (Excellent/Good/Acceptable/Poor/Problematic)

#### Technical Analyzer (`src/core/analyzers/technical.py`)

Identifies technical and business weaknesses:

**Technical Weaknesses**:
- Product stage maturity
- Scalability concerns
- Security issues
- Outdated technology
- Testing/QA gaps
- Architecture limitations

**Narrative Weaknesses**:
- GTM clarity
- Customer acquisition economics
- Market messaging
- Competitive positioning
- Revenue model viability
- Customer validation

**Output**: WeaknessAnalysis with severity levels (Critical/High/Medium/Low/Info)

#### Investor Fit Analyzer (`src/core/analyzers/investor_fit.py`)

Predicts fit with 6 investor types:

1. **Growth Stage VCs** - Focus on traction, team, large markets
2. **Seed Stage VCs** - Focus on founders and market opportunity
3. **Crypto Specialists** - Focus on tokenomics and Web3 experience
4. **Strategic Corporates** - Focus on synergy and IP defensibility
5. **Angel Investors** - Focus on founder quality and story
6. **Token Funds** - Focus on token mechanics and community

**Scoring Logic**:
- Weight different factors by investor type
- Identify alignment and misalignment factors
- Provide positioning recommendations

**Output**: InvestorFitPrediction with scores for all types

### 3. Data Models (`src/core/models/`)

#### Schemas (`schemas.py`)

Pydantic models for type-safe data:
- `FounderReadinessScore` - Founder assessment
- `MarketAnalysis` - Market opportunity
- `CompetitionAnalysis` - Competitive landscape
- `TokenUtilityAnalysis` - Token evaluation
- `WeaknessAnalysis` - Issues identified
- `InvestorFitPrediction` - Investor matching
- `AnalysisResult` - Complete analysis output

#### Enumerations (`enums.py`)

Standard enums:
- `InvestorType` - 6 investor types
- `WeaknessLevel` - Severity levels (Critical→Info)
- `MarketStage` - Market development (Emerging→Declining)
- `FounderBackgroundType` - Background categories
- `TokenomicsHealth` - Token health status

### 4. Utilities (`src/core/utils/`)

#### Config (`config.py`)
- Load YAML configuration
- Default configuration fallback
- Extensible settings system

#### Logging (`logging.py`)
- Centralized logging setup
- Console and file handlers
- Structured logging support

### 5. API (`src/api/main.py`)

FastAPI application with endpoints:

```
POST /analyze
- Single deal analysis
- Request: AnalysisRequest
- Response: AnalysisResult

POST /analyze-batch  
- Batch analysis of multiple deals
- Request: List[AnalysisRequest]
- Response: Batch results with errors

GET /health
- Health check endpoint

GET /
- API documentation
```

## Scoring System

### Component Scoring

Each analyzer returns a 0-100 score with:
- Individual component scores
- Weighting system
- Supporting reasoning

### Overall Deal Quality Score

Weighted composite of all components:

```
Overall Score = 
  Founder (25%) +
  Market (25%) +
  Competition (15%) +
  Tokenomics (15%) +
  Weakness Penalty (15%) +
  Investor Fit (5%)
```

**Penalties**:
- Each critical weakness: -15 points
- Each high-severity weakness: -5 points
- Deal-killers: Automatic fail

### Investment Recommendation

```
80-100: "Strong Pass - Excellent deal quality"
70-79:  "Pass - Good fundamentals"
60-69:  "Borderline - Address key concerns"
50-59:  "Weak Pass - Significant work needed"
0-49:   "Pass - Do not advance"
```

## Data Flow

### Input Processing

1. **Validation**: Pydantic validates input structure
2. **Normalization**: Standardize units and formats
3. **Enrichment**: Add derived fields
4. **Distribution**: Pass to individual analyzers

### Analysis Processing

1. **Scoring**: Each analyzer scores components
2. **Identification**: Find weaknesses and risks
3. **Assessment**: Qualitative evaluation
4. **Reasoning**: Generate supporting explanations
5. **Aggregation**: Combine into component result

### Output Generation

1. **Composition**: Combine all analyzer results
2. **Synthesis**: Generate executive summary
3. **Extraction**: Pull key points
4. **Recommendation**: Generate go/no-go
5. **Serialization**: Convert to JSON/API response

## Extensibility

### Adding a New Analyzer

1. **Create module**: `src/core/analyzers/new_analyzer.py`
2. **Implement interface**:
   ```python
   class NewAnalyzer:
       def __init__(self, llm_provider=None):
           pass
       
       def analyze(self, data: Dict) -> NewResult:
           # Scoring logic
           return NewResult(...)
   ```
3. **Define result model**: Add to `schemas.py`
4. **Register**: Add to `DQDAAgent`
5. **Weight**: Configure in `DQDAAgent._calculate_overall_score()`

### Adding LLM Provider

1. **Create provider**: `src/core/llm/provider_name.py`
2. **Implement interface**: 
   ```python
   class LLMProvider:
       def analyze(self, prompt: str) -> str:
           pass
   ```
3. **Pass to analyzers**: `DQDAAgent(llm_provider=provider)`
4. **Use in analysis**: `self.llm.analyze(prompt)` if available

### Adding Document Extractor

1. **Create extractor**: `src/core/extractors/doc_type.py`
2. **Implement parsing**:
   ```python
   class PDFExtractor:
       def extract(self, path: str) -> Dict:
           # Parse and return structured data
           pass
   ```
3. **Integrate with agent**: Add to input processing

## Performance Considerations

### Current Optimizations
- Single-pass analysis (all modules run once)
- No external API calls (unless LLM enabled)
- Pure Python calculations
- Pydantic model caching

### Future Optimizations
- Parallel analyzer execution
- Caching of extracted data
- Batch processing with async
- Streaming responses
- Database persistence

## Testing Strategy

### Unit Tests (`tests/test_analyzers.py`)
- Individual analyzer validation
- Scoring boundary conditions
- Input validation
- Output schema compliance

### Integration Tests (needed)
- End-to-end analysis
- API endpoint validation
- Batch processing
- Error handling

### Performance Tests (needed)
- Large batch processing
- API response times
- Memory usage
- Scaling characteristics

## Security Considerations

### Data Handling
- Input validation (Pydantic)
- No sensitive data persistence
- Rate limiting ready (FastAPI)
- CORS configuration available

### Future Security
- Authentication/authorization
- Data encryption at rest
- Audit logging
- Access controls

## Deployment

### Single Instance
```bash
python -m src.api.main
```

### With Gunicorn
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.main:app
```

### Docker Support (template)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "-m", "src.api.main"]
```

## Configuration

YAML-based configuration in `config/settings.yaml`:
- Analysis weights
- Scoring thresholds
- LLM settings
- Extractor parameters
- Technology lists

## Development Workflow

1. **Add requirement** to `requirements.txt`
2. **Create new analyzer** in `src/core/analyzers/`
3. **Add data model** to `src/core/models/schemas.py`
4. **Integrate into agent** in `src/core/agent.py`
5. **Add tests** in `tests/`
6. **Update documentation**

## Future Enhancements

### Short-term
- [ ] Document extractors (PDF, website)
- [ ] LLM provider integrations
- [ ] Enhanced founder research
- [ ] Investor database integration

### Medium-term
- [ ] Web UI dashboard
- [ ] Batch analysis engine
- [ ] Historical analysis tracking
- [ ] Performance benchmarking

### Long-term
- [ ] Machine learning model training
- [ ] Automated deal sourcing
- [ ] Market intelligence integration
- [ ] Exit prediction models
