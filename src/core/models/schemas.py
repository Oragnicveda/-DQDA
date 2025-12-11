"""Pydantic schemas for DQDA analysis results"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from .enums import (
    InvestorType,
    WeaknessLevel,
    MarketStage,
    FounderBackgroundType,
    TokenomicsHealth,
)


class ScoreComponent(BaseModel):
    """Single scoring component"""
    category: str
    score: float = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    reasoning: str


class FounderReadinessScore(BaseModel):
    """Founder readiness assessment"""
    overall_score: float = Field(ge=0, le=100, description="0-100 founder readiness score")
    summary: str = Field(description="Executive summary of founder readiness")
    
    # Components
    experience_score: float = Field(ge=0, le=100)
    track_record_score: float = Field(ge=0, le=100)
    execution_capability_score: float = Field(ge=0, le=100)
    team_completeness_score: float = Field(ge=0, le=100)
    
    founder_backgrounds: List[FounderBackgroundType] = Field(description="Types of expertise on team")
    previous_exits: Optional[List[Dict[str, Any]]] = Field(default=None, description="Past exits and outcomes")
    domain_expertise_level: str = Field(description="Assessment of domain expertise")
    potential_red_flags: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=list)
    
    recommendation: str = Field(description="Go/No-go recommendation")


class MarketAnalysis(BaseModel):
    """Market size and opportunity analysis"""
    overall_score: float = Field(ge=0, le=100)
    summary: str
    
    # Market sizing
    tam_estimate_usd: Optional[float] = Field(default=None, description="Total Addressable Market in USD")
    sam_estimate_usd: Optional[float] = Field(default=None, description="Serviceable Addressable Market")
    som_estimate_usd: Optional[float] = Field(default=None, description="Serviceable Obtainable Market")
    
    market_stage: MarketStage = Field(description="Current stage of market development")
    growth_rate_percent: Optional[float] = Field(default=None, description="Annual growth rate %")
    market_size_assessment: str = Field(description="Qualitative assessment of market size")
    
    target_segments: List[str] = Field(default_factory=list, description="Key target customer segments")
    market_trends: List[str] = Field(default_factory=list, description="Relevant market trends")
    regulatory_considerations: List[str] = Field(default_factory=list)
    
    opportunity_strength: str = Field(description="Strong/Moderate/Weak market opportunity")


class Competitor(BaseModel):
    """Single competitor assessment"""
    name: str
    positioning: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    differentiation_vs_target: str = Field(description="How target company differs")
    funding_stage: Optional[str] = Field(default=None)
    threat_level: str = Field(description="Low/Medium/High threat")


class CompetitionAnalysis(BaseModel):
    """Competition landscape analysis"""
    overall_score: float = Field(ge=0, le=100)
    summary: str
    
    direct_competitors: List[Competitor] = Field(default_factory=list)
    indirect_competitors: List[Competitor] = Field(default_factory=list)
    potential_new_entrants: List[str] = Field(default_factory=list)
    
    competitive_advantage: str = Field(description="Company's stated competitive advantage")
    competitive_advantage_defensibility: str = Field(description="How defensible is the advantage")
    market_positioning: str = Field(description="Unique positioning in market")
    
    red_flags: List[str] = Field(default_factory=list, description="Competitive concerns")
    opportunities: List[str] = Field(default_factory=list, description="Competitive opportunities")


class TokenDistribution(BaseModel):
    """Token distribution details"""
    recipient: str
    percentage: float = Field(ge=0, le=100)
    vesting_period_months: Optional[int] = Field(default=None)
    lock_period_months: Optional[int] = Field(default=None)


class TokenUtilityAnalysis(BaseModel):
    """Token utility and tokenomics analysis"""
    overall_score: float = Field(ge=0, le=100)
    summary: str
    
    token_health: TokenomicsHealth = Field(description="Overall tokenomics health")
    
    # Token basics
    token_name: str
    ticker: str
    total_supply: float
    circulating_supply: float
    max_supply: Optional[float] = Field(default=None)
    
    # Utility assessment
    utility_description: str = Field(description="Description of token utility")
    utility_strength: str = Field(description="Strong/Moderate/Weak utility")
    is_governance_token: bool = Field(description="Whether token has governance rights")
    is_fee_token: bool = Field(description="Whether token captures fees/value")
    
    # Distribution
    distribution: List[TokenDistribution] = Field(default_factory=list)
    team_allocation_percent: float = Field(ge=0, le=100)
    investor_allocation_percent: float = Field(ge=0, le=100)
    community_allocation_percent: float = Field(ge=0, le=100)
    
    # Concerns
    inflation_concerns: List[str] = Field(default_factory=list)
    concentration_risks: List[str] = Field(default_factory=list)
    vesting_concerns: List[str] = Field(default_factory=list)
    
    recommendation: str = Field(description="Tokenomics viability assessment")


class Weakness(BaseModel):
    """Individual weakness/gap identified"""
    category: str = Field(description="e.g., technical, narrative, market")
    issue: str = Field(description="Description of the issue")
    severity: WeaknessLevel
    impact: str = Field(description="Impact on investment thesis")
    remediation: Optional[str] = Field(default=None, description="How to fix")


class WeaknessAnalysis(BaseModel):
    """Combined technical and narrative weakness analysis"""
    technical_summary: str
    narrative_summary: str
    
    technical_weaknesses: List[Weakness] = Field(default_factory=list)
    narrative_weaknesses: List[Weakness] = Field(default_factory=list)
    
    total_critical_issues: int = Field(ge=0)
    total_high_issues: int = Field(ge=0)
    
    overall_risk_assessment: str = Field(description="Low/Medium/High risk")
    deal_killers: List[str] = Field(default_factory=list, description="Fatal flaws if any")


class InvestorFitScore(BaseModel):
    """Fit score for a specific investor type"""
    investor_type: InvestorType
    fit_score: float = Field(ge=0, le=100)
    rationale: str
    alignment_factors: List[str] = Field(default_factory=list)
    misalignment_factors: List[str] = Field(default_factory=list)


class InvestorFitPrediction(BaseModel):
    """Investor fit predictions across investor types"""
    scores: List[InvestorFitScore] = Field(default_factory=list)
    
    best_fit_investor_type: InvestorType
    best_fit_score: float = Field(ge=0, le=100)
    
    should_pitch: bool = Field(description="Whether team should pitch broadly")
    target_investor_profiles: List[str] = Field(
        default_factory=list,
        description="Specific investor types/funds to target"
    )
    positioning_recommendations: List[str] = Field(
        default_factory=list,
        description="How to position for target investors"
    )


class AnalysisResult(BaseModel):
    """Complete DQDA analysis result"""
    # Metadata
    deal_name: str
    analysis_date: datetime = Field(default_factory=datetime.utcnow)
    founder_name: Optional[str] = Field(default=None)
    
    # Overall scoring
    overall_deal_quality_score: float = Field(
        ge=0, le=100,
        description="Composite score (0-100) of deal quality"
    )
    investment_recommendation: str = Field(
        description="Strong Pass/Pass/Borderline/Weak Pass/Pass on this deal"
    )
    
    # Component analyses
    founder_readiness: FounderReadinessScore
    market_analysis: MarketAnalysis
    competition_analysis: CompetitionAnalysis
    token_utility_analysis: TokenUtilityAnalysis
    weakness_analysis: WeaknessAnalysis
    investor_fit: InvestorFitPrediction
    
    # Executive summary
    executive_summary: str = Field(
        description="2-3 paragraph summary of deal potential and key issues"
    )
    key_strengths: List[str] = Field(default_factory=list)
    key_concerns: List[str] = Field(default_factory=list)
    immediate_action_items: List[str] = Field(default_factory=list)
    
    # Raw data for reference
    source_documents: Dict[str, Optional[str]] = Field(
        default_factory=dict,
        description="References to source documents analyzed"
    )
