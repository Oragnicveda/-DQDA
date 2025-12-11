"""Configuration management for DQDA"""

import os
import yaml
from typing import Dict, Any


def load_config(config_path: str = "config/settings.yaml") -> Dict[str, Any]:
    """Load configuration from YAML file
    
    Args:
        config_path: Path to config file
    
    Returns:
        Configuration dictionary
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    # Return default config if file doesn't exist
    return get_default_config()


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        "analysis": {
            "founder_weight": 0.25,
            "market_weight": 0.25,
            "competition_weight": 0.15,
            "tokenomics_weight": 0.15,
            "technical_weight": 0.15,
            "investor_fit_weight": 0.05,
        },
        "scoring": {
            "excellent_threshold": 80,
            "good_threshold": 65,
            "acceptable_threshold": 50,
            "poor_threshold": 35,
        },
        "extractors": {
            "pdf_timeout": 30,
            "max_file_size_mb": 50,
        },
        "llm": {
            "provider": "openai",
            "model": "gpt-4",
            "temperature": 0.3,
        },
    }
