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
from data.countries import COUNTRIES_BY_TIER, iter_countries
from models import Country, GameState


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

        added = 0
        updated = 0

        for tier, code, name, has_medaled in iter_countries():
            existing = Country.query.filter_by(code=code).first()

            if existing:
                existing.name = name
                existing.tier = tier
                existing.has_medaled_2010_2022 = has_medaled
                existing.is_active = True
                updated += 1
                print(f"  Updated: {code} - {name} (Tier {tier})")
            else:
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
        for tier in COUNTRIES_BY_TIER.keys():
            count = Country.query.filter_by(tier=tier).count()
            print(f"  Tier {tier}: {count} countries")


def list_countries() -> None:
    """List all countries in the database."""
    with app.app_context():
        print("\nAll Countries in Database:")
        print("=" * 60)

        for tier in COUNTRIES_BY_TIER.keys():
            countries = Country.query.filter_by(tier=tier).order_by(Country.name).all()
            print(f"\nTier {tier} ({len(countries)} countries):")
            for c in countries:
                medal_status = "✅" if c.has_medaled_2010_2022 else "⚪"
                print(f"  {c.code} - {c.name} ({medal_status})")


if __name__ == '__main__':
    reset_flag = '--reset' in sys.argv
    seed_countries(reset=reset_flag)

    print("\nNext steps:")
    print("  - Log in to the admin dashboard to verify data.")
    print("  - Update Tier 6 countries as official lists are released.")

    list_countries()
