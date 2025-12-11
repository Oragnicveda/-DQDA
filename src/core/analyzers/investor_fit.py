"""Investor fit prediction module"""

from typing import Dict, Any, List
from ..models.schemas import InvestorFitPrediction, InvestorFitScore
from ..models.enums import InvestorType


class InvestorFitAnalyzer:
    """Predicts fit with different investor types"""
    
    def __init__(self, llm_provider=None):
        """Initialize investor fit analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, analysis_data: Dict[str, Any]) -> InvestorFitPrediction:
        """Analyze investor fit across investor types
        
        Args:
            analysis_data: Complete analysis data including founder, market, and tokenomics
        
        Returns:
            InvestorFitPrediction with recommendations
        """
        # Calculate fit scores for each investor type
        scores = [
            self._score_growth_stage_vc(analysis_data),
            self._score_seed_stage_vc(analysis_data),
            self._score_crypto_specialist(analysis_data),
            self._score_strategic_corporate(analysis_data),
            self._score_angel_investor(analysis_data),
            self._score_token_fund(analysis_data),
        ]
        
        # Find best fit
        best_score = max(scores, key=lambda s: s.fit_score)
        
        # Determine if should pitch broadly
        should_pitch = best_score.fit_score >= 60
        
        # Get target profiles
        target_profiles = self._get_target_profiles(scores)
        
        # Get positioning recommendations
        positioning = self._get_positioning_recommendations(
            best_score.investor_type,
            analysis_data
        )
        
        return InvestorFitPrediction(
            scores=sorted(scores, key=lambda s: s.fit_score, reverse=True),
            best_fit_investor_type=best_score.investor_type,
            best_fit_score=best_score.fit_score,
            should_pitch=should_pitch,
            target_investor_profiles=target_profiles,
            positioning_recommendations=positioning,
        )
    
    def _score_growth_stage_vc(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with growth-stage VCs"""
        score = 0
        alignment = []
        misalignment = []
        
        # Check traction
        revenue = analysis_data.get("revenue", 0)
        if revenue > 1_000_000:
            score += 30
            alignment.append("Strong revenue traction ($1M+)")
        elif revenue > 100_000:
            score += 15
            alignment.append("Some revenue traction")
        else:
            misalignment.append("Limited revenue/traction")
        
        # Check team
        team_size = len(analysis_data.get("team", []))
        if team_size >= 5:
            score += 20
            alignment.append("Established team of 5+")
        elif team_size >= 2:
            score += 10
        else:
            misalignment.append("Small or solo team")
        
        # Check founder track record
        founder_score = analysis_data.get("founder_readiness_score", 50)
        if founder_score >= 70:
            score += 15
            alignment.append("Strong founder with track record")
        elif founder_score >= 50:
            score += 5
        else:
            misalignment.append("Weak founder readiness")
        
        # Check market size
        tam = analysis_data.get("tam_estimate_usd", 0)
        if tam >= 100_000_000:
            score += 15
            alignment.append("Large TAM ($100M+)")
        elif tam >= 10_000_000:
            score += 5
        else:
            misalignment.append("Small TAM")
        
        # Check product-market fit
        if analysis_data.get("product_market_fit"):
            score += 10
            alignment.append("Demonstrated product-market fit")
        else:
            misalignment.append("No clear product-market fit yet")
        
        return InvestorFitScore(
            investor_type=InvestorType.GROWTH_STAGE_VC,
            fit_score=max(0, min(100, score)),
            rationale="Growth-stage VCs focus on companies with traction, strong teams, and large markets",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _score_seed_stage_vc(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with seed-stage VCs"""
        score = 0
        alignment = []
        misalignment = []
        
        # Check founder quality (most important for seed)
        founder_score = analysis_data.get("founder_readiness_score", 50)
        if founder_score >= 70:
            score += 35
            alignment.append("Strong founder with relevant experience")
        elif founder_score >= 50:
            score += 20
        else:
            misalignment.append("Weak founder for early-stage")
            score -= 10
        
        # Check market opportunity
        tam = analysis_data.get("tam_estimate_usd", 0)
        if tam >= 10_000_000:
            score += 25
            alignment.append("Large addressable market")
        elif tam >= 1_000_000:
            score += 15
        else:
            misalignment.append("Market too small for VC")
        
        # Check product stage
        product_stage = analysis_data.get("product_stage", "").lower()
        if "mvp" in product_stage or "beta" in product_stage:
            score += 20
            alignment.append("Has MVP/beta product")
        elif "idea" in product_stage or "concept" in product_stage:
            score += 5
            misalignment.append("Still in idea stage")
        
        # Check growth rate
        growth_rate = analysis_data.get("growth_rate_percent", 0)
        if growth_rate >= 10:
            score += 10
            alignment.append("Strong market growth")
        
        return InvestorFitScore(
            investor_type=InvestorType.SEED_STAGE_VC,
            fit_score=max(0, min(100, score)),
            rationale="Seed VCs focus on founders and large markets, less concerned with current traction",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _score_crypto_specialist(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with crypto/Web3 specialists"""
        score = 0
        alignment = []
        misalignment = []
        
        # Check if it's crypto/Web3
        if analysis_data.get("token_utility_analysis"):
            score += 30
            alignment.append("Has tokenomics strategy")
        else:
            misalignment.append("No token/crypto component")
            return InvestorFitScore(
                investor_type=InvestorType.CRYPTO_SPECIALIST,
                fit_score=0,
                rationale="Only relevant for crypto/Web3 companies",
                alignment_factors=alignment,
                misalignment_factors=misalignment,
            )
        
        # Check token utility
        token_utility = analysis_data.get("token_utility_strength", "").lower()
        if "strong" in token_utility:
            score += 25
            alignment.append("Strong token utility and economic model")
        elif "moderate" in token_utility:
            score += 10
        else:
            misalignment.append("Weak or unclear token utility")
        
        # Check founder crypto experience
        founder_background = analysis_data.get("founder_backgrounds", [])
        crypto_exp = analysis_data.get("founder_crypto_experience", False)
        if crypto_exp:
            score += 20
            alignment.append("Founder has crypto/Web3 experience")
        else:
            misalignment.append("Limited founder crypto experience")
        
        # Check market/adoption
        community_allocation = analysis_data.get("community_allocation_percent", 0)
        if community_allocation >= 20:
            score += 15
            alignment.append("Significant community allocation shows token distribution")
        
        # Check growth trajectory
        growth_rate = analysis_data.get("growth_rate_percent", 0)
        if growth_rate >= 30:
            score += 10
            alignment.append("High market growth trajectory")
        
        return InvestorFitScore(
            investor_type=InvestorType.CRYPTO_SPECIALIST,
            fit_score=max(0, min(100, score)),
            rationale="Crypto specialists invest in Web3 with strong tokenomics and founder crypto experience",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _score_strategic_corporate(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with strategic corporates"""
        score = 0
        alignment = []
        misalignment = []
        
        # Check for synergy with corporate
        target_market = analysis_data.get("target_market", "").lower()
        if any(ind in target_market for ind in ["enterprise", "b2b", "saas", "workflow", "data"]):
            score += 25
            alignment.append("Enterprise/B2B focus aligns with corporate strategic interests")
        
        # Check product maturity
        product_stage = analysis_data.get("product_stage", "").lower()
        if "beta" in product_stage or "launched" in product_stage or "launched" in product_stage:
            score += 20
            alignment.append("Product is launched and gaining traction")
        elif "mvp" in product_stage:
            score += 10
        else:
            misalignment.append("Product not yet launched")
        
        # Check team capability
        team_size = len(analysis_data.get("team", []))
        if team_size >= 3:
            score += 15
            alignment.append("Capable team for execution")
        else:
            misalignment.append("Team too small for corporate partnership")
        
        # Check competitive positioning
        competitive_advantage = analysis_data.get("competitive_advantage", "").lower()
        if "proprietary" in competitive_advantage or "patent" in competitive_advantage:
            score += 15
            alignment.append("Defensible technology/IP")
        
        return InvestorFitScore(
            investor_type=InvestorType.STRATEGIC_CORPORATE,
            fit_score=max(0, min(100, score)),
            rationale="Strategic investors look for synergies, defensible tech, and execution capability",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _score_angel_investor(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with angel investors"""
        score = 0
        alignment = []
        misalignment = []
        
        # Angels invest in founders first
        founder_score = analysis_data.get("founder_readiness_score", 50)
        if founder_score >= 60:
            score += 40
            alignment.append("Strong founder characteristics")
        else:
            misalignment.append("Founder doesn't meet angel expectations")
        
        # Check for domain expertise or networks
        founder_background = analysis_data.get("founder_backgrounds", [])
        if founder_background:
            score += 15
            alignment.append("Founder has relevant domain expertise")
        
        # Angels are more flexible on stage
        product_stage = analysis_data.get("product_stage", "").lower()
        if "idea" in product_stage or "mvp" in product_stage:
            score += 15
            alignment.append("Early-stage OK for angels")
        
        # Clear vision/story
        summary = analysis_data.get("executive_summary", "")
        if summary and len(summary) > 50:
            score += 10
            alignment.append("Clear founding story and vision")
        
        # Market opportunity
        tam = analysis_data.get("tam_estimate_usd", 0)
        if tam >= 1_000_000:
            score += 15
            alignment.append("Sufficient market opportunity")
        
        return InvestorFitScore(
            investor_type=InvestorType.ANGEL_INVESTOR,
            fit_score=max(0, min(100, score)),
            rationale="Angels invest in founders, domain expertise, and compelling stories",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _score_token_fund(self, analysis_data: Dict[str, Any]) -> InvestorFitScore:
        """Score fit with token funds"""
        score = 0
        alignment = []
        misalignment = []
        
        # Must have token
        if not analysis_data.get("token_utility_analysis"):
            misalignment.append("No token or tokenomics")
            return InvestorFitScore(
                investor_type=InvestorType.TOKEN_FUND,
                fit_score=0,
                rationale="Token funds only invest in projects with tokens",
                alignment_factors=alignment,
                misalignment_factors=misalignment,
            )
        
        # Check token metrics
        circ_supply = analysis_data.get("circulating_supply", 0)
        total_supply = analysis_data.get("total_supply", 0)
        if total_supply > 0:
            score += 20
            alignment.append("Clear token supply mechanics")
        
        # Token health
        token_health = analysis_data.get("token_health", "").lower()
        if "excellent" in token_health or "good" in token_health:
            score += 25
            alignment.append("Strong tokenomics design")
        elif "acceptable" in token_health:
            score += 10
        else:
            misalignment.append("Problematic tokenomics")
        
        # Governance/utility
        is_governance = analysis_data.get("is_governance_token", False)
        is_fee = analysis_data.get("is_fee_token", False)
        if is_governance or is_fee:
            score += 20
            alignment.append("Token has governance or fee capture")
        else:
            misalignment.append("Token utility unclear")
        
        # Community allocation
        community = analysis_data.get("community_allocation_percent", 0)
        if community >= 20:
            score += 15
            alignment.append("Good community/DAO allocation")
        
        return InvestorFitScore(
            investor_type=InvestorType.TOKEN_FUND,
            fit_score=max(0, min(100, score)),
            rationale="Token funds focus on token mechanics, governance, and community allocation",
            alignment_factors=alignment,
            misalignment_factors=misalignment,
        )
    
    def _get_target_profiles(self, scores: List[InvestorFitScore]) -> List[str]:
        """Get target investor profiles based on fit scores"""
        targets = []
        
        for score in scores:
            if score.fit_score >= 70:
                targets.append(f"{score.investor_type.value}: Excellent fit")
            elif score.fit_score >= 50:
                targets.append(f"{score.investor_type.value}: Good fit")
        
        return targets
    
    def _get_positioning_recommendations(
        self,
        investor_type: InvestorType,
        analysis_data: Dict[str, Any]
    ) -> List[str]:
        """Get positioning recommendations for target investor type"""
        recommendations = []
        
        if investor_type == InvestorType.GROWTH_STAGE_VC:
            recommendations.append("Emphasize revenue traction and unit economics")
            recommendations.append("Show clear path to profitability")
            recommendations.append("Highlight market size and expansion potential")
        
        elif investor_type == InvestorType.SEED_STAGE_VC:
            recommendations.append("Lead with founder story and relevant experience")
            recommendations.append("Show strong market opportunity (TAM)")
            recommendations.append("Demonstrate initial traction or MVP")
        
        elif investor_type == InvestorType.CRYPTO_SPECIALIST:
            recommendations.append("Emphasize tokenomics and incentive structure")
            recommendations.append("Show founder crypto/Web3 experience and network")
            recommendations.append("Highlight community building and token distribution")
        
        elif investor_type == InvestorType.STRATEGIC_CORPORATE:
            recommendations.append("Position technology as strategic asset")
            recommendations.append("Emphasize synergies with corporate's existing business")
            recommendations.append("Show defensible IP and technical moat")
        
        elif investor_type == InvestorType.ANGEL_INVESTOR:
            recommendations.append("Focus on compelling founder story and vision")
            recommendations.append("Show passion and domain expertise")
            recommendations.append("Highlight near-term traction milestones")
        
        elif investor_type == InvestorType.TOKEN_FUND:
            recommendations.append("Lead with token economics and supply mechanics")
            recommendations.append("Emphasize governance rights and community benefits")
            recommendations.append("Show path to token utility and value capture")
        
        return recommendations
