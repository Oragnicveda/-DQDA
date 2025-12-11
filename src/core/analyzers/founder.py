"""Founder readiness analysis module"""

from typing import List, Dict, Optional, Any
from ..models.schemas import FounderReadinessScore
from ..models.enums import FounderBackgroundType


class FounderAnalyzer:
    """Analyzes founder readiness and team quality"""
    
    def __init__(self, llm_provider=None):
        """Initialize founder analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, founder_data: Dict[str, Any]) -> FounderReadinessScore:
        """Analyze founder readiness
        
        Args:
            founder_data: Dictionary with founder information
                - name: str
                - background: str
                - previous_experience: List[Dict]
                - previous_exits: List[Dict]
                - team_size: int
                - team_composition: List[Dict]
                - domain_expertise: str
                - education: str
                - achievements: List[str]
        
        Returns:
            FounderReadinessScore with assessment
        """
        # Score individual components
        experience_score = self._score_experience(founder_data)
        track_record_score = self._score_track_record(founder_data)
        execution_capability_score = self._score_execution(founder_data)
        team_completeness_score = self._score_team_completeness(founder_data)
        
        # Calculate weighted overall score
        overall_score = (
            experience_score * 0.25 +
            track_record_score * 0.35 +
            execution_capability_score * 0.30 +
            team_completeness_score * 0.10
        )
        
        # Analyze backgrounds
        backgrounds = self._extract_backgrounds(founder_data)
        
        # Identify strengths and red flags
        strengths = self._identify_strengths(founder_data, backgrounds)
        red_flags = self._identify_red_flags(founder_data)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(overall_score, red_flags)
        
        return FounderReadinessScore(
            overall_score=round(overall_score, 1),
            summary=self._generate_summary(founder_data, overall_score),
            experience_score=round(experience_score, 1),
            track_record_score=round(track_record_score, 1),
            execution_capability_score=round(execution_capability_score, 1),
            team_completeness_score=round(team_completeness_score, 1),
            founder_backgrounds=backgrounds,
            previous_exits=founder_data.get("previous_exits"),
            domain_expertise_level=founder_data.get("domain_expertise", "Unknown"),
            potential_red_flags=red_flags,
            strengths=strengths,
            recommendation=recommendation,
        )
    
    def _score_experience(self, founder_data: Dict[str, Any]) -> float:
        """Score based on relevant experience"""
        score = 50  # baseline
        
        # Years of experience
        prev_exp = founder_data.get("previous_experience", [])
        total_years = sum(exp.get("years", 0) for exp in prev_exp)
        
        if total_years >= 10:
            score += 30
        elif total_years >= 5:
            score += 20
        elif total_years >= 2:
            score += 10
        
        # Relevant experience in domain
        domain = founder_data.get("domain", "").lower()
        for exp in prev_exp:
            exp_domain = exp.get("domain", "").lower()
            if domain in exp_domain or exp_domain in domain:
                score += 15
                break
        
        # Senior roles in previous companies
        for exp in prev_exp:
            role = exp.get("role", "").lower()
            if any(title in role for title in ["cto", "vp", "head", "director", "founder"]):
                score += 10
                break
        
        return min(100, score)
    
    def _score_track_record(self, founder_data: Dict[str, Any]) -> float:
        """Score based on previous successes"""
        score = 50  # baseline
        
        exits = founder_data.get("previous_exits", [])
        
        for exit in exits:
            outcome = exit.get("outcome", "").lower()
            if "acquisition" in outcome or "sold" in outcome:
                score += 30
            elif "profitable" in outcome or "exit" in outcome:
                score += 20
        
        # Revenue/growth in previous roles
        achievements = founder_data.get("achievements", [])
        if any("million" in str(a).lower() or "$" in str(a) for a in achievements):
            score += 15
        
        return min(100, score)
    
    def _score_execution(self, founder_data: Dict[str, Any]) -> float:
        """Score execution capability"""
        score = 50  # baseline
        
        achievements = founder_data.get("achievements", [])
        
        # Number of verified achievements
        if len(achievements) >= 5:
            score += 30
        elif len(achievements) >= 3:
            score += 20
        elif len(achievements) >= 1:
            score += 10
        
        # Evidence of shipping/building
        build_evidence = [a for a in achievements if any(
            word in str(a).lower() for word in ["shipped", "launched", "built", "scaled", "grew"]
        )]
        if build_evidence:
            score += 15
        
        return min(100, score)
    
    def _score_team_completeness(self, founder_data: Dict[str, Any]) -> float:
        """Score team composition and completeness"""
        score = 50  # baseline
        team = founder_data.get("team_composition", [])
        
        team_size = len(team)
        if team_size >= 4:
            score += 25
        elif team_size >= 2:
            score += 15
        elif team_size == 1:
            score += 5
        
        # Skill diversity
        roles = set(member.get("role_type", "").lower() for member in team)
        if "technical" in roles and "business" in roles:
            score += 15
        
        if "operations" in roles or "product" in roles:
            score += 5
        
        return min(100, score)
    
    def _extract_backgrounds(self, founder_data: Dict[str, Any]) -> List[FounderBackgroundType]:
        """Extract founder background types"""
        backgrounds = []
        team = [{"name": founder_data.get("name", "Founder")}] + founder_data.get("team_composition", [])
        
        for member in team:
            role_type = member.get("role_type", "").lower()
            background = member.get("background", "").lower()
            
            if any(word in role_type + background for word in ["engineer", "developer", "cto", "tech"]):
                backgrounds.append(FounderBackgroundType.TECHNICAL)
            elif any(word in role_type + background for word in ["ceo", "founder", "business", "bd", "sales"]):
                backgrounds.append(FounderBackgroundType.BUSINESS)
            elif any(word in role_type + background for word in ["product", "pm"]):
                backgrounds.append(FounderBackgroundType.PRODUCT)
            elif any(word in role_type + background for word in ["ops", "finance", "cfo"]):
                backgrounds.append(FounderBackgroundType.OPERATIONS)
            elif any(word in background for word in ["phd", "research", "professor"]):
                backgrounds.append(FounderBackgroundType.DOMAIN_EXPERT)
            
            if len(member.get("previous_experience", [])) == 0:
                backgrounds.append(FounderBackgroundType.FIRST_TIME)
        
        # Return unique backgrounds
        return list(set(backgrounds)) if backgrounds else [FounderBackgroundType.FIRST_TIME]
    
    def _identify_strengths(self, founder_data: Dict[str, Any], backgrounds: List[FounderBackgroundType]) -> List[str]:
        """Identify founder strengths"""
        strengths = []
        
        # Based on backgrounds
        if FounderBackgroundType.TECHNICAL in backgrounds:
            strengths.append("Technical co-founder with engineering expertise")
        if FounderBackgroundType.BUSINESS in backgrounds:
            strengths.append("Business-focused leader with GTM experience")
        if FounderBackgroundType.DOMAIN_EXPERT in backgrounds:
            strengths.append("Domain expert with deep market knowledge")
        
        # Based on track record
        exits = founder_data.get("previous_exits", [])
        if exits:
            strengths.append(f"{len(exits)} previous successful exits")
        
        # Based on team
        team_size = len(founder_data.get("team_composition", []))
        if team_size >= 3:
            strengths.append("Strong founding team with complementary skills")
        
        if founder_data.get("domain_expertise") == "High":
            strengths.append("Deep expertise in target domain")
        
        return strengths
    
    def _identify_red_flags(self, founder_data: Dict[str, Any]) -> List[str]:
        """Identify potential red flags"""
        flags = []
        
        # Inexperienced founders
        prev_exp = founder_data.get("previous_experience", [])
        total_years = sum(exp.get("years", 0) for exp in prev_exp)
        if total_years == 0:
            flags.append("First-time founder with no previous work experience")
        elif total_years < 2:
            flags.append("Limited professional experience (<2 years)")
        
        # No exits
        if not founder_data.get("previous_exits"):
            flags.append("No previous exits or successful ventures")
        
        # Solo founder
        if not founder_data.get("team_composition"):
            flags.append("Solo founder without co-founding team")
        
        # Lack of domain expertise
        if founder_data.get("domain_expertise") == "Low":
            flags.append("Limited domain expertise in target market")
        
        # Previous failures
        exits = founder_data.get("previous_exits", [])
        failed_exits = [e for e in exits if "failed" in e.get("outcome", "").lower()]
        if len(failed_exits) > 1:
            flags.append("Multiple failed ventures in track record")
        
        return flags
    
    def _generate_summary(self, founder_data: Dict[str, Any], score: float) -> str:
        """Generate summary text"""
        if score >= 80:
            return (f"{founder_data.get('name', 'Founder')} demonstrates strong founder readiness with "
                   "extensive experience, proven track record, and complementary team.")
        elif score >= 60:
            return (f"{founder_data.get('name', 'Founder')} shows good founder readiness but has some "
                   "gaps in experience or track record that should be addressed.")
        elif score >= 40:
            return (f"{founder_data.get('name', 'Founder')} has moderate founder readiness but would "
                   "benefit from additional experience or team building.")
        else:
            return (f"{founder_data.get('name', 'Founder')} appears to lack sufficient experience or "
                   "track record for this type of venture at this stage.")
    
    def _generate_recommendation(self, score: float, red_flags: List[str]) -> str:
        """Generate go/no-go recommendation"""
        if red_flags and any("deal killer" in flag.lower() for flag in red_flags):
            return "NO-GO: Fatal founder/team issues identified"
        elif score >= 75:
            return "STRONG GO: Excellent founder readiness"
        elif score >= 60:
            return "GO: Adequate founder readiness for early stage"
        elif score >= 40:
            return "CAUTIOUS: Marginal founder readiness - consider advisory board/mentorship"
        else:
            return "NO-GO: Insufficient founder readiness at this time"
