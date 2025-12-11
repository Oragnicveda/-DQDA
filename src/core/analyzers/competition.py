"""Competition analysis module"""

from typing import Dict, Any, List
from ..models.schemas import CompetitionAnalysis, Competitor


class CompetitionAnalyzer:
    """Analyzes competitive landscape"""
    
    def __init__(self, llm_provider=None):
        """Initialize competition analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, competition_data: Dict[str, Any]) -> CompetitionAnalysis:
        """Analyze competitive landscape
        
        Args:
            competition_data: Dictionary with competition information
                - company_name: str
                - competitive_advantage: str
                - direct_competitors: List[Dict]
                - indirect_competitors: List[Dict]
                - potential_new_entrants: List[str]
                - unique_positioning: str
        
        Returns:
            CompetitionAnalysis with assessment
        """
        # Process competitors
        direct_competitors = self._process_competitors(
            competition_data.get("direct_competitors", []),
            company_name=competition_data.get("company_name")
        )
        
        indirect_competitors = self._process_competitors(
            competition_data.get("indirect_competitors", []),
            company_name=competition_data.get("company_name"),
            is_indirect=True
        )
        
        # Score components
        advantage_score = self._score_competitive_advantage(competition_data)
        positioning_score = self._score_positioning(competition_data)
        competitive_score = self._score_competitive_landscape(
            direct_competitors, indirect_competitors
        )
        
        # Calculate overall score
        overall_score = (
            advantage_score * 0.35 +
            positioning_score * 0.30 +
            competitive_score * 0.35
        )
        
        # Identify red flags and opportunities
        red_flags = self._identify_competitive_risks(
            direct_competitors, competition_data
        )
        opportunities = self._identify_opportunities(competition_data)
        
        return CompetitionAnalysis(
            overall_score=round(overall_score, 1),
            summary=self._generate_summary(competition_data, overall_score),
            direct_competitors=direct_competitors,
            indirect_competitors=indirect_competitors,
            potential_new_entrants=competition_data.get("potential_new_entrants", []),
            competitive_advantage=competition_data.get("competitive_advantage", "Not specified"),
            competitive_advantage_defensibility=self._assess_defensibility(competition_data),
            market_positioning=competition_data.get("unique_positioning", "Not specified"),
            red_flags=red_flags,
            opportunities=opportunities,
        )
    
    def _process_competitors(
        self,
        competitors: List[Dict[str, Any]],
        company_name: str = "",
        is_indirect: bool = False
    ) -> List[Competitor]:
        """Process and analyze competitor data"""
        processed = []
        
        for comp_data in competitors:
            threat_level = self._assess_threat_level(comp_data, is_indirect)
            
            competitor = Competitor(
                name=comp_data.get("name", "Unknown"),
                positioning=comp_data.get("positioning", "Not specified"),
                strengths=comp_data.get("strengths", []),
                weaknesses=comp_data.get("weaknesses", []),
                differentiation_vs_target=self._analyze_differentiation(
                    comp_data, company_name
                ),
                funding_stage=comp_data.get("funding_stage"),
                threat_level=threat_level,
            )
            processed.append(competitor)
        
        return processed
    
    def _score_competitive_advantage(self, competition_data: Dict[str, Any]) -> float:
        """Score strength of competitive advantage"""
        score = 50  # baseline
        
        advantage = competition_data.get("competitive_advantage", "").lower()
        
        # Clear advantage statement
        if advantage and len(advantage) > 20:
            score += 15
        
        # Type of advantage
        if any(word in advantage for word in ["proprietary", "patent", "moat", "network", "brand"]):
            score += 25
        elif any(word in advantage for word in ["team", "experience", "cost", "speed"]):
            score += 15
        else:
            score -= 10
        
        # Defensibility assessment
        defensibility = competition_data.get("competitive_advantage_defensibility", "").lower()
        if "defensible" in defensibility or "strong" in defensibility:
            score += 15
        elif "weak" in defensibility or "copyable" in defensibility:
            score -= 15
        
        return max(0, min(100, score))
    
    def _score_positioning(self, competition_data: Dict[str, Any]) -> float:
        """Score market positioning clarity"""
        score = 50  # baseline
        
        positioning = competition_data.get("unique_positioning", "").lower()
        
        # Clear positioning
        if positioning and len(positioning) > 20:
            score += 20
        
        # Positioning specificity
        if any(word in positioning for word in ["vs", "unlike", "only", "first", "different"]):
            score += 15
        
        # Target market clarity
        target = competition_data.get("target_market", "")
        if target and len(target) > 5:
            score += 15
        
        return min(100, score)
    
    def _score_competitive_landscape(
        self,
        direct_competitors: List[Competitor],
        indirect_competitors: List[Competitor]
    ) -> float:
        """Score competitive landscape favorability"""
        score = 50  # baseline
        
        # Fragmented market is positive
        if len(direct_competitors) <= 2:
            score += 25  # Emerging/monopoly potential
        elif len(direct_competitors) <= 5:
            score += 15  # Moderate competition
        else:
            score -= 10  # Crowded market
        
        # Major players
        big_players = [c for c in direct_competitors if c.funding_stage and "Series" in c.funding_stage]
        if len(big_players) == 0:
            score += 15
        elif len(big_players) > 3:
            score -= 15
        
        # Check threat levels
        high_threat = [c for c in direct_competitors if c.threat_level == "High"]
        if len(high_threat) == 0:
            score += 10
        elif len(high_threat) > 2:
            score -= 20
        
        return max(0, min(100, score))
    
    def _assess_threat_level(self, competitor: Dict[str, Any], is_indirect: bool) -> str:
        """Assess threat level of competitor"""
        if is_indirect:
            return "Low"  # Indirect competitors are lower threat
        
        threat = "Medium"  # Default
        
        # Check funding level
        funding = competitor.get("funding_stage", "").lower()
        if "series c" in funding or "series d" in funding or "public" in funding:
            threat = "High"
        elif "seed" in funding or "series a" in funding:
            threat = "Low"
        
        # Check market share
        market_share = competitor.get("market_share", 0)
        if market_share > 20:
            threat = "High"
        elif market_share > 5:
            threat = "Medium"
        
        # Check growth
        growth = competitor.get("growth_rate", 0)
        if growth > 50 and threat == "Medium":
            threat = "High"
        
        return threat
    
    def _analyze_differentiation(
        self,
        competitor: Dict[str, Any],
        target_company: str
    ) -> str:
        """Analyze how target company differs from competitor"""
        comp_positioning = competitor.get("positioning", "")
        
        if comp_positioning:
            return f"Different approach: {comp_positioning}"
        else:
            return "Differentiation requires clarification"
    
    def _identify_competitive_risks(
        self,
        direct_competitors: List[Competitor],
        competition_data: Dict[str, Any]
    ) -> List[str]:
        """Identify competitive risks"""
        risks = []
        
        # Major well-funded competitors
        for comp in direct_competitors:
            if comp.threat_level == "High":
                risks.append(f"Direct competitor {comp.name} is well-funded and established")
        
        # Market consolidation risk
        if len(direct_competitors) > 10:
            risks.append("Highly fragmented market may consolidate around few winners")
        
        # Big tech entry risk
        potential_entrants = competition_data.get("potential_new_entrants", [])
        if any("google" in str(p).lower() or "amazon" in str(p).lower() for p in potential_entrants):
            risks.append("Risk of big tech companies entering market")
        
        # Weak differentiation
        advantage = competition_data.get("competitive_advantage", "").lower()
        if not advantage or len(advantage) < 10:
            risks.append("Weak or unclear competitive advantage")
        
        # Copying risk
        defensibility = competition_data.get("competitive_advantage_defensibility", "").lower()
        if "weak" in defensibility or "easily copied" in defensibility:
            risks.append("Competitive advantage may be easily copied by larger players")
        
        return risks
    
    def _identify_opportunities(self, competition_data: Dict[str, Any]) -> List[str]:
        """Identify competitive opportunities"""
        opportunities = []
        
        # Emerging market
        direct_competitors = competition_data.get("direct_competitors", [])
        if len(direct_competitors) <= 2:
            opportunities.append("Opportunity to establish category leadership in emerging market")
        
        # Consolidation
        if len(direct_competitors) > 5:
            opportunities.append("Fragmented market opportunity for consolidation play")
        
        # Underserved segment
        segments = competition_data.get("underserved_segments", [])
        if segments:
            opportunities.append(f"Opportunity to serve underserved segments: {', '.join(segments)}")
        
        # Tech advantage
        if "AI" in competition_data.get("competitive_advantage", "") or "ML" in competition_data.get("competitive_advantage", ""):
            opportunities.append("Strong technology moat potential with continued development")
        
        return opportunities
    
    def _assess_defensibility(self, competition_data: Dict[str, Any]) -> str:
        """Assess how defensible the competitive advantage is"""
        advantage = competition_data.get("competitive_advantage", "").lower()
        
        # Patent/IP
        if "patent" in advantage or "proprietary" in advantage:
            return "Strong - Protected by IP/patents"
        
        # Network effects
        if "network" in advantage or "community" in advantage:
            return "Strong - Network effects create moat"
        
        # Data/ML
        if "data" in advantage or "ai" in advantage or "ml" in advantage:
            return "Strong - Data advantage improving over time"
        
        # Brand
        if "brand" in advantage or "reputation" in advantage:
            return "Moderate - Brand moat is defensible but requires maintenance"
        
        # Team/operations
        if "team" in advantage or "operations" in advantage:
            return "Weak - Team and operational advantages are copyable"
        
        # Cost
        if "cost" in advantage or "price" in advantage:
            return "Weak - Cost advantages typically not sustainable"
        
        return "Unclear - Defensibility assessment required"
    
    def _generate_summary(self, competition_data: Dict[str, Any], score: float) -> str:
        """Generate summary text"""
        direct_competitors = competition_data.get("direct_competitors", [])
        
        if score >= 75:
            return (f"Strong competitive position with clear differentiation. "
                   f"Moderate competition landscape ({len(direct_competitors)} direct competitors) "
                   f"with sustainable competitive advantage.")
        elif score >= 60:
            return (f"Reasonable competitive positioning but with some crowding "
                   f"({len(direct_competitors)} direct competitors). Advantage needs to be defensible.")
        elif score >= 40:
            return (f"Competitive landscape is challenging with {len(direct_competitors)} competitors "
                   f"and unclear differentiation. Consider pivoting or focusing on niche.")
        else:
            return (f"Highly competitive market ({len(direct_competitors)} competitors) with weak "
                   f"competitive advantage. Difficult to achieve market leadership.")
