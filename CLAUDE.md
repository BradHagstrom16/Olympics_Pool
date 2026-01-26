# CLAUDE.md - AI Assistant Guide for Olympics Pool

## Project Overview

This is a **Flask-based fantasy sports web application** for the 2026 Milano-Cortina Winter Olympics. Players create fantasy Olympic teams by selecting 8 countries across 6 strategic tiers and earn points based on medals those countries win.

**Key Stats:**
- Target: 20-30 players
- Pick Deadline: February 6, 2026 at 11:59 PM CT
- Olympics: February 6-22, 2026

## Tech Stack

- **Backend:** Python 3.11+ with Flask 3.0.0
- **Database:** SQLite (SQLAlchemy 2.0+)
- **Frontend:** Bootstrap 5.3.0, vanilla JavaScript, Jinja2 templates
- **Auth:** Flask-Login, Flask-WTF (CSRF), Werkzeug (password hashing)
- **Deployment:** PythonAnywhere, Heroku, Railway, or DigitalOcean

## Project Structure

```
Olympics_Pool/
├── app.py                 # Main Flask application - routes, CLI commands
├── models.py              # SQLAlchemy database models (User, Country, Pick, etc.)
├── config.py              # Configuration & game rules (dates, points, multipliers)
├── helpers.py             # Template filters & utilities (flag conversion, etc.)
├── seed_data.py           # Database initialization script
├── requirements.txt       # Python dependencies
├── olympics_pool.db       # SQLite database (gitignored)
│
├── data/
│   └── countries.py       # Country/tier definitions with IOC↔ISO mappings
│
├── static/css/
│   └── style.css          # Theming, Olympic rings CSS, tier colors
│
└── templates/
    ├── base.html          # Base template with navbar/footer
    ├── index.html         # Homepage with leaderboard preview
    ├── edit_picks.html    # Main pick selection interface
    ├── leaderboard.html   # Full leaderboard view
    ├── medals.html        # Medal tracker
    └── admin/             # Admin dashboard, medal entry, user management
```

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
flask init-db

# Create admin user
flask create-admin

# Run development server
flask run

