"""Market analysis module"""

from typing import Dict, Any, List, Optional
from ..models.schemas import MarketAnalysis
from ..models.enums import MarketStage


class MarketAnalyzer:
    """Analyzes market size and opportunity"""
    
    def __init__(self, llm_provider=None):
        """Initialize market analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, market_data: Dict[str, Any]) -> MarketAnalysis:
        """Analyze market opportunity
        
        Args:
            market_data: Dictionary with market information
                - target_market: str
                - total_addressable_market: float
                - serviceable_addressable_market: float
                - serviceable_obtainable_market: float
                - market_stage: str
                - growth_rate: float
                - target_segments: List[str]
                - market_trends: List[str]
                - regulatory_environment: str
        
        Returns:
            MarketAnalysis with assessment
        """
        # Score market components
        tam_som_score = self._score_tam_sizing(market_data)
        growth_score = self._score_growth_potential(market_data)
        segment_score = self._score_target_segments(market_data)
        trend_score = self._score_market_trends(market_data)
        
        # Calculate overall score
        overall_score = (
            tam_som_score * 0.30 +
            growth_score * 0.35 +
            segment_score * 0.20 +
            trend_score * 0.15
        )
        
        # Get market stage
        market_stage = self._determine_market_stage(market_data)
        
        # Assess opportunity strength
        opportunity_strength = self._assess_opportunity_strength(overall_score, market_data)
        
        return MarketAnalysis(
            overall_score=round(overall_score, 1),
            summary=self._generate_summary(market_data, overall_score),
            tam_estimate_usd=market_data.get("total_addressable_market"),
            sam_estimate_usd=market_data.get("serviceable_addressable_market"),
            som_estimate_usd=market_data.get("serviceable_obtainable_market"),
            market_stage=market_stage,
            growth_rate_percent=market_data.get("growth_rate"),
            market_size_assessment=self._assess_market_size(market_data),
            target_segments=market_data.get("target_segments", []),
            market_trends=market_data.get("market_trends", []),
            regulatory_considerations=self._identify_regulatory_concerns(market_data),
            opportunity_strength=opportunity_strength,
        )
    
    def _score_tam_sizing(self, market_data: Dict[str, Any]) -> float:
        """Score TAM sizing and validity"""
        score = 50  # baseline
        
        tam = market_data.get("total_addressable_market", 0)
        
        # TAM size assessment
        if tam >= 100_000_000:  # $100M+
            score += 30
        elif tam >= 10_000_000:  # $10M+
            score += 20
        elif tam >= 1_000_000:  # $1M+
            score += 10
        
        # SAM/SOM defined
        sam = market_data.get("serviceable_addressable_market", 0)
        som = market_data.get("serviceable_obtainable_market", 0)
        
        if sam and sam < tam:
            score += 15
        if som and som < sam:
            score += 15
        
        # TAM methodology clarity
        tam_methodology = market_data.get("tam_methodology", "")
        if tam_methodology:
            score += 10
        
        return min(100, score)
    
    def _score_growth_potential(self, market_data: Dict[str, Any]) -> float:
        """Score growth potential"""
        score = 50  # baseline
        
        growth_rate = market_data.get("growth_rate", 0)
        
        # CAGR assessment
        if growth_rate >= 30:
            score += 35
        elif growth_rate >= 15:
            score += 25
        elif growth_rate >= 5:
            score += 15
        
        # Stage of market
        market_stage_str = market_data.get("market_stage", "").lower()
        if "emerging" in market_stage_str or "early" in market_stage_str:
            score += 20
        elif "growing" in market_stage_str:
            score += 10
        
        return min(100, score)
    
    def _score_target_segments(self, market_data: Dict[str, Any]) -> float:
        """Score quality of target segments"""
        score = 50  # baseline
        
        segments = market_data.get("target_segments", [])
        
        # Number of segments
        if len(segments) >= 3:
            score += 15
        elif len(segments) >= 1:
            score += 10
        
        # Segment clarity
        for segment in segments:
            if segment and len(segment) > 5:  # Well-described segment
                score += 5
                break
        
        # Segment size/attractiveness
        segment_assessment = market_data.get("segment_assessment", "")
        if "large" in segment_assessment.lower() or "attractive" in segment_assessment.lower():
            score += 15
        
        return min(100, score)
    
    def _score_market_trends(self, market_data: Dict[str, Any]) -> float:
        """Score alignment with market trends"""
        score = 50  # baseline
        
        trends = market_data.get("market_trends", [])
        
        # Identified trends
        if len(trends) >= 3:
            score += 25
        elif len(trends) >= 1:
            score += 15
        
        # Trend tailwinds
        for trend in trends:
            if any(word in str(trend).lower() for word in ["growth", "adoption", "demand", "expansion"]):
                score += 10
                break
        
        return min(100, score)
    
    def _determine_market_stage(self, market_data: Dict[str, Any]) -> MarketStage:
        """Determine current market stage"""
        stage_str = market_data.get("market_stage", "").lower()
        
        if "emerging" in stage_str or "early" in stage_str:
            return MarketStage.EMERGING
        elif "growing" in stage_str or "growth" in stage_str:
            return MarketStage.GROWING
        elif "mature" in stage_str or "established" in stage_str:
            return MarketStage.MATURE
        elif "declining" in stage_str:
            return MarketStage.DECLINING
        else:
            return MarketStage.GROWING
    
    def _assess_opportunity_strength(self, score: float, market_data: Dict[str, Any]) -> str:
        """Assess overall opportunity strength"""
        tam = market_data.get("total_addressable_market", 0)
        
        if score >= 75 and tam >= 100_000_000:
            return "Strong market opportunity with large TAM and growth tailwinds"
        elif score >= 65 and tam >= 10_000_000:
            return "Moderate market opportunity with adequate size and growth"
        elif score >= 50:
            return "Moderate opportunity but with some market sizing or growth questions"
        else:
            return "Weak market opportunity or insufficient market data"
    
    def _assess_market_size(self, market_data: Dict[str, Any]) -> str:
        """Assess market sizing approach"""
        tam = market_data.get("total_addressable_market", 0)
        methodology = market_data.get("tam_methodology", "")
        
        if tam >= 100_000_000 and methodology:
            return f"Large TAM (${tam/1e6:.0f}M) with clear methodology"
        elif tam >= 10_000_000:
            return f"Adequate TAM (${tam/1e6:.0f}M) for VC investment"
        elif tam >= 1_000_000:
            return f"Modest TAM (${tam/1e6:.0f}M) - may limit upside"
        else:
            return "Market sizing unclear or insufficient TAM disclosed"
    
    def _identify_regulatory_concerns(self, market_data: Dict[str, Any]) -> List[str]:
        """Identify regulatory considerations"""
        concerns = []
        
        regulatory = market_data.get("regulatory_environment", "").lower()
        
        if "strict" in regulatory or "regulated" in regulatory:
            concerns.append("Highly regulated market - compliance requirements")
        if "changing" in regulatory or "uncertain" in regulatory:
            concerns.append("Regulatory environment uncertain or changing")
        if "antitrust" in regulatory or "antitrust" in market_data.get("target_market", "").lower():
            concerns.append("Potential antitrust or monopoly considerations")
        
        return concerns
    
    def _generate_summary(self, market_data: Dict[str, Any], score: float) -> str:
        """Generate summary text"""
        tam = market_data.get("total_addressable_market", 0)
        growth = market_data.get("growth_rate", 0)
        
        tam_str = f"${tam/1e6:.0f}M" if tam >= 1_000_000 else f"${tam/1e3:.0f}K"
        
        if score >= 75:
            return (f"Large addressable market ({tam_str}) with {growth:.0f}% annual growth. "
                   "Strong macro tailwinds and clear customer segments.")
        elif score >= 60:
            return (f"Adequate market size ({tam_str}) with {growth:.0f}% growth. "
                   "Clear opportunity but may require more specificity on TAM sizing.")
        elif score >= 40:
            return (f"Market opportunity exists but sizing assumptions unclear. "
                   "TAM estimate of {tam_str} requires validation.")
        else:
            return "Market sizing concerns or insufficient opportunity for venture-scale returns."
