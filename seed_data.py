"""
2026 Milano-Cortina Winter Olympics Pool - Seed Data
=====================================================
Script to populate the database with initial country data.

Usage:
    python seed_data.py          # Seed all countries
    python seed_data.py --reset  # Clear and re-seed
"""

import sys
from app import app, db
from models import Country, GameState

# =============================================================================
# COUNTRY DATA BY TIER
# =============================================================================

# Format: (IOC code, name, has_medaled_2010_2022)

TIER_1_COUNTRIES = [
    ('NOR', 'Norway', True),
    ('GER', 'Germany', True),
    ('USA', 'United States', True),
    ('CAN', 'Canada', True),
]

TIER_2_COUNTRIES = [
    ('NED', 'Netherlands', True),
    ('AUT', 'Austria', True),
    ('SWE', 'Sweden', True),
    ('FRA', 'France', True),
    ('SUI', 'Switzerland', True),
    ('KOR', 'South Korea', True),
]

TIER_3_COUNTRIES = [
    ('CHN', 'China', True),
    ('JPN', 'Japan', True),
    ('ITA', 'Italy', True),  # 2026 Host!
]

TIER_4_COUNTRIES = [
    ('FIN', 'Finland', True),
    ('CZE', 'Czech Republic', True),
    ('SLO', 'Slovenia', True),
]

TIER_5_COUNTRIES = [
    ('POL', 'Poland', True),
    ('GBR', 'Great Britain', True),
    ('AUS', 'Australia', True),
    ('SVK', 'Slovakia', True),
    ('LAT', 'Latvia', True),
]

# Tier 6: Countries that HAVE medaled 2010-2022
TIER_6_MEDALED = [
    ('NZL', 'New Zealand', True),
    ('UKR', 'Ukraine', True),
    ('HUN', 'Hungary', True),
    ('KAZ', 'Kazakhstan', True),
    ('CRO', 'Croatia', True),
    ('BEL', 'Belgium', True),
    ('ESP', 'Spain', True),
    ('EST', 'Estonia', True),
    ('LIE', 'Liechtenstein', True),
]

# Tier 6: Countries that have NOT medaled 2010-2022
# These will show the ⚪ indicator
# Add more as official participant list is released
TIER_6_NEVER_MEDALED = [
    # Examples - uncomment and add real countries when list is available
    # ('AND', 'Andorra', False),
    # ('ARG', 'Argentina', False),
    # ('ARM', 'Armenia', False),
    # ('AZE', 'Azerbaijan', False),
    # ('BIH', 'Bosnia and Herzegovina', False),
    # ('BRA', 'Brazil', False),
    # ('BUL', 'Bulgaria', False),
    # ('CHI', 'Chile', False),
    # ('COL', 'Colombia', False),
    # ('CYP', 'Cyprus', False),
    # ('DEN', 'Denmark', False),
    # ('GEO', 'Georgia', False),
    # ('GRE', 'Greece', False),
    # ('HKG', 'Hong Kong', False),
    # ('IND', 'India', False),
    # ('IRI', 'Iran', False),
    # ('IRL', 'Ireland', False),
    # ('ISR', 'Israel', False),
    # ('JAM', 'Jamaica', False),
    # ('KGZ', 'Kyrgyzstan', False),
    # ('LBN', 'Lebanon', False),
    # ('LTU', 'Lithuania', False),
    # ('LUX', 'Luxembourg', False),
    # ('MDA', 'Moldova', False),
    # ('MEX', 'Mexico', False),
    # ('MGL', 'Mongolia', False),
    # ('MKD', 'North Macedonia', False),
    # ('MNE', 'Montenegro', False),
    # ('MAR', 'Morocco', False),
    # ('PAK', 'Pakistan', False),
    # ('PER', 'Peru', False),
    # ('PHI', 'Philippines', False),
    # ('POR', 'Portugal', False),
    # ('ROU', 'Romania', False),
    # ('RSA', 'South Africa', False),
    # ('SRB', 'Serbia', False),
    # ('SMR', 'San Marino', False),
    # ('TPE', 'Chinese Taipei', False),
    # ('THA', 'Thailand', False),
    # ('TUR', 'Turkey', False),
    # ('UZB', 'Uzbekistan', False),
]


