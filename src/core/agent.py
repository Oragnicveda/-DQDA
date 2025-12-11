"""Main DQDA orchestrator agent"""

from typing import Dict, Any, Optional
from datetime import datetime

from .models.schemas import AnalysisResult
from .analyzers import (
    FounderAnalyzer,
    MarketAnalyzer,
    CompetitionAnalyzer,
    TokenomicsAnalyzer,
    TechnicalAnalyzer,
    InvestorFitAnalyzer,
)


class DQDAAgent:
    """Main orchestrator for DQDA analysis"""
    
    def __init__(self, llm_provider=None):
        """Initialize DQDA agent with optional LLM provider
        
        Args:
            llm_provider: Optional LLM provider for enhanced analysis
        """
        self.llm = llm_provider
        
        # Initialize analyzers
        self.founder_analyzer = FounderAnalyzer(llm_provider)
        self.market_analyzer = MarketAnalyzer(llm_provider)
        self.competition_analyzer = CompetitionAnalyzer(llm_provider)
        self.tokenomics_analyzer = TokenomicsAnalyzer(llm_provider)
        self.technical_analyzer = TechnicalAnalyzer(llm_provider)
        self.investor_fit_analyzer = InvestorFitAnalyzer(llm_provider)
    
    def analyze(self, deal_data: Dict[str, Any]) -> AnalysisResult:
        """Perform comprehensive DQDA analysis
        
        Args:
            deal_data: Dictionary containing all deal information
                - name: str (deal/company name)
                - founder: Dict (founder information)
                - market: Dict (market opportunity data)
                - competition: Dict (competitive landscape)
                - tokenomics: Dict (token data, if applicable)
                - technical: Dict (technical assessment)
                - narrative: Dict (business narrative assessment)
        
        Returns:
            AnalysisResult with complete analysis
        """
        deal_name = deal_data.get("name", "Unknown Deal")
        
        print(f"\n{'='*60}")
        print(f"DQDA Analysis: {deal_name}")
        print(f"{'='*60}")
        
        # Run individual analyses
        print("\n[1/7] Analyzing founder readiness...")
        founder_analysis = self.founder_analyzer.analyze(deal_data.get("founder", {}))
        
        print("[2/7] Analyzing market opportunity...")
        market_analysis = self.market_analyzer.analyze(deal_data.get("market", {}))
        
        print("[3/7] Analyzing competitive landscape...")
        competition_analysis = self.competition_analyzer.analyze(deal_data.get("competition", {}))
        
        print("[4/7] Analyzing tokenomics...")
        token_analysis = self.tokenomics_analyzer.analyze(deal_data.get("tokenomics", {}))
        
        print("[5/7] Identifying weaknesses...")
        weakness_analysis = self.technical_analyzer.analyze(deal_data.get("technical", {}))
        
        print("[6/7] Predicting investor fit...")
        # Add analysis data for investor fit
        investor_fit_data = {
            **deal_data,
            "founder_readiness_score": founder_analysis.overall_score,
            "market_analysis": market_analysis,
            "token_utility_analysis": token_analysis,
            "founder_backgrounds": founder_analysis.founder_backgrounds,
        }
        investor_fit_analysis = self.investor_fit_analyzer.analyze(investor_fit_data)
        
        print("[7/7] Generating final assessment...")
        
        # Calculate overall deal quality score
        overall_score = self._calculate_overall_score(
            founder_analysis,
            market_analysis,
            competition_analysis,
            token_analysis,
            weakness_analysis,
            investor_fit_analysis,
        )
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            overall_score,
            weakness_analysis,
            investor_fit_analysis,
        )
        
        # Generate executive summary
        summary = self._generate_executive_summary(
            deal_name,
            founder_analysis,
            market_analysis,
            competition_analysis,
            weakness_analysis,
        )
        
        # Compile key strengths and concerns
        key_strengths = self._extract_strengths(
            founder_analysis,
            market_analysis,
            competition_analysis,
        )
        
        key_concerns = self._extract_concerns(
            weakness_analysis,
            competition_analysis,
            founder_analysis,
        )
        
        # Get action items
        action_items = self._identify_action_items(
            weakness_analysis,
            market_analysis,
        )
        
        # Create result
        result = AnalysisResult(
            deal_name=deal_name,
            analysis_date=datetime.utcnow(),
            founder_name=deal_data.get("founder", {}).get("name"),
            overall_deal_quality_score=overall_score,
            investment_recommendation=recommendation,
            founder_readiness=founder_analysis,
            market_analysis=market_analysis,
            competition_analysis=competition_analysis,
            token_utility_analysis=token_analysis,
            weakness_analysis=weakness_analysis,
            investor_fit=investor_fit_analysis,
            executive_summary=summary,
            key_strengths=key_strengths,
            key_concerns=key_concerns,
            immediate_action_items=action_items,
            source_documents={
                "pitch_deck": deal_data.get("pitch_deck_path"),
                "whitepaper": deal_data.get("whitepaper_path"),
                "website": deal_data.get("website_url"),
            }
        )
        
        print(f"\n✓ Analysis complete!")
        print(f"Overall Quality Score: {overall_score}/100")
        print(f"Recommendation: {recommendation}")
        
        return result
    
    def _calculate_overall_score(
        self,
        founder_analysis,
        market_analysis,
        competition_analysis,
        token_analysis,
        weakness_analysis,
        investor_fit_analysis,
    ) -> float:
        """Calculate composite deal quality score"""
        # Weights
        weights = {
            "founder": 0.25,
            "market": 0.25,
            "competition": 0.15,
            "tokenomics": 0.15,
            "weakness_penalty": 0.15,
            "investor_fit": 0.05,
        }
        
        # Base scores
        founder_score = founder_analysis.overall_score
        market_score = market_analysis.overall_score
        competition_score = competition_analysis.overall_score
        tokenomics_score = token_analysis.overall_score
        investor_fit_score = investor_fit_analysis.best_fit_score
        
        # Weakness penalty
        critical_count = weakness_analysis.total_critical_issues
        high_count = weakness_analysis.total_high_issues
        weakness_penalty = (critical_count * 15) + (high_count * 5)
        weakness_score = max(0, 100 - weakness_penalty)
        
        # Calculate weighted score
        overall = (
            founder_score * weights["founder"] +
            market_score * weights["market"] +
            competition_score * weights["competition"] +
            tokenomics_score * weights["tokenomics"] +
            weakness_score * weights["weakness_penalty"] +
            investor_fit_score * weights["investor_fit"]
        )
        
        return round(overall, 1)
    
    def _generate_recommendation(
        self,
        overall_score: float,
        weakness_analysis,
        investor_fit_analysis,
    ) -> str:
        """Generate investment recommendation"""
        if weakness_analysis.deal_killers:
            return "Pass on this deal - fatal flaws identified"
        
        if overall_score >= 80:
            return "Strong Pass - Excellent deal quality and fit"
        elif overall_score >= 70:
            return "Pass - Good deal with strong fundamentals"
        elif overall_score >= 60:
            return "Borderline - Address key concerns before moving forward"
        elif overall_score >= 50:
            return "Weak Pass - Significant work needed"
        else:
            return "Pass - Do not advance at this time"
    
    def _generate_executive_summary(
        self,
        deal_name: str,
        founder_analysis,
        market_analysis,
        competition_analysis,
        weakness_analysis,
    ) -> str:
        """Generate 2-3 paragraph executive summary"""
        summary = f"**{deal_name}** presents "
        
        # Market assessment
        if market_analysis.overall_score >= 70:
            summary += f"a strong market opportunity with ${market_analysis.tam_estimate_usd/1e6:.0f}M+ TAM. "
        else:
            summary += "a market opportunity but with sizing questions. "
        
        # Founder assessment
        if founder_analysis.overall_score >= 70:
            summary += f"The founding team has strong experience and execution capability. "
        else:
            summary += f"The founding team would benefit from additional experience. "
        
        # Competition
        if competition_analysis.overall_score >= 70:
            summary += f"The company has defensible competitive positioning. "
        else:
            summary += f"The competitive landscape is challenging. "
        
        # Weaknesses
        if weakness_analysis.deal_killers:
            summary += f"\n\nHowever, critical issues require resolution: "
            summary += "; ".join(weakness_analysis.deal_killers[:2])
        elif weakness_analysis.total_critical_issues > 0:
            summary += f"\n\nKey concerns include critical gaps in {', '.join([w.category for w in weakness_analysis.technical_weaknesses + weakness_analysis.narrative_weaknesses if w.severity.value == 'critical'][:2])}."
        else:
            summary += f"\n\nKey areas for improvement include addressing identified weaknesses before closing."
        
        return summary
    
    def _extract_strengths(
        self,
        founder_analysis,
        market_analysis,
        competition_analysis,
    ) -> list:
        """Extract key deal strengths"""
        strengths = []
        
        # From founder
        strengths.extend(founder_analysis.strengths[:2])
        
        # From market
        if market_analysis.overall_score >= 70:
            strengths.append(f"Large market opportunity (${market_analysis.tam_estimate_usd/1e6:.0f}M TAM)")
        
        # From competition
        if competition_analysis.overall_score >= 70:
            strengths.append(f"Defensible competitive positioning: {competition_analysis.competitive_advantage}")
        
        return strengths
    
    def _extract_concerns(
        self,
        weakness_analysis,
        competition_analysis,
        founder_analysis,
    ) -> list:
        """Extract key deal concerns"""
        concerns = []
        
        # From weaknesses
        critical_issues = [w for w in weakness_analysis.technical_weaknesses + weakness_analysis.narrative_weaknesses 
                          if w.severity.value == 'critical']
        for issue in critical_issues[:3]:
            concerns.append(f"{issue.category}: {issue.issue}")
        
        # From competition
        if competition_analysis.red_flags:
            concerns.extend(competition_analysis.red_flags[:2])
        
        # From founder
        if founder_analysis.potential_red_flags:
            concerns.extend(founder_analysis.potential_red_flags[:1])
        
        return concerns
    
    def _identify_action_items(
        self,
        weakness_analysis,
        market_analysis,
    ) -> list:
        """Identify immediate action items"""
        items = []
        
        # From weaknesses
        for weakness in weakness_analysis.technical_weaknesses + weakness_analysis.narrative_weaknesses:
            if weakness.severity.value in ['critical', 'high']:
                if weakness.remediation:
                    items.append(weakness.remediation)
        
        # Market validation
        if market_analysis.overall_score < 60:
            items.append("Validate market sizing assumptions with customer interviews")
        
        return items[:5]  # Return top 5 items
