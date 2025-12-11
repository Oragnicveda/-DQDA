"""Unit tests for DQDA analyzers"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.analyzers import (
    FounderAnalyzer,
    MarketAnalyzer,
    CompetitionAnalyzer,
    TokenomicsAnalyzer,
)


def test_founder_analyzer():
    """Test founder analyzer"""
    analyzer = FounderAnalyzer()
    
    founder_data = {
        "name": "John Founder",
        "background": "Technical",
        "previous_experience": [
            {
                "company": "Google",
                "role": "Senior Engineer",
                "years": 5,
                "domain": "AI/ML"
            }
        ],
        "previous_exits": [
            {
                "company": "AI Startup",
                "outcome": "Acquired"
            }
        ],
        "team_composition": [
            {
                "name": "Jane Co-founder",
                "role_type": "business",
                "background": "MBA from Stanford"
            }
        ],
        "domain_expertise": "High",
        "achievements": [
            "Shipped product used by 1M users",
            "Scaled team to 50 engineers",
            "Raised $10M Series A"
        ]
    }
    
    result = analyzer.analyze(founder_data)
    
    assert result.overall_score > 0
    assert result.overall_score <= 100
    assert result.experience_score <= 100
    assert result.track_record_score <= 100
    print(f"✓ Founder analyzer test passed (score: {result.overall_score})")


def test_market_analyzer():
    """Test market analyzer"""
    analyzer = MarketAnalyzer()
    
    market_data = {
        "target_market": "Enterprise AI",
        "total_addressable_market": 500_000_000,
        "serviceable_addressable_market": 150_000_000,
        "serviceable_obtainable_market": 50_000_000,
        "market_stage": "Growing",
        "growth_rate": 45,
        "target_segments": ["Healthcare", "Finance", "E-commerce"],
        "market_trends": ["Increasing AI adoption", "Regulatory focus"],
        "regulatory_environment": "Evolving"
    }
    
    result = analyzer.analyze(market_data)
    
    assert result.overall_score > 0
    assert result.overall_score <= 100
    assert result.tam_estimate_usd == 500_000_000
    print(f"✓ Market analyzer test passed (score: {result.overall_score})")


def test_competition_analyzer():
    """Test competition analyzer"""
    analyzer = CompetitionAnalyzer()
    
    competition_data = {
        "company_name": "TechStartup AI",
        "competitive_advantage": "Proprietary ML algorithm",
        "unique_positioning": "Only platform-agnostic solution",
        "direct_competitors": [
            {
                "name": "Competitor A",
                "positioning": "Cloud-native",
                "strengths": ["Established", "Large customer base"],
                "weaknesses": ["Legacy tech"],
                "funding_stage": "Series C",
                "market_share": 15
            }
        ],
        "indirect_competitors": [],
        "potential_new_entrants": ["Google", "Amazon"],
        "competitive_advantage_defensibility": "Strong - Patents protect"
    }
    
    result = analyzer.analyze(competition_data)
    
    assert result.overall_score > 0
    assert result.overall_score <= 100
    assert len(result.direct_competitors) == 1
    print(f"✓ Competition analyzer test passed (score: {result.overall_score})")


def test_tokenomics_analyzer():
    """Test tokenomics analyzer"""
    analyzer = TokenomicsAnalyzer()
    
    tokenomics_data = {
        "token_name": "TechToken",
        "ticker": "TECH",
        "total_supply": 1_000_000_000,
        "circulating_supply": 250_000_000,
        "max_supply": 1_000_000_000,
        "utility_description": "Governance and fee capture",
        "is_governance_token": True,
        "is_fee_token": True,
        "distribution": [
            {
                "recipient": "Team",
                "percentage": 20,
                "vesting_months": 36,
                "lock_months": 12
            },
            {
                "recipient": "Community",
                "percentage": 30,
                "vesting_months": 0
            }
        ],
        "team_allocation": 20,
        "investor_allocation": 25,
        "community_allocation": 30,
        "vesting_schedule": {"monthly_emissions": 0.2}
    }
    
    result = analyzer.analyze(tokenomics_data)
    
    assert result.overall_score > 0
    assert result.overall_score <= 100
    assert result.is_governance_token == True
    assert result.is_fee_token == True
    print(f"✓ Tokenomics analyzer test passed (score: {result.overall_score})")


def run_all_tests():
    """Run all analyzer tests"""
    print("\n" + "="*60)
    print("Running DQDA Analyzer Tests")
    print("="*60 + "\n")
    
    try:
        test_founder_analyzer()
        test_market_analyzer()
        test_competition_analyzer()
        test_tokenomics_analyzer()
        
        print("\n" + "="*60)
        print("✓ All tests passed!")
        print("="*60)
    
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
