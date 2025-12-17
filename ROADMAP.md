# 2026 Milano-Cortina Winter Olympics Pool
## Development Roadmap

**Status:** Session 1 In Progress  
**Last Updated:** December 16, 2024

---

## ALL DECISIONS FINALIZED ✅

| Decision | Final Answer |
|----------|--------------|
| App name | 2026 Milano-Cortina Winter Olympics Pool |
| Tiers | 1, 2, 3, 4, 5, 6 (sequential numbers) |
| Picks | 1 + 2 + 1 + 1 + 1 + 2 = 8 |
| Multipliers | ×1, ×2, ×3, ×6, ×10, ×20 |
| Medal weights | Gold=3, Silver=2, Bronze=1 |
| Deadline | Feb 6, 2026 at 11:59 PM Central |
| Tiebreaker | USA Gold → Silver → Bronze guesses |
| Tied tiebreaker | Co-champions (easiest to code) |
| Registration | Open signup (link access), email required |
| Expected users | 20-30 players |
| Prize | Bragging rights (monetary hooks for later) |
| Pick visibility | Hidden until deadline |
| User list visibility | Visible before deadline |
| Pick editing | Unlimited until deadline |
| Country withdrawal | Counts as 0 points |
| Medal data | Automated API (research later), manual fallback |
| Doping adjustments | No retroactive changes |
| Team events | Same as individual (1 medal = 1 medal) |
| Tier 6 indicator | ⚪ for never-medaled countries |
| Tier 6 UI | Scrollable list + search filter |
| Admin features | View picks, manual medals, password reset |
| Last updated display | Yes, show timestamp |

---

## SESSION 1: DATABASE & MODELS ✅ COMPLETE

### Objectives
- [x] Create project structure
- [x] Create specification document
- [x] Create roadmap document
- [x] Design database schema
- [x] Build models.py
- [x] Create country seed data
- [x] Build config.py
- [x] Build app.py with all routes
- [x] Create all templates (26 files)
- [x] Create custom CSS

### Database Schema
```
countries          - All participating countries with tier assignments
users              - Player accounts
picks              - User's 8-country selections
tiebreakers        - USA medal guesses
medals             - Medal counts per country (updated during Games)
```

---

## SESSION 2: CORE APPLICATION ✅ COMPLETE

### Objectives
- [x] Create app.py with Flask setup
- [x] Build authentication (register, login, logout)
- [x] Create base template with branding
- [x] Build home page (leaderboard preview)
- [x] Create user dashboard

---

## SESSION 3: PICK SUBMISSION SYSTEM ✅ COMPLETE

### Objectives
- [x] Build pick submission page (all 6 tiers)
- [x] Implement tier validation (correct counts)
- [x] Add tiebreaker guess form
- [x] Build pick editing functionality
- [x] Implement deadline enforcement
- [x] Add Tier 6 search/filter
- [x] Add ⚪ never-medaled indicators

---

## SESSION 4: SCORING & LEADERBOARD ✅ COMPLETE

### Objectives
- [x] Build scoring calculation engine
- [x] Create leaderboard display
- [x] Add "last updated" timestamp
- [x] Build country detail views
- [x] Create medal tracking display
- [x] Implement tiebreaker logic

---

## SESSION 5: ADMIN & POLISH ✅ COMPLETE

### Objectives
- [x] Build admin dashboard
- [x] Create manual medal entry interface
- [x] Add password reset functionality
- [x] Add pick visibility toggle (deadline-based)
- [x] Polish UI/UX
- [x] Mobile responsiveness
- [x] Create rules page

---

## SESSION 6: TESTING & DEPLOYMENT ← NEXT

### Objectives
- [ ] Install dependencies (pip install -r requirements.txt)
- [ ] Initialize database (flask init-db)
- [ ] Seed country data (python seed_data.py)
- [ ] Create admin user (flask create-admin)
- [ ] End-to-end testing
- [ ] Deploy to PythonAnywhere
- [ ] Configure production database
- [ ] Final verification

---

## FUTURE: MEDAL API RESEARCH

**Timeline:** January 2026 (closer to Games)

### Options to Research
1. Official Olympics API
2. Free sports data APIs
3. ESPN/NBC medal trackers
4. Web scraping solutions
5. Replicate Excel automation approach

---

## FILE STRUCTURE (Planned)

```
olympics_pool/
├── app.py                 # Main Flask application
├── models.py              # SQLAlchemy models
├── config.py              # Configuration settings
├── requirements.txt       # Dependencies
├── SPECIFICATION.md       # Locked game spec
├── ROADMAP.md            # This file
├── seed_data.py          # Country data seeding
├── static/
│   ├── css/
│   │   └── style.css
│   └── img/
│       └── (flags, logos)
└── templates/
    ├── base.html
    ├── index.html
    ├── register.html
    ├── login.html
    ├── picks.html
    ├── leaderboard.html
    ├── rules.html
    ├── country.html
    └── admin/
        ├── dashboard.html
        ├── users.html
        └── medals.html
```

---

*Roadmap created December 16, 2024*