# Recalculate all scores
flask calculate-scores
```

## Core Game Mechanics

### Tier Structure (6 tiers, 8 total picks)

| Tier | Name | Picks | Multiplier | Countries |
|------|------|-------|------------|-----------|
| 1 | Elite | 1 | ×1 | Norway, Germany, USA, Canada |
| 2 | Strong | 2 | ×2 | Netherlands, Austria, Sweden, France, Switzerland, South Korea |
| 3 | Competitive | 1 | ×3 | China, Japan, Italy (host) |
| 4 | Emerging | 1 | ×6 | Finland, Czech Republic, Slovenia |
| 5 | Occasional | 1 | ×10 | Poland, Great Britain, Australia, Slovakia, Latvia |
| 6 | Wildcard | 2 | ×20 | 50+ other countries |

### Scoring Formula

```
Points = (Gold × 3 + Silver × 2 + Bronze × 1) × Tier Multiplier
```

### Tiebreaker

USA medal count predictions (Gold → Silver → Bronze)

## Database Models

### Primary Models (models.py)

- **User** - Credentials, display name, total points, admin flag
- **Country** - IOC code, name, tier, medal counts, is_active
- **Pick** - User-Country pairing with tier caching and points earned
- **Tiebreaker** - User's USA medal predictions
- **GameState** - Singleton for game metadata (timestamps, winner, completion)
- **MedalAudit** - Audit log for all medal changes

### Key Relationships

- User → Pick (one-to-many)
- User → Tiebreaker (one-to-one)
- Pick → Country (many-to-one)

### Business Logic Constraints

SQLite triggers enforce:
- Max 8 picks per user total
- Per-tier pick limits (1 for tiers 1,3,4,5; 2 for tiers 2,6)
- Unique user-country combinations

## Key Routes

### Public
- `/` - Homepage with leaderboard preview
- `/leaderboard` - Full rankings (after deadline)
- `/medals` - Medal tracker
- `/countries` - Browse countries by tier
- `/rules` - Game rules

### Authenticated
- `/picks` - View current picks
- `/picks/edit` - Main pick selection interface

### Admin (`@admin_required`)
- `/admin` - Dashboard with game statistics
- `/admin/medals` - Manual medal entry with safeguards
- `/admin/users` - User management
- `/admin/picks` - View all picks and scoring
- `/admin/calculate` - Trigger score recalculation

### API (JSON)
- `/api/leaderboard` - Leaderboard data for AJAX
- `/api/medals` - Medal data for real-time tracking

## Code Conventions

### Naming
- **Python:** snake_case for functions/variables, PascalCase for classes
- **CSS:** kebab-case for classes and IDs
- **IOC codes:** UPPERCASE 3-letter (e.g., 'USA', 'GER')
- **ISO codes:** lowercase 2-letter (e.g., 'us', 'de')
- **Tiers:** Referenced by numeric IDs (1-6)

### Architecture Patterns
- MVC: Models (models.py) → Views (routes in app.py) → Templates (Jinja2)
- Flask context processors for global template variables
- Decorator pattern for auth (`@login_required`, `@admin_required`)
- Jinja2 filters for display formatting (defined in helpers.py)

### Template Filters (helpers.py)
- `|flag` - Generate flag emoji from IOC code
- `|flag_class` - CSS class for flag-icons library
- `|iso` - Convert IOC to ISO code
- `|flag_img` - Generate flagcdn.com CDN URLs
- `|medal_count` - Format medal counts
- `|medal_status` - Medal status display

## Important Files to Know

### data/countries.py
Contains all IOC↔ISO code mappings for 91 countries across 6 tiers. Critical for flag display. Excluded countries: Russia, Belarus, AIN (sanctioned).

### config.py
- `PICK_DEADLINE` - February 6, 2026 11:59 PM CT
- `MEDAL_POINTS` - Gold=3, Silver=2, Bronze=1
- `TIER_MULTIPLIERS` - {1: 1, 2: 2, 3: 3, 4: 6, 5: 10, 6: 20}
- Flask configuration classes (Development/Production/Testing)

### static/css/style.css
- Pure CSS Olympic rings implementation (sm/md/lg variants)
- Tier color gradients (Gold, Silver, Bronze, Blue, Purple, Teal)
- Medal emoji styling with shadows
- Winter Olympics theme with CSS variables

## Security Considerations

- **CSRF Protection:** All forms use Flask-WTF tokens
- **Password Security:** Werkzeug secure hashing
- **SQL Injection:** SQLAlchemy ORM parameterized queries
- **Session:** Secure cookies with 30-day lifetime
- **Authorization:** `@admin_required` decorator on sensitive routes
- **Medal Safeguards:** Prevents accidental decreases without confirmation
- **Audit Trail:** Complete MedalAudit log for accountability

## Common Tasks

### Adding a New Country
1. Add to appropriate tier in `data/countries.py`
2. Include IOC code, country name, and ISO code mapping
3. Run `flask init-db` or add via admin

### Updating Medal Counts
1. Use `/admin/medals` interface (creates audit log)
2. Or use CLI: `flask calculate-scores` after manual DB update

### Modifying Tier Structure
1. Update `TIER_MULTIPLIERS` in `config.py`
2. Update tier assignments in `data/countries.py`
3. Re-run database seeding if needed

### Testing Locally
```bash
# Set development mode
export FLASK_ENV=development
export FLASK_DEBUG=1

# Run with auto-reload
flask run --reload
```

## Documentation Files

- **README.md** - Full project documentation, installation guide, deployment
- **SPECIFICATION.md** - Locked game specification (v1.0) - DO NOT MODIFY game rules without discussion

## Things to Watch Out For

1. **IOC vs ISO codes** - Always use the mapping in `data/countries.py` for flag display
2. **Pick deadline logic** - Check `config.PICK_DEADLINE` before allowing pick changes
3. **SQLite triggers** - Business logic enforced at DB level, not just Python
4. **Tier 6 split** - Has both medaled (2010-2022) and non-medaled countries
5. **Admin routes** - Always protected by `@admin_required` decorator
6. **Audit logging** - All medal changes must create MedalAudit records

## Development Workflow

1. Create feature branch from main
2. Make changes following code conventions
3. Test locally with `flask run`
4. Ensure CSRF tokens on all forms
5. Add audit logging for any data changes
6. Update README.md if adding features
7. Commit with descriptive messages
8. Push and create PR

## Environment Variables

```bash
FLASK_APP=app.py
FLASK_ENV=development|production
SECRET_KEY=<your-secret-key>
DATABASE_URL=sqlite:///olympics_pool.db  # or PostgreSQL URL
```

## Future Enhancements (Planned)

- Automated medal API integration
- Email notifications
- Historical leaderboards
- Summer Olympics 2028 adaptation
- Mobile app
- Social features
