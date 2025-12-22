# 🏔️ 2026 Milano-Cortina Winter Olympics Pool

<div align="center">

**A fantasy sports pool for the 2026 Winter Olympics**

[Features](#-features) • [How It Works](#-how-it-works) • [Installation](#-installation) • [Tech Stack](#-tech-stack) • [Deployment](#-deployment)

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

🇮🇹 **February 6-22, 2026 • Milano-Cortina, Italy**

</div>

---

## 📖 About

Pick your countries, predict the medals, and compete for glory! This web application lets players create their fantasy Olympic teams by selecting countries across six strategic tiers, with underdog picks earning higher point multipliers.

The game combines sports knowledge, strategic risk-taking, and a bit of luck to create an engaging experience for Winter Olympics fans.

## ✨ Features

### 🎮 For Players
- **Strategic Country Selection**: Pick 8 countries across 6 tiers (Elite → Wildcard)
- **Dynamic Point Multipliers**: Lower-tier countries earn more points per medal (×1 to ×20)
- **Real-time Leaderboard**: Track your standing as medals are won
- **USA Tiebreaker System**: Predict USA's medal count to break ties
- **Mobile-Responsive Design**: Play on any device
- **Pick Editing**: Update your selections anytime before the deadline

### 🛠️ For Admins
- **Manual Medal Entry**: Update medal counts with built-in safeguards
- **Automatic Score Calculation**: Points recalculate instantly after medal updates
- **User Management**: View all players and reset passwords
- **Audit Trail**: Track all medal changes with timestamps
- **Game State Dashboard**: Monitor participation and game progress

### 🎨 Visual Design
- **Olympic Rings**: Pure CSS implementation of the official Olympic rings
- **Country Flags**: Reliable flag display using flagcdn.com
- **Tier Badges**: Color-coded tier system (Gold → Silver → Bronze → Blue → Purple → Teal)
- **Medal Indicators**: Visual tracking of 🥇 Gold, 🥈 Silver, 🥉 Bronze medals

## 🎯 How It Works

### Pick Structure
| Tier | Name | Countries | Picks | Multiplier |
|------|------|-----------|-------|------------|
| **1** | Elite | Norway, Germany, USA, Canada | 1 | ×1 |
| **2** | Strong | Netherlands, Austria, Sweden, France, Switzerland, South Korea | 2 | ×2 |
| **3** | Competitive | China, Japan, Italy (Host!) | 1 | ×3 |
| **4** | Emerging | Finland, Czech Republic, Slovenia | 1 | ×6 |
| **5** | Occasional | Poland, Great Britain, Australia, Slovakia, Latvia | 1 | ×10 |
| **6** | Wildcard | 50+ countries including underdogs | 2 | ×20 |

### Scoring System
```
Points = (Gold × 3 + Silver × 2 + Bronze × 1) × Tier Multiplier
```

**Example**: If you pick Slovenia (Tier 4) and they win a gold medal:
```
3 points (gold) × 10 (Tier 4 multiplier) = 30 points!
```

### Tiebreaker
In case of equal points, the winner is determined by closest guess to:
1. USA's Gold medal count
2. USA's Silver medal count (if still tied)
3. USA's Bronze medal count (if still tied)
4. Co-champions if still tied!

## 🚀 Installation

### Prerequisites
- Python 3.11+
- pip
- Virtual environment (recommended)

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/olympics-pool.git
cd olympics-pool
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
flask init-db
python seed_data.py
```

5. **Create an admin user**
```bash
flask create-admin
```

6. **Run the development server**
```bash
flask run
```

Visit `http://localhost:5000` in your browser!

## 🏗️ Tech Stack

### Backend
- **Flask 3.0.0** - Web framework
- **SQLAlchemy 2.0+** - ORM and database management
- **Flask-Login 0.6.3** - User authentication
- **Flask-WTF 1.2.1** - Form handling and CSRF protection
- **SQLite** - Database (easily upgradeable to PostgreSQL)

### Frontend
- **Bootstrap 5.3.0** - UI framework
- **Bootstrap Icons** - Icon library
- **Custom CSS** - Olympic-themed styling with pure CSS rings
- **Vanilla JavaScript** - Interactive pick selection

### Security
- **Werkzeug** - Password hashing
- **email-validator** - Email validation
- **CSRF Protection** - Form security

## 📁 Project Structure

```
olympics-pool/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── config.py                   # Configuration settings
├── helpers.py                  # Template filters and utilities
├── requirements.txt            # Python dependencies
├── seed_data.py               # Country data seeding script
│
├── data/
│   └── countries.py           # Canonical country/tier definitions
│
├── static/
│   └── css/
│       └── style.css          # Olympic-themed CSS with rings
│
└── templates/
    ├── base.html              # Base template with navbar
    ├── index.html             # Home page
    ├── leaderboard.html       # Full leaderboard
    ├── medals.html            # Medal tracker
    ├── countries.html         # Country browser
    ├── country_detail.html    # Individual country page
    ├── edit_picks.html        # Pick selection interface
    ├── my_picks.html          # User's picks view
    ├── rules.html             # Game rules
    ├── users.html             # Player list
    ├── user_detail.html       # Player profile
    ├── login.html             # Login page
    ├── register.html          # Registration page
    ├── change_password.html   # Password change
    └── admin/
        ├── dashboard.html     # Admin overview
        ├── medals.html        # Medal entry form
        ├── picks.html         # All picks view
        └── users.html         # User management
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required for production
SECRET_KEY=your-secret-key-here

# Optional - defaults to SQLite
DATABASE_URL=sqlite:///olympics_pool.db

# Optional - deployment environment
FLASK_ENV=production
```

### Game Settings
All game rules are defined in `config.py`:
- Pick deadline: February 6, 2026 at 11:59 PM CT
- Tier structure and multipliers
- Medal point values (Gold: 3, Silver: 2, Bronze: 1)
- Total picks required: 8

### Tier Structure
Tiers are based on statistical analysis of 2010-2022 Winter Olympics performance:
- **K-means clustering** for optimal country groupings
- **Historical medal data** across 4 Olympic cycles
- **Balanced expected values** across tiers (except Tier 6 wildcards)

## 🌐 Deployment

### PythonAnywhere (Recommended)

1. **Upload files** to PythonAnywhere
2. **Set up virtual environment**
3. **Configure WSGI file**:
```python
import sys
path = '/home/yourusername/olympics-pool'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```
4. **Initialize database**:
```bash
flask init-db
python seed_data.py
flask create-admin
```
5. **Set environment variables** in web app settings
6. **Reload web app**

### Other Platforms
- **Heroku**: Use `gunicorn` (already in requirements.txt)
- **Railway**: Connect GitHub repo and deploy
- **DigitalOcean**: Use App Platform or Droplet

## 🎮 Usage

### For Players
1. **Sign Up**: Create an account with username, email, and password
2. **Make Picks**: Select 8 countries across 6 tiers before the deadline
3. **Set Tiebreaker**: Predict USA's gold, silver, and bronze medal counts
4. **Watch & Wait**: Follow the leaderboard as medals are won
5. **Win**: Have the most points when the Olympics conclude!

### For Admins
1. **Update Medals**: Enter medal counts manually or via API (future feature)
2. **Monitor Progress**: Track user participation and game state
3. **Manage Users**: Reset passwords and view all picks
4. **Recalculate Scores**: Trigger score updates (automatic after medal changes)

## 📊 Database Schema

```sql
users          # Player accounts and scores
countries      # All participating countries with medal counts
picks          # User's 8 country selections (with constraints)
tiebreakers    # USA medal predictions
game_state     # Singleton for game metadata
medal_audit    # Audit log of all medal changes
```

### Database Constraints
- **Total picks limit**: 8 picks per user (enforced by triggers)
- **Per-tier limits**: Enforced via SQLite triggers
- **Unique picks**: Users can't select the same country twice
- **Game state singleton**: Prevents multiple game state rows

## 🔒 Security Features

- **Password hashing** with Werkzeug
- **CSRF protection** on all forms
- **Session management** with secure cookies
- **Input validation** for all user data
- **SQL injection prevention** via SQLAlchemy ORM
- **Admin-only routes** with decorator protection
- **Medal decrease safeguards** to prevent accidental data loss

## 📝 Future Enhancements

- [ ] **Automated Medal API**: Real-time medal updates from official sources
- [ ] **Email Notifications**: Deadline reminders and score updates
- [ ] **Historical Leaderboards**: Track winners across multiple years
- [ ] **Summer Olympics Support**: Adapt for 2028 Los Angeles Olympics
- [ ] **Advanced Statistics**: Player analytics and country performance trends
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Social Features**: Comments, trash talk, and player interactions

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Olympic Ring CSS**: Pure CSS implementation of official Olympic colors
- **Flag Icons**: Powered by [flagcdn.com](https://flagcdn.com)
- **Bootstrap**: UI framework by Twitter
- **Flask Community**: Excellent documentation and support
- **Winter Olympics Data**: Medal counts from 2010-2022 Olympics

## 👤 Author

Created for the 2026 Milano-Cortina Winter Olympics

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](../../issues).

---

<div align="center">

**Made with ❤️ for Winter Olympics fans**

🏔️ ⛷️ 🏒 ⛸️ 🏂


</div>
