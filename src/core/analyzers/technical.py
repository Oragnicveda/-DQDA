"""Technical and narrative weakness analysis module"""

from typing import Dict, Any, List
from ..models.schemas import WeaknessAnalysis, Weakness
from ..models.enums import WeaknessLevel


class TechnicalAnalyzer:
    """Analyzes technical and narrative weaknesses"""
    
    def __init__(self, llm_provider=None):
        """Initialize technical analyzer
        
        Args:
            llm_provider: LLM provider for enhanced analysis
        """
        self.llm = llm_provider
    
    def analyze(self, weakness_data: Dict[str, Any]) -> WeaknessAnalysis:
        """Analyze technical and narrative weaknesses
        
        Args:
            weakness_data: Dictionary with weakness information
                - technical_assessment: Dict
                - narrative_assessment: Dict
                - product_stage: str
                - technology_stack: List[str]
                - scalability_concerns: List[str]
                - security_concerns: List[str]
                - gtm_clarity: str
                - customer_acquisition: str
                - market_messaging: str
        
        Returns:
            WeaknessAnalysis with detailed findings
        """
        # Extract technical weaknesses
        technical_weaknesses = self._identify_technical_weaknesses(weakness_data)
        
        # Extract narrative weaknesses
        narrative_weaknesses = self._identify_narrative_weaknesses(weakness_data)
        
        # Count severity levels
        critical_count = sum(1 for w in technical_weaknesses + narrative_weaknesses 
                            if w.severity == WeaknessLevel.CRITICAL)
        high_count = sum(1 for w in technical_weaknesses + narrative_weaknesses 
                        if w.severity == WeaknessLevel.HIGH)
        
        # Determine overall risk
        risk_assessment = self._assess_overall_risk(technical_weaknesses, narrative_weaknesses)
        
        # Identify deal killers
        deal_killers = self._identify_deal_killers(technical_weaknesses, narrative_weaknesses)
        
        return WeaknessAnalysis(
            technical_summary=self._generate_technical_summary(technical_weaknesses),
            narrative_summary=self._generate_narrative_summary(narrative_weaknesses),
            technical_weaknesses=technical_weaknesses,
            narrative_weaknesses=narrative_weaknesses,
            total_critical_issues=critical_count,
            total_high_issues=high_count,
            overall_risk_assessment=risk_assessment,
            deal_killers=deal_killers,
        )
    
    def _identify_technical_weaknesses(self, weakness_data: Dict[str, Any]) -> List[Weakness]:
        """Identify technical weaknesses"""
        weaknesses = []
        
        tech_assessment = weakness_data.get("technical_assessment", {})
        
        # Product stage assessment
        product_stage = weakness_data.get("product_stage", "").lower()
        if "idea" in product_stage:
            weaknesses.append(Weakness(
                category="Product Stage",
                issue="Product is still in concept/idea stage with no MVP or prototype",
                severity=WeaknessLevel.CRITICAL,
                impact="Unable to validate product-market fit or technical feasibility",
                remediation="Build MVP and validate with early customers",
            ))
        elif "early" in product_stage or "alpha" in product_stage:
            weaknesses.append(Weakness(
                category="Product Stage",
                issue="Product is in early alpha stage with limited features",
                severity=WeaknessLevel.HIGH,
                impact="Risk of significant pivots required based on customer feedback",
                remediation="Accelerate user feedback loop and iterate quickly",
            ))
        
        # Scalability concerns
        scalability = weakness_data.get("scalability_concerns", [])
        for concern in scalability:
            weaknesses.append(Weakness(
                category="Scalability",
                issue=concern,
                severity=WeaknessLevel.HIGH,
                impact="May not be able to scale to enterprise usage patterns",
                remediation="Address architectural limitations and implement scalability improvements",
            ))
        
        # Security concerns
        security = weakness_data.get("security_concerns", [])
        for concern in security:
            weaknesses.append(Weakness(
                category="Security",
                issue=concern,
                severity=WeaknessLevel.CRITICAL,
                impact="Risk of data breach, loss of customer trust, regulatory issues",
                remediation="Conduct security audit and implement recommended fixes",
            ))
        
        # Technology stack outdated
        tech_stack = weakness_data.get("technology_stack", [])
        outdated = [t for t in tech_stack if self._is_outdated_tech(t)]
        if outdated:
            weaknesses.append(Weakness(
                category="Technology Stack",
                issue=f"Using outdated technologies: {', '.join(outdated)}",
                severity=WeaknessLevel.MEDIUM,
                impact="Difficulty attracting engineering talent, potential security vulnerabilities",
                remediation="Plan technology migration or rebuild with modern stack",
            ))
        
        # Architecture concerns
        arch_assessment = tech_assessment.get("architecture_assessment", "").lower()
        if "monolithic" in arch_assessment:
            weaknesses.append(Weakness(
                category="Architecture",
                issue="Monolithic architecture may limit scalability and deployment flexibility",
                severity=WeaknessLevel.MEDIUM,
                impact="Difficulty scaling individual components and managing deployments",
                remediation="Plan migration to microservices or modular architecture",
            ))
        
        # Testing/QA gaps
        if not tech_assessment.get("has_automated_testing"):
            weaknesses.append(Weakness(
                category="Quality Assurance",
                issue="Limited or no automated testing infrastructure",
                severity=WeaknessLevel.MEDIUM,
                impact="Risk of regressions and bugs reaching production",
                remediation="Implement comprehensive automated testing (unit, integration, e2e)",
            ))
        
        # Documentation
        if not tech_assessment.get("documentation_exists"):
            weaknesses.append(Weakness(
                category="Documentation",
                issue="Limited API, architecture, or code documentation",
                severity=WeaknessLevel.LOW,
                impact="Difficulty onboarding new engineers and maintaining code quality",
                remediation="Build comprehensive documentation",
            ))
        
        return weaknesses
    
    def _identify_narrative_weaknesses(self, weakness_data: Dict[str, Any]) -> List[Weakness]:
        """Identify narrative/business weaknesses"""
        weaknesses = []
        
        narrative = weakness_data.get("narrative_assessment", {})
        
        # GTM clarity
        gtm = weakness_data.get("gtm_clarity", "").lower()
        if not gtm or "unclear" in gtm or "not defined" in gtm:
            weaknesses.append(Weakness(
                category="Go-To-Market",
                issue="Go-to-market strategy is unclear or not well-defined",
                severity=WeaknessLevel.CRITICAL,
                impact="Unable to assess customer acquisition path or revenue potential",
                remediation="Define clear GTM strategy with customer segments, channels, and unit economics",
            ))
        
        # Customer acquisition
        ca = weakness_data.get("customer_acquisition", "").lower()
        if "expensive" in ca or "unclear" in ca:
            weaknesses.append(Weakness(
                category="Customer Acquisition",
                issue="Customer acquisition strategy or economics are unclear",
                severity=WeaknessLevel.HIGH,
                impact="Risk of unit economics not supporting profitability at scale",
                remediation="Validate CAC, LTV, and payback period through customer interviews and pilots",
            ))
        
        # Market messaging
        messaging = weakness_data.get("market_messaging", "").lower()
        if not messaging or len(messaging) < 20:
            weaknesses.append(Weakness(
                category="Market Messaging",
                issue="Market positioning and value proposition are not clearly articulated",
                severity=WeaknessLevel.HIGH,
                impact="Difficulty getting customers and investors to understand the offering",
                remediation="Develop clear positioning and messaging that resonates with target customers",
            ))
        
        # Competitive positioning
        if not weakness_data.get("competitive_positioning"):
            weaknesses.append(Weakness(
                category="Competition",
                issue="Competitive positioning and differentiation are not well-articulated",
                severity=WeaknessLevel.HIGH,
                impact="At risk of being seen as 'me-too' competitor without clear edge",
                remediation="Identify and communicate specific competitive advantages",
            ))
        
        # Revenue model clarity
        revenue_model = weakness_data.get("revenue_model", "").lower()
        if not revenue_model or "unclear" in revenue_model:
            weaknesses.append(Weakness(
                category="Business Model",
                issue="Revenue model is unclear or not sustainable at scale",
                severity=WeaknessLevel.HIGH,
                impact="Difficulty achieving financial sustainability and path to profitability",
                remediation="Define clear revenue model with unit economics and scalability",
            ))
        
        # Customer validation
        if not weakness_data.get("customer_validation"):
            weaknesses.append(Weakness(
                category="Customer Validation",
                issue="Limited or no customer validation of product-market fit",
                severity=WeaknessLevel.CRITICAL,
                impact="High risk that product doesn't solve real customer problems at scale",
                remediation="Conduct extensive customer interviews and pilots to validate demand",
            ))
        
        # Pitch deck quality
        if weakness_data.get("pitch_deck_quality") == "Poor":
            weaknesses.append(Weakness(
                category="Pitch Materials",
                issue="Pitch deck or materials are unclear or unprofessional",
                severity=WeaknessLevel.MEDIUM,
                impact="Poor impression with investors may lead to pass decisions",
                remediation="Hire experienced pitch deck designer or use pitch deck template",
            ))
        
        return weaknesses
    
    def _is_outdated_tech(self, tech: str) -> bool:
        """Check if a technology is outdated"""
        outdated_techs = [
            "flash", "silverlight", "ie6", "ie7", "ie8",
            "python2", "python 2", "django 1", "rails 2",
            "jsp", "asp.net classic", "cold fusion", "cfml"
        ]
        return any(old in tech.lower() for old in outdated_techs)
    
    def _assess_overall_risk(
        self,
        technical_weaknesses: List[Weakness],
        narrative_weaknesses: List[Weakness]
    ) -> str:
        """Assess overall risk level"""
        critical_count = sum(1 for w in technical_weaknesses + narrative_weaknesses 
                            if w.severity == WeaknessLevel.CRITICAL)
        high_count = sum(1 for w in technical_weaknesses + narrative_weaknesses 
                        if w.severity == WeaknessLevel.HIGH)
        
        if critical_count > 0:
            return "High - Critical issues must be resolved before investment"
        elif high_count >= 3:
            return "High - Multiple significant issues require attention"
        elif high_count >= 1:
            return "Medium - Some significant issues but addressable"
        else:
            return "Low - Minor issues typical for stage"
    
    def _identify_deal_killers(
        self,
        technical_weaknesses: List[Weakness],
        narrative_weaknesses: List[Weakness]
    ) -> List[str]:
        """Identify deal-killer issues"""
        deal_killers = []
        
        for weakness in technical_weaknesses + narrative_weaknesses:
            if weakness.severity == WeaknessLevel.CRITICAL:
                deal_killers.append(f"{weakness.category}: {weakness.issue}")
        
        return deal_killers
    
    def _generate_technical_summary(self, weaknesses: List[Weakness]) -> str:
        """Generate technical weaknesses summary"""
        if not weaknesses:
            return "No significant technical weaknesses identified."
        
        critical = [w for w in weaknesses if w.severity == WeaknessLevel.CRITICAL]
        high = [w for w in weaknesses if w.severity == WeaknessLevel.HIGH]
        
        summary = f"Identified {len(weaknesses)} technical issues: "
        
        if critical:
            summary += f"{len(critical)} critical (product stage, security, scalability), "
        if high:
            summary += f"{len(high)} high-severity "
        
        summary += "that require attention."
        return summary
    
    def _generate_narrative_summary(self, weaknesses: List[Weakness]) -> str:
        """Generate narrative weaknesses summary"""
        if not weaknesses:
            return "No significant narrative or business model weaknesses identified."
        
        critical = [w for w in weaknesses if w.severity == WeaknessLevel.CRITICAL]
        high = [w for w in weaknesses if w.severity == WeaknessLevel.HIGH]
        
        summary = f"Identified {len(weaknesses)} narrative issues: "
        
        if critical:
            summary += f"{len(critical)} critical (GTM clarity, customer validation), "
        if high:
            summary += f"{len(high)} high-severity (competitive positioning, revenue model) "
        
        summary += "that require clarification and refinement."
        return summary
