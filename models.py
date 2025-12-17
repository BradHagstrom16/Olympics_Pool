"""
2026 Milano-Cortina Winter Olympics Pool - Database Models
==========================================================
SQLAlchemy models for the Olympics fantasy pool game.

Core Concepts:
- Users select 8 countries across 6 tiers
- Points = medal count × medal weight × tier multiplier
- Tiebreaker based on USA medal guesses
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from config import TIERS, MEDAL_POINTS, TIMEZONE, PICK_DEADLINE

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    A player in the Olympics pool.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(100), nullable=True)
    
    # Scoring
    total_points = db.Column(db.Integer, default=0)
    
    # Admin flag
    is_admin = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    picks = db.relationship('Pick', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    tiebreaker = db.relationship('Tiebreaker', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password: str) -> None:
        """Hash and store password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def get_display_name(self) -> str:
        """Return display name or username."""
        return self.display_name or self.username
    
    def has_complete_picks(self) -> bool:
        """Check if user has submitted all 8 picks."""
        return self.picks.count() == 8
    
    def has_tiebreaker(self) -> bool:
        """Check if user has submitted tiebreaker guesses."""
        return self.tiebreaker is not None
    
    def is_ready(self) -> bool:
        """Check if user is fully registered (picks + tiebreaker)."""
        return self.has_complete_picks() and self.has_tiebreaker()
    
    def get_picks_by_tier(self) -> dict:
        """Return picks organized by tier."""
        result = {tier: [] for tier in TIERS.keys()}
        for pick in self.picks:
            result[pick.country.tier].append(pick)
        return result
    
    def calculate_total_points(self) -> int:
        """Calculate and update total points from all picks."""
        total = 0
        for pick in self.picks:
            total += pick.calculate_points()
        self.total_points = total
        return total
    
    def __repr__(self):
        return f'<User {self.username}>'


class Country(db.Model):
    """
    A country that can be selected in the pool.
    """
    __tablename__ = 'countries'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(3), unique=True, nullable=False, index=True)  # IOC code (e.g., 'USA')
    name = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.Integer, nullable=False, index=True)
    
    # Medal history flag (for Tier 6 display)
    has_medaled_2010_2022 = db.Column(db.Boolean, default=True)
    
    # Is this country participating? (can be toggled if country withdraws)
    is_active = db.Column(db.Boolean, default=True)
    
    # Current medal counts (updated during Games)
    gold_count = db.Column(db.Integer, default=0)
    silver_count = db.Column(db.Integer, default=0)
    bronze_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    picks = db.relationship('Pick', backref='country', lazy='dynamic')
    
    @property
    def total_medals(self) -> int:
        """Total medal count."""
        return self.gold_count + self.silver_count + self.bronze_count
    
    @property
    def multiplier(self) -> int:
        """Get the scoring multiplier for this country's tier."""
        return TIERS.get(self.tier, {}).get('multiplier', 1)
    
    @property
    def tier_name(self) -> str:
        """Get the display name for this country's tier."""
        return TIERS.get(self.tier, {}).get('name', 'Unknown')
    
    def calculate_points(self) -> int:
        """Calculate points this country would earn based on current medals."""
        multiplier = self.multiplier
        points = (
            self.gold_count * MEDAL_POINTS['gold'] * multiplier +
            self.silver_count * MEDAL_POINTS['silver'] * multiplier +
            self.bronze_count * MEDAL_POINTS['bronze'] * multiplier
        )
        return points
    
    def get_medal_points_breakdown(self) -> dict:
        """Get detailed points breakdown by medal type."""
        multiplier = self.multiplier
        return {
            'gold': {
                'count': self.gold_count,
                'points_each': MEDAL_POINTS['gold'] * multiplier,
                'total': self.gold_count * MEDAL_POINTS['gold'] * multiplier,
            },
            'silver': {
                'count': self.silver_count,
                'points_each': MEDAL_POINTS['silver'] * multiplier,
                'total': self.silver_count * MEDAL_POINTS['silver'] * multiplier,
            },
            'bronze': {
                'count': self.bronze_count,
                'points_each': MEDAL_POINTS['bronze'] * multiplier,
                'total': self.bronze_count * MEDAL_POINTS['bronze'] * multiplier,
            },
            'total_points': self.calculate_points(),
        }
    
    def __repr__(self):
        return f'<Country {self.code} ({self.name}) - Tier {self.tier}>'


class Pick(db.Model):
    """
    A user's selection of a country.
    Each user makes 8 picks (across 6 tiers).
    """
    __tablename__ = 'picks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    
    # Cache the tier for easier querying
    tier = db.Column(db.Integer, nullable=False)
    
    # Points earned (calculated after medals are finalized)
    points_earned = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: user can only pick a country once
    __table_args__ = (
        db.UniqueConstraint('user_id', 'country_id', name='unique_user_country_pick'),
    )
    
    def calculate_points(self) -> int:
        """Calculate points for this pick based on country's medals."""
        points = self.country.calculate_points()
        self.points_earned = points
        return points
    
    def __repr__(self):
        return f'<Pick User:{self.user_id} Country:{self.country.code}>'


