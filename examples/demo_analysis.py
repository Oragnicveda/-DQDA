#!/usr/bin/env python3
"""Demo DQDA analysis with sample data"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.agent import DQDAAgent
from src.core.utils.logging import setup_logging


# Setup logging
logger = setup_logging()


def get_sample_deal_data():
    """Get sample deal data for demo"""
    return {
        "name": "TechVenture AI",
        "founder": {
            "name": "Jane Smith",
            "background": "ML Engineer at Google",
            "previous_experience": [
                {
                    "company": "Google",
                    "role": "Senior ML Engineer",
                    "years": 5,
                    "domain": "AI/ML"
                },
                {
                    "company": "Stanford University",
                    "role": "PhD Researcher",
                    "years": 3,
                    "domain": "Machine Learning"
                }
            ],
            "previous_exits": [
                {
                    "company": "ML Startup Inc",
                    "outcome": "Acquired by Google",
                    "exit_value": 50_000_000
                }
            ],
            "team_composition": [
                {
                    "name": "John Doe",
                    "role_type": "technical",
                    "background": "VP Eng at Facebook",
                    "previous_experience": [
                        {
                            "company": "Facebook",
                            "role": "VP Engineering",
                            "years": 7,
                            "domain": "Distributed Systems"
                        }
                    ]
                },
                {
                    "name": "Alice Johnson",
                    "role_type": "business",
                    "background": "Sales at Salesforce",
                    "previous_experience": [
                        {
                            "company": "Salesforce",
                            "role": "Director of Sales",
                            "years": 4,
                            "domain": "Enterprise Sales"
                        }
                    ]
                }
            ],
            "domain_expertise": "High",
            "achievements": [
                "Published 5 papers in top ML conferences",
                "Developed novel recommendation algorithm",
                "Scaled ML platform to 10M+ users",
                "Raised $5M seed round"
            ]
        },
        "market": {
            "target_market": "Enterprise AI/ML",
            "total_addressable_market": 500_000_000,
            "serviceable_addressable_market": 150_000_000,
            "serviceable_obtainable_market": 50_000_000,
            "market_stage": "Growing",
            "growth_rate": 45,
            "target_segments": [
                "Healthcare AI",
                "Financial Services ML",
                "E-commerce Personalization"
            ],
            "market_trends": [
                "Increasing enterprise adoption of AI",
                "Rising demand for ML talent",
                "Growth in ethical AI compliance"
            ],
            "regulatory_environment": "Evolving with increasing compliance requirements",
            "tam_methodology": "Bottom-up from addressable customer segments"
        },
        "competition": {
            "company_name": "TechVenture AI",
            "competitive_advantage": "Proprietary ML algorithms with 2x faster inference and 95% accuracy",
            "unique_positioning": "Only platform-agnostic ML solution with multi-cloud support",
            "direct_competitors": [
                {
                    "name": "DataSystems Inc",
                    "positioning": "Enterprise ML Platform",
                    "strengths": ["Large customer base", "Established market"],
                    "weaknesses": ["Legacy technology", "High price point"],
                    "funding_stage": "Series C",
                    "market_share": 15
                },
                {
                    "name": "AI Engine Co",
                    "positioning": "Cloud-native ML",
                    "strengths": ["AWS partnership", "Easy integration"],
                    "weaknesses": ["AWS-only", "Limited customization"],
                    "funding_stage": "Series B",
                    "market_share": 8
                }
            ],
            "indirect_competitors": [],
            "potential_new_entrants": ["Amazon", "Google Cloud", "Microsoft Azure"],
            "competitive_advantage_defensibility": "Strong - Protected by patents and continuous R&D"
        },
        "tokenomics": {
            "token_name": "TechVenture Token",
            "ticker": "TECH",
            "total_supply": 1_000_000_000,
            "circulating_supply": 250_000_000,
            "max_supply": 1_000_000_000,
            "utility_description": "Governance token for ML platform decisions and fee capture on compute resources",
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
                    "recipient": "Investors",
                    "percentage": 25,
                    "vesting_months": 24,
                    "lock_months": 6
                },
                {
                    "recipient": "Community",
                    "percentage": 30,
                    "vesting_months": 0,
                    "lock_months": 0
                },
                {
                    "recipient": "Treasury",
                    "percentage": 25,
                    "vesting_months": 0,
                    "lock_months": 0
                }
            ],
            "team_allocation": 20,
            "investor_allocation": 25,
            "community_allocation": 30,
            "vesting_schedule": {
                "monthly_emissions": 0.2
            },
            "inflation_concerns": [],
            "economic_model": "Deflationary with monthly burns from compute fees"
        },
        "technical": {
            "product_stage": "Beta - Early customer pilots",
            "product_market_fit": True,
            "technology_stack": [
                "PyTorch",
                "Kubernetes",
                "PostgreSQL",
                "Go for backend services"
            ],
            "scalability_concerns": [],
            "security_concerns": [],
            "technical_assessment": {
                "architecture_assessment": "Modern microservices architecture",
                "has_automated_testing": True,
                "documentation_exists": True
            },
            "gtm_clarity": "Clear GTM with focus on healthcare and financial services",
            "customer_acquisition": "Enterprise sales with 6-12 month sales cycle",
            "market_messaging": "Purpose-built ML platform for regulated industries",
            "competitive_positioning": "Platform-agnostic with superior performance and governance",
            "revenue_model": "SaaS subscription based on compute usage and support tier",
            "customer_validation": True,
            "pitch_deck_quality": "Professional"
        }
    }


def main():
    """Run demo analysis"""
    print("\n" + "="*70)
    print("DQDA - Deal Qualification & Due Diligence Agent")
    print("Demo Analysis")
    print("="*70)
    
    # Create agent
    agent = DQDAAgent()
    
    # Get sample data
    deal_data = get_sample_deal_data()
    
    # Run analysis
    result = agent.analyze(deal_data)
    
    # Print results
    print_analysis_results(result)
    
    # Optionally save to JSON
    save_results_to_json(result, "analysis_result.json")


def print_analysis_results(result):
    """Print formatted analysis results"""
    print("\n" + "="*70)
    print("ANALYSIS RESULTS")
    print("="*70)
    
    print(f"\nDeal: {result.deal_name}")
    print(f"Date: {result.analysis_date.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "-"*70)
    print("OVERALL ASSESSMENT")
    print("-"*70)
    print(f"Quality Score: {result.overall_deal_quality_score}/100")
    print(f"Recommendation: {result.investment_recommendation}")
    
    print("\n" + "-"*70)
    print("COMPONENT SCORES")
    print("-"*70)
    print(f"Founder Readiness: {result.founder_readiness.overall_score}/100")
    print(f"  Recommendation: {result.founder_readiness.recommendation}")
    print(f"Market Analysis: {result.market_analysis.overall_score}/100")
    print(f"  TAM: ${result.market_analysis.tam_estimate_usd/1e6:.0f}M")
    print(f"Competition: {result.competition_analysis.overall_score}/100")
    print(f"Token Utility: {result.token_utility_analysis.overall_score}/100")
    print(f"  Health: {result.token_utility_analysis.token_health.value}")
    print(f"Investor Fit: {result.investor_fit.best_fit_score}/100")
    print(f"  Best Fit: {result.investor_fit.best_fit_investor_type.value}")
    
    print("\n" + "-"*70)
    print("KEY STRENGTHS")
    print("-"*70)
    for i, strength in enumerate(result.key_strengths[:5], 1):
        print(f"{i}. {strength}")
    
    print("\n" + "-"*70)
    print("KEY CONCERNS")
    print("-"*70)
    if result.key_concerns:
        for i, concern in enumerate(result.key_concerns[:5], 1):
            print(f"{i}. {concern}")
    else:
        print("No major concerns identified.")
    
    print("\n" + "-"*70)
    print("CRITICAL ISSUES")
    print("-"*70)
    if result.weakness_analysis.deal_killers:
        for killer in result.weakness_analysis.deal_killers:
            print(f"⚠️  {killer}")
    else:
        print("No deal-killer issues identified.")
    
    print("\n" + "-"*70)
    print("IMMEDIATE ACTION ITEMS")
    print("-"*70)
    if result.immediate_action_items:
        for i, item in enumerate(result.immediate_action_items, 1):
            print(f"{i}. {item}")
    else:
        print("No critical action items required.")
    
    print("\n" + "-"*70)
    print("EXECUTIVE SUMMARY")
    print("-"*70)
    print(result.executive_summary)
    
    print("\n" + "="*70)


def save_results_to_json(result, filename: str):
    """Save analysis results to JSON file"""
    try:
        result_dict = result.model_dump(mode='json')
        with open(filename, 'w') as f:
            json.dump(result_dict, f, indent=2, default=str)
        print(f"\n✓ Results saved to {filename}")
    except Exception as e:
        print(f"\n✗ Error saving results: {e}")


if __name__ == "__main__":
    main()
