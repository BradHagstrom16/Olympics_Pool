"""
2026 Milano-Cortina Winter Olympics Pool - Configuration
=========================================================
All game settings, scoring rules, and application configuration.
"""

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from data.countries import COUNTRIES_BY_TIER, EXCLUDED_COUNTRIES

# Base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# =============================================================================
# TIMEZONE CONFIGURATION
# =============================================================================

TIMEZONE = ZoneInfo("America/Chicago")  # Central Time

# =============================================================================
# GAME CONFIGURATION
# =============================================================================

# Key dates
OLYMPICS_START = datetime(2026, 2, 6, tzinfo=TIMEZONE)
OLYMPICS_END = datetime(2026, 2, 22, 23, 59, 59, tzinfo=TIMEZONE)
PICK_DEADLINE = datetime(2026, 2, 6, 23, 59, 59, tzinfo=TIMEZONE)  # 11:59 PM CT

# Scoring: Medal base points (before tier multiplier)
MEDAL_POINTS = {
    'gold': 3,
    'silver': 2,
    'bronze': 1,
}

# Tier configuration
# Format: tier_number -> (name, multiplier, picks_required)
TIERS = {
    1: {'name': 'Elite', 'multiplier': 1, 'picks': 1},
    2: {'name': 'Strong', 'multiplier': 2, 'picks': 2},
    3: {'name': 'Competitive', 'multiplier': 3, 'picks': 1},
    4: {'name': 'Emerging', 'multiplier': 6, 'picks': 1},
    5: {'name': 'Occasional', 'multiplier': 10, 'picks': 1},
    6: {'name': 'Wildcard', 'multiplier': 20, 'picks': 2},
}

# Total picks required
TOTAL_PICKS = sum(tier['picks'] for tier in TIERS.values())  # = 8

# Points per medal by tier (calculated from base points × multiplier)
def get_medal_points(tier: int, medal_type: str) -> int:
    """Calculate points for a medal based on tier and medal type."""
    base = MEDAL_POINTS.get(medal_type.lower(), 0)
    multiplier = TIERS.get(tier, {}).get('multiplier', 1)
    return base * multiplier

# Tier 6 warning message
TIER_6_WARNING = """
⚠️ Wildcard Tier Notice
Not all countries in Tier 6 have recent Olympic medal history. 
Countries marked with ⚪ have not won a medal in the last four 
Winter Olympics (2010–2022). Choose wisely—or boldly.
"""


# =============================================================================
# FLASK CONFIGURATION
# =============================================================================

class Config:
    """Base Flask configuration."""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'olympics_pool.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30  # 30 days
    
    # App settings
    APP_NAME = "2026 Milano-Cortina Winter Olympics Pool"
    APP_SHORT_NAME = "Olympics Pool"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