class Tiebreaker(db.Model):
    """
    User's tiebreaker guesses (USA medal counts).
    """
    __tablename__ = 'tiebreakers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # USA medal count guesses
    usa_gold = db.Column(db.Integer, nullable=False)
    usa_silver = db.Column(db.Integer, nullable=False)
    usa_bronze = db.Column(db.Integer, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_differences(self, actual_gold: int, actual_silver: int, actual_bronze: int) -> tuple:
        """
        Calculate differences from actual USA medal counts.
        Returns (gold_diff, silver_diff, bronze_diff) as absolute values.
        """
        return (
            abs(self.usa_gold - actual_gold),
            abs(self.usa_silver - actual_silver),
            abs(self.usa_bronze - actual_bronze),
        )
    
    def __repr__(self):
        return f'<Tiebreaker User:{self.user_id} ({self.usa_gold}/{self.usa_silver}/{self.usa_bronze})>'


class GameState(db.Model):
    """
    Singleton table to track overall game state.
    """
    __tablename__ = 'game_state'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Medal data last updated
    medals_updated_at = db.Column(db.DateTime, nullable=True)
    
    # Scores last calculated
    scores_calculated_at = db.Column(db.DateTime, nullable=True)
    
    # Is the game complete?
    is_complete = db.Column(db.Boolean, default=False)
    
    # Winner(s) - comma-separated user IDs if co-champions
    winner_ids = db.Column(db.String(100), nullable=True)
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton game state."""
        state = cls.query.first()
        if not state:
            state = cls()
            db.session.add(state)
            db.session.commit()
        return state
    
    def __repr__(self):
        return f'<GameState updated:{self.medals_updated_at} complete:{self.is_complete}>'


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def is_picks_locked() -> bool:
    """Check if the pick deadline has passed."""
    now = datetime.now(TIMEZONE)
    return now > PICK_DEADLINE


def get_current_time() -> datetime:
    """Get current time in the configured timezone."""
    return datetime.now(TIMEZONE)


def validate_picks(user_id: int, picks_data: dict) -> tuple[bool, list[str]]:
    """
    Validate a set of picks before saving.
    
    Args:
        user_id: The user making the picks
        picks_data: Dict of {tier: [country_ids]}
    
    Returns:
        (is_valid, list_of_error_messages)
    """
    errors = []
    
    # Check deadline
    if is_picks_locked():
        errors.append("The pick deadline has passed.")
        return False, errors
    
    # Check each tier has correct number of picks
    for tier, config in TIERS.items():
        required = config['picks']
        submitted = len(picks_data.get(tier, []))
        if submitted != required:
            errors.append(f"Tier {tier} ({config['name']}) requires {required} pick(s), got {submitted}.")
    
    # Check for duplicate countries
    all_country_ids = []
    for tier_picks in picks_data.values():
        all_country_ids.extend(tier_picks)
    
    if len(all_country_ids) != len(set(all_country_ids)):
        errors.append("Each country can only be selected once.")
    
    # Verify all countries exist and are active
    for country_id in all_country_ids:
        country = Country.query.get(country_id)
        if not country:
            errors.append(f"Invalid country ID: {country_id}")
        elif not country.is_active:
            errors.append(f"{country.name} is not available for selection.")
    
    # Verify countries are in correct tiers
    for tier, country_ids in picks_data.items():
        for country_id in country_ids:
            country = Country.query.get(country_id)
            if country and country.tier != tier:
                errors.append(f"{country.name} is not in Tier {tier}.")
    
    return len(errors) == 0, errors


def calculate_all_scores() -> None:
    """Recalculate scores for all users."""
    users = User.query.all()
    for user in users:
        user.calculate_total_points()
    db.session.commit()


def get_leaderboard() -> list[dict]:
    """
    Get the current leaderboard with tiebreaker info.
    Returns list of dicts sorted by points (desc), then tiebreaker.
    """
    users = User.query.filter(User.picks.any()).all()  # Only users with picks
    
    # Get USA's actual medal counts
    usa = Country.query.filter_by(code='USA').first()
    usa_actual = (usa.gold_count, usa.silver_count, usa.bronze_count) if usa else (0, 0, 0)
    
    leaderboard = []
    for user in users:
        entry = {
            'user': user,
            'points': user.total_points,
            'tiebreaker': None,
            'tiebreaker_diff': (999, 999, 999),  # Default for sorting
        }
        
        if user.tiebreaker:
            entry['tiebreaker'] = user.tiebreaker
            entry['tiebreaker_diff'] = user.tiebreaker.get_differences(*usa_actual)
        
        leaderboard.append(entry)
    
    # Sort: points DESC, then tiebreaker diffs ASC (gold, silver, bronze)
    leaderboard.sort(key=lambda x: (
        -x['points'],
        x['tiebreaker_diff'][0],  # Gold diff
        x['tiebreaker_diff'][1],  # Silver diff
        x['tiebreaker_diff'][2],  # Bronze diff
    ))
    
    # Add ranks (handling ties)
    for i, entry in enumerate(leaderboard):
        entry['rank'] = i + 1
    
    return leaderboard
