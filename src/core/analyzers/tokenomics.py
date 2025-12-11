"""Tokenomics analysis module"""

from typing import Dict, Any, List
from ..models.schemas import TokenUtilityAnalysis, TokenDistribution
from ..models.enums import TokenomicsHealth


class TokenomicsAnalyzer:
    """Analyzes token utility and tokenomics"""
    
    def __init__(self, llm_provider=None):
        """Initialize tokenomics analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, tokenomics_data: Dict[str, Any]) -> TokenUtilityAnalysis:
        """Analyze tokenomics and token utility
        
        Args:
            tokenomics_data: Dictionary with tokenomics information
                - token_name: str
                - ticker: str
                - total_supply: float
                - circulating_supply: float
                - max_supply: float
                - utility_description: str
                - is_governance_token: bool
                - is_fee_token: bool
                - distribution: List[Dict]
                - team_allocation: float
                - investor_allocation: float
                - community_allocation: float
                - vesting_schedule: Dict
                - inflation_concerns: List[str]
        
        Returns:
            TokenUtilityAnalysis with assessment
        """
        # Score components
        utility_score = self._score_utility(tokenomics_data)
        distribution_score = self._score_distribution(tokenomics_data)
        vesting_score = self._score_vesting(tokenomics_data)
        incentive_score = self._score_incentive_alignment(tokenomics_data)
        
        # Calculate overall score
        overall_score = (
            utility_score * 0.35 +
            distribution_score * 0.25 +
            vesting_score * 0.20 +
            incentive_score * 0.20
        )
        
        # Determine health
        health = self._determine_health(overall_score)
        
        # Identify concerns
        inflation_concerns = self._identify_inflation_concerns(tokenomics_data)
        concentration_risks = self._identify_concentration_risks(tokenomics_data)
        vesting_concerns = self._identify_vesting_concerns(tokenomics_data)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(health, overall_score)
        
        # Process distribution data
        distribution = [
            TokenDistribution(
                recipient=dist.get("recipient", "Unknown"),
                percentage=dist.get("percentage", 0),
                vesting_period_months=dist.get("vesting_months"),
                lock_period_months=dist.get("lock_months"),
            )
            for dist in tokenomics_data.get("distribution", [])
        ]
        
        return TokenUtilityAnalysis(
            overall_score=round(overall_score, 1),
            summary=self._generate_summary(tokenomics_data, overall_score),
            token_health=health,
            token_name=tokenomics_data.get("token_name", "Unknown"),
            ticker=tokenomics_data.get("ticker", ""),
            total_supply=tokenomics_data.get("total_supply", 0),
            circulating_supply=tokenomics_data.get("circulating_supply", 0),
            max_supply=tokenomics_data.get("max_supply"),
            utility_description=tokenomics_data.get("utility_description", "Not specified"),
            utility_strength=self._assess_utility_strength(tokenomics_data),
            is_governance_token=tokenomics_data.get("is_governance_token", False),
            is_fee_token=tokenomics_data.get("is_fee_token", False),
            distribution=distribution,
            team_allocation_percent=tokenomics_data.get("team_allocation", 0),
            investor_allocation_percent=tokenomics_data.get("investor_allocation", 0),
            community_allocation_percent=tokenomics_data.get("community_allocation", 0),
            inflation_concerns=inflation_concerns,
            concentration_risks=concentration_risks,
            vesting_concerns=vesting_concerns,
            recommendation=recommendation,
        )
    
    def _score_utility(self, tokenomics_data: Dict[str, Any]) -> float:
        """Score token utility and use cases"""
        score = 50  # baseline
        
        utility = tokenomics_data.get("utility_description", "").lower()
        
        # Utility clarity
        if utility and len(utility) > 30:
            score += 15
        
        # Multiple use cases
        if any(word in utility for word in ["fee", "stake", "govern", "vote"]):
            score += 10
        if utility.count(",") >= 2:  # Multiple use cases indicated
            score += 10
        
        # Governance
        if tokenomics_data.get("is_governance_token"):
            score += 15
        
        # Fee capture
        if tokenomics_data.get("is_fee_token"):
            score += 15
        
        # Staking/economic model
        if "stake" in utility or "earn" in utility:
            score += 15
        
        # Weakness: no real utility
        if not utility or utility in ["store of value", "speculative"]:
            score -= 25
        
        return max(0, min(100, score))
    
    def _score_distribution(self, tokenomics_data: Dict[str, Any]) -> float:
        """Score fairness and health of token distribution"""
        score = 50  # baseline
        
        # Get allocations
        team = tokenomics_data.get("team_allocation", 0)
        investor = tokenomics_data.get("investor_allocation", 0)
        community = tokenomics_data.get("community_allocation", 0)
        
        # Balanced distribution is good
        if community >= 40:
            score += 20
        elif community >= 20:
            score += 10
        elif community < 5:
            score -= 20
        
        # Team allocation assessment
        if 15 <= team <= 30:
            score += 15
        elif team > 40:
            score -= 15
        elif team < 5:
            score -= 10
        
        # Investor allocation
        if investor <= 30:
            score += 10
        elif investor > 50:
            score -= 20
        
        # Concentration check
        if team + investor > 70:
            score -= 15  # Too concentrated to team/investors
        
        return max(0, min(100, score))
    
    def _score_vesting(self, tokenomics_data: Dict[str, Any]) -> float:
        """Score vesting schedule appropriateness"""
        score = 50  # baseline
        
        distribution = tokenomics_data.get("distribution", [])
        vesting_schedule = tokenomics_data.get("vesting_schedule", {})
        
        # Check for vesting
        if distribution:
            with_vesting = sum(1 for d in distribution if d.get("vesting_months", 0) > 0)
            if with_vesting > len(distribution) / 2:
                score += 20
            else:
                score -= 10
        
        # Check vesting lengths
        for dist in distribution:
            vesting = dist.get("vesting_months", 0)
            if 12 <= vesting <= 48:  # 1-4 years reasonable
                score += 5
            elif vesting > 0:
                score -= 5
        
        # Lock periods
        for dist in distribution:
            lock = dist.get("lock_months", 0)
            if lock > 0:
                score += 5
        
        # Team vesting critical
        team_dist = [d for d in distribution if "team" in str(d.get("recipient", "")).lower()]
        if team_dist:
            for td in team_dist:
                vesting = td.get("vesting_months", 0)
                if vesting < 12:
                    score -= 25
                elif vesting < 24:
                    score -= 10
        
        return max(0, min(100, score))
    
    def _score_incentive_alignment(self, tokenomics_data: Dict[str, Any]) -> float:
        """Score incentive alignment and mechanism design"""
        score = 50  # baseline
        
        utility = tokenomics_data.get("utility_description", "").lower()
        
        # Burn mechanism
        if "burn" in utility or tokenomics_data.get("has_burn_mechanism"):
            score += 15
        
        # Stake rewards
        if "stake" in utility or "reward" in utility:
            score += 15
        
        # Deflationary mechanism
        if "deflationary" in utility or "deflation" in tokenomics_data.get("economic_model", "").lower():
            score += 10
        
        # Supply control
        max_supply = tokenomics_data.get("max_supply")
        if max_supply and max_supply > 0:
            score += 10
        
        # Founder incentive alignment
        team_vesting = tokenomics_data.get("team_vesting_months", 0)
        if team_vesting >= 24:
            score += 15
        
        return min(100, score)
    
    def _determine_health(self, overall_score: float) -> TokenomicsHealth:
        """Determine overall tokenomics health"""
        if overall_score >= 80:
            return TokenomicsHealth.EXCELLENT
        elif overall_score >= 65:
            return TokenomicsHealth.GOOD
        elif overall_score >= 50:
            return TokenomicsHealth.ACCEPTABLE
        elif overall_score >= 35:
            return TokenomicsHealth.POOR
        else:
            return TokenomicsHealth.PROBLEMATIC
    
    def _assess_utility_strength(self, tokenomics_data: Dict[str, Any]) -> str:
        """Assess strength of token utility"""
        utility = tokenomics_data.get("utility_description", "").lower()
        is_gov = tokenomics_data.get("is_governance_token", False)
        is_fee = tokenomics_data.get("is_fee_token", False)
        
        if is_gov and is_fee:
            return "Strong - Governance and fee capture"
        elif is_fee:
            return "Strong - Direct fee capture mechanism"
        elif is_gov:
            return "Moderate - Governance only"
        elif "stake" in utility:
            return "Moderate - Staking incentive mechanism"
        elif "utility" in utility or "use" in utility:
            return "Weak - Limited utility beyond speculation"
        else:
            return "Weak - No clear utility identified"
    
    def _identify_inflation_concerns(self, tokenomics_data: Dict[str, Any]) -> List[str]:
        """Identify inflation and supply concerns"""
        concerns = []
        
        circ = tokenomics_data.get("circulating_supply", 0)
        total = tokenomics_data.get("total_supply", 0)
        max_supply = tokenomics_data.get("max_supply", 0)
        
        if max_supply == 0:
            concerns.append("No maximum supply cap - unlimited inflation possible")
        
        if total and circ and total > 0:
            circulation_ratio = circ / total
            if circulation_ratio < 0.1:
                concerns.append(f"Only {circulation_ratio*100:.1f}% circulating - high future dilution expected")
        
        # Check for high emission schedules
        vesting_data = tokenomics_data.get("vesting_schedule", {})
        if "monthly_emissions" in vesting_data:
            monthly = vesting_data.get("monthly_emissions", 0)
            if monthly > 0.5:  # >0.5% monthly
                concerns.append("High monthly token emissions may cause continuous selling pressure")
        
        return concerns
    
    def _identify_concentration_risks(self, tokenomics_data: Dict[str, Any]) -> List[str]:
        """Identify token concentration risks"""
        risks = []
        
        team = tokenomics_data.get("team_allocation", 0)
        investor = tokenomics_data.get("investor_allocation", 0)
        
        if team > 30:
            risks.append(f"High team allocation ({team}%) creates sell pressure risk")
        
        if investor > 40:
            risks.append(f"High investor allocation ({investor}%) may lead to lock-up expiry dumps")
        
        # Check top holder concentration
        distribution = tokenomics_data.get("distribution", [])
        if distribution:
            sorted_dist = sorted(distribution, key=lambda x: x.get("percentage", 0), reverse=True)
            top_3_pct = sum(d.get("percentage", 0) for d in sorted_dist[:3])
            if top_3_pct > 60:
                risks.append(f"Top 3 holders control {top_3_pct:.1f}% - high concentration risk")
        
        return risks
    
    def _identify_vesting_concerns(self, tokenomics_data: Dict[str, Any]) -> List[str]:
        """Identify vesting schedule concerns"""
        concerns = []
        
        distribution = tokenomics_data.get("distribution", [])
        
        # Check for immediate release
        immediate_release = [d for d in distribution if d.get("vesting_months", 0) == 0]
        if immediate_release:
            pct = sum(d.get("percentage", 0) for d in immediate_release)
            if pct > 30:
                concerns.append(f"{pct:.1f}% released immediately - immediate sell pressure")
        
        # Check for cliff vesting (release all at once)
        cliff_vesting = [d for d in distribution if d.get("vesting_months", 0) > 0 and d.get("cliff_months") == d.get("vesting_months")]
        if cliff_vesting:
            pct = sum(d.get("percentage", 0) for d in cliff_vesting)
            if pct > 20:
                concerns.append(f"{pct:.1f}% uses cliff vesting - may cause price shock at unlock")
        
        # Team vesting
        team_dist = [d for d in distribution if "team" in str(d.get("recipient", "")).lower()]
        for td in team_dist:
            vesting = td.get("vesting_months", 0)
            if vesting == 0:
                concerns.append("Team tokens have no vesting - poor incentive alignment")
            elif vesting < 24:
                concerns.append(f"Team vesting only {vesting} months - short commitment")
        
        return concerns
    
    def _generate_recommendation(self, health: TokenomicsHealth, score: float) -> str:
        """Generate tokenomics viability recommendation"""
        if health == TokenomicsHealth.EXCELLENT:
            return "Strong tokenomics with good utility, fair distribution, and proper incentive alignment"
        elif health == TokenomicsHealth.GOOD:
            return "Solid tokenomics but review for potential improvements in utility or vesting"
        elif health == TokenomicsHealth.ACCEPTABLE:
            return "Acceptable tokenomics but address key concerns before investment"
        elif health == TokenomicsHealth.POOR:
            return "Weak tokenomics - significant issues must be resolved. Consider rework before investing"
        else:
            return "Problematic tokenomics - major red flags present. Do not invest without substantial changes"
    
    def _generate_summary(self, tokenomics_data: Dict[str, Any], score: float) -> str:
        """Generate summary text"""
        token = tokenomics_data.get("token_name", "Token")
        utility = tokenomics_data.get("is_governance_token") or tokenomics_data.get("is_fee_token")
        
        if score >= 75:
            util_desc = "governance and fee capture" if utility else "defined utility"
            return (f"{token} demonstrates strong tokenomics with clear {util_desc}, "
                   "fair distribution, and appropriate vesting schedules.")
        elif score >= 60:
            return (f"{token} has reasonable tokenomics but review distribution and vesting "
                   "schedules for potential improvements.")
        elif score >= 40:
            return (f"{token} tokenomics need improvement. Address concerns around utility clarity, "
                   "distribution fairness, and vesting alignment.")
        else:
            return (f"{token} has significant tokenomics issues. Major concerns around inflation potential, "
                   "concentration, and incentive alignment.")