def seed_countries(reset: bool = False) -> None:
    """
    Seed the database with country data.
    
    Args:
        reset: If True, delete all existing countries first
    """
    with app.app_context():
        if reset:
            print("Resetting countries table...")
            Country.query.delete()
            db.session.commit()
        
        # Combine all tiers with their tier numbers
        all_countries = [
            (1, TIER_1_COUNTRIES),
            (2, TIER_2_COUNTRIES),
            (3, TIER_3_COUNTRIES),
            (4, TIER_4_COUNTRIES),
            (5, TIER_5_COUNTRIES),
            (6, TIER_6_MEDALED + TIER_6_NEVER_MEDALED),
        ]
        
        added = 0
        updated = 0
        
        for tier, countries in all_countries:
            for code, name, has_medaled in countries:
                # Check if country already exists
                existing = Country.query.filter_by(code=code).first()
                
                if existing:
                    # Update existing
                    existing.name = name
                    existing.tier = tier
                    existing.has_medaled_2010_2022 = has_medaled
                    updated += 1
                    print(f"  Updated: {code} - {name} (Tier {tier})")
                else:
                    # Create new
                    country = Country(
                        code=code,
                        name=name,
                        tier=tier,
                        has_medaled_2010_2022=has_medaled,
                        is_active=True,
                        gold_count=0,
                        silver_count=0,
                        bronze_count=0,
                    )
                    db.session.add(country)
                    added += 1
                    print(f"  Added: {code} - {name} (Tier {tier})")
        
        db.session.commit()
        
        # Initialize game state if needed
        GameState.get_instance()
        
        print(f"\n{'='*50}")
        print(f"Seeding complete!")
        print(f"  Added: {added}")
        print(f"  Updated: {updated}")
        print(f"  Total countries: {Country.query.count()}")
        print(f"{'='*50}")
        
        # Print summary by tier
        print("\nCountries by tier:")
        for tier in range(1, 7):
            count = Country.query.filter_by(tier=tier).count()
            print(f"  Tier {tier}: {count} countries")


def list_countries() -> None:
    """List all countries in the database."""
    with app.app_context():
        print("\nAll Countries in Database:")
        print("=" * 60)
        
        for tier in range(1, 7):
            countries = Country.query.filter_by(tier=tier).order_by(Country.name).all()
            print(f"\nTier {tier} ({len(countries)} countries):")
            for c in countries:
                medal_indicator = "" if c.has_medaled_2010_2022 else " ⚪"
                active_indicator = "" if c.is_active else " [INACTIVE]"
                print(f"  {c.code} - {c.name}{medal_indicator}{active_indicator}")


def add_tier6_country(code: str, name: str, has_medaled: bool = False) -> None:
    """
    Add a single Tier 6 country.
    Useful for adding countries as the official list is released.
    """
    with app.app_context():
        existing = Country.query.filter_by(code=code).first()
        if existing:
            print(f"Country {code} already exists.")
            return
        
        country = Country(
            code=code,
            name=name,
            tier=6,
            has_medaled_2010_2022=has_medaled,
            is_active=True,
        )
        db.session.add(country)
        db.session.commit()
        print(f"Added Tier 6 country: {code} - {name}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            seed_countries(reset=True)
        elif sys.argv[1] == "--list":
            list_countries()
        elif sys.argv[1] == "--add" and len(sys.argv) >= 4:
            # python seed_data.py --add CODE "Country Name" [has_medaled]
            code = sys.argv[2].upper()
            name = sys.argv[3]
            has_medaled = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else False
            add_tier6_country(code, name, has_medaled)
        else:
            print("Usage:")
            print("  python seed_data.py          # Seed countries")
            print("  python seed_data.py --reset  # Clear and re-seed")
            print("  python seed_data.py --list   # List all countries")
            print("  python seed_data.py --add CODE 'Name' [true/false]  # Add Tier 6 country")
    else:
        seed_countries()
