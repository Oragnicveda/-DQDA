"""Enumerations for DQDA analysis"""

from enum import Enum


class InvestorType(str, Enum):
    """Types of investors for fit prediction"""
    GROWTH_STAGE_VC = "growth_stage_vc"
    SEED_STAGE_VC = "seed_stage_vc"
    CRYPTO_SPECIALIST = "crypto_specialist"
    STRATEGIC_CORPORATE = "strategic_corporate"
    ANGEL_INVESTOR = "angel_investor"
    TOKEN_FUND = "token_fund"


class WeaknessLevel(str, Enum):
    """Severity levels for identified weaknesses"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class MarketStage(str, Enum):
    """Market development stage"""
    EMERGING = "emerging"
    GROWING = "growing"
    MATURE = "mature"
    DECLINING = "declining"


class FounderBackgroundType(str, Enum):
    """Types of founder background"""
    TECHNICAL = "technical"
    BUSINESS = "business"
    PRODUCT = "product"
    OPERATIONS = "operations"
    DOMAIN_EXPERT = "domain_expert"
    FIRST_TIME = "first_time"


class TokenomicsHealth(str, Enum):
    """Overall health assessment of tokenomics"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    POOR = "poor"
    PROBLEMATIC = "problematic"
