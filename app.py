"""
2026 Milano-Cortina Winter Olympics Pool - Main Application
============================================================
Flask application for the Olympics fantasy pool game.
"""

import os
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect, generate_csrf
from sqlalchemy import func
from email_validator import validate_email, EmailNotValidError

from config import (
    config, TIERS, MEDAL_POINTS, TIMEZONE, PICK_DEADLINE, TOTAL_PICKS,
    TIER_6_WARNING, get_medal_points
)
from models import (
    db, User, Country, Pick, Tiebreaker, GameState,
    is_picks_locked, get_current_time, validate_picks,
    calculate_all_scores, get_leaderboard, install_pick_constraints,
    MedalAudit
)

# =============================================================================
# APP INITIALIZATION
# =============================================================================

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLASK_ENV', 'default')])
from helpers import register_template_helpers
register_template_helpers(app)

# Initialize extensions
db.init_app(app)
with app.app_context():
    install_pick_constraints()
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))


# =============================================================================
# DECORATORS
# =============================================================================

def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# =============================================================================
# CONTEXT PROCESSORS
# =============================================================================

@app.context_processor
def inject_globals():
    """Inject global variables into all templates."""
    game_state = GameState.get_instance()
    return {
        'app_name': app.config['APP_NAME'],
        'app_short_name': app.config['APP_SHORT_NAME'],
        'current_time': get_current_time(),
        'pick_deadline': PICK_DEADLINE,
        'picks_locked': is_picks_locked(),
        'tiers': TIERS,
        'medal_points': MEDAL_POINTS,
        'game_state': game_state,
        'csrf_token': generate_csrf,
    }


# =============================================================================
# PUBLIC ROUTES
# =============================================================================

@app.route('/')
def index():
    """Home page - shows leaderboard and game status."""
    game_state = GameState.get_instance()
    
    # Get registered user count
    total_users = User.query.count()
    ready_users = User.query.filter(User.picks.any()).count()
    
    # Get leaderboard if picks are locked
    leaderboard = []
    if is_picks_locked():
        leaderboard = get_leaderboard()
    
    # Get medal leaders (top 5 countries by total medals)
    medal_leaders = Country.query.filter(
        (Country.gold_count + Country.silver_count + Country.bronze_count) > 0
    ).order_by(
        Country.gold_count.desc(),
        Country.silver_count.desc(),
        Country.bronze_count.desc()
    ).limit(5).all()
    
    return render_template('index.html',
                         total_users=total_users,
                         ready_users=ready_users,
                         leaderboard=leaderboard,
                         medal_leaders=medal_leaders)


@app.route('/leaderboard')
def leaderboard():
    """Full leaderboard page."""
    if not is_picks_locked():
        flash('Leaderboard will be available after picks lock on February 6th.', 'info')
        return redirect(url_for('index'))
    
    leaderboard_data = get_leaderboard()
    game_state = GameState.get_instance()
    
    # Get USA actual medals for tiebreaker display
    usa = Country.query.filter_by(code='USA').first()
    usa_medals = {
        'gold': usa.gold_count if usa else 0,
        'silver': usa.silver_count if usa else 0,
        'bronze': usa.bronze_count if usa else 0,
    }
    
    return render_template('leaderboard.html',
                         leaderboard=leaderboard_data,
                         usa_medals=usa_medals,
                         last_updated=game_state.medals_updated_at)


@app.route('/countries')
def countries():
    """Browse all countries by tier."""
    countries_by_tier = {}
    for tier in range(1, 7):
        countries_by_tier[tier] = Country.query.filter_by(
            tier=tier,
            is_active=True
        ).order_by(Country.name).all()
    
    return render_template('countries.html',
                         countries_by_tier=countries_by_tier,
                         tier_6_warning=TIER_6_WARNING)


@app.route('/country/<int:country_id>')
def country_detail(country_id):
    """Country detail page with medal breakdown."""
    country = Country.query.get_or_404(country_id)
    
    # Get users who picked this country (only after deadline)
    picked_by = []
    if is_picks_locked():
        picks = Pick.query.filter_by(country_id=country_id).all()
        picked_by = [pick.user for pick in picks]
    
    return render_template('country_detail.html',
                         country=country,
                         picked_by=picked_by)


@app.route('/rules')
def rules():
    """Game rules page."""
    return render_template('rules.html',
                         tiers=TIERS,
                         medal_points=MEDAL_POINTS,
                         tier_6_warning=TIER_6_WARNING)


@app.route('/medals')
def medals():
    """Medal tracker - all countries sorted by medal count."""
    countries = Country.query.filter(
        Country.is_active == True
    ).all()
    
    # Sort by gold, then silver, then bronze
    countries.sort(key=lambda c: (c.gold_count, c.silver_count, c.bronze_count), reverse=True)
    
    # Filter to only those with medals for the "medal table" view
    medaled_countries = [c for c in countries if c.total_medals > 0]
    
    game_state = GameState.get_instance()
    
    return render_template('medals.html',
                         countries=medaled_countries,
                         last_updated=game_state.medals_updated_at)


# =============================================================================
# AUTHENTICATION ROUTES
# =============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        display_name = request.form.get('display_name', '').strip() or None
        
        errors = []
        
        # Validate username
        if len(username) < 3:
            errors.append('Username must be at least 3 characters.')
        if User.query.filter(func.lower(User.username) == username.lower()).first():
            errors.append('Username already taken.')
        
        # Validate email
        try:
            validated_email = validate_email(email, check_deliverability=False).email
        except EmailNotValidError as e:
            errors.append(str(e))
            validated_email = None
        
        if validated_email and User.query.filter(func.lower(User.email) == validated_email.lower()).first():
            errors.append('Email already registered.')
        
        # Validate password
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if password != confirm_password:
            errors.append('Passwords do not match.')
        
        if errors:
            for error in errors:
                flash(error, 'error')
        else:
            user = User(
                username=username,
                email=validated_email or email.lower(),
                display_name=display_name
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in to make your picks.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = User.query.filter(func.lower(User.username) == username.lower()).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash(f'Welcome back, {user.get_display_name()}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# =============================================================================
# PICK ROUTES
# =============================================================================

@app.route('/picks')
@login_required
def my_picks():
    """View user's current picks."""
    picks_by_tier = current_user.get_picks_by_tier()
    
    return render_template('my_picks.html',
                         picks_by_tier=picks_by_tier,
                         tiebreaker=current_user.tiebreaker)


@app.route('/picks/edit', methods=['GET', 'POST'])
@login_required
def edit_picks():
    """Edit picks - the main pick submission page."""
    if is_picks_locked():
        flash('The pick deadline has passed. Picks can no longer be edited.', 'error')
        return redirect(url_for('my_picks'))
    
    if request.method == 'POST':
        # Collect picks from form
        picks_data = {}
        for tier in TIERS.keys():
            tier_picks = request.form.getlist(f'tier_{tier}')
            picks_data[tier] = [int(cid) for cid in tier_picks if cid]
        
        # Collect tiebreaker guesses
        try:
            usa_gold = int(request.form.get('usa_gold', 0))
            usa_silver = int(request.form.get('usa_silver', 0))
            usa_bronze = int(request.form.get('usa_bronze', 0))
        except ValueError:
            flash('Tiebreaker guesses must be numbers.', 'error')
            return redirect(url_for('edit_picks'))
        
        # Validate picks
        is_valid, errors = validate_picks(current_user.id, picks_data)
        
        if not is_valid:
            for error in errors:
                flash(error, 'error')
        else:
            # Clear existing picks
            Pick.query.filter_by(user_id=current_user.id).delete()
            
            # Save new picks
            for tier, country_ids in picks_data.items():
                for country_id in country_ids:
                    pick = Pick(
                        user_id=current_user.id,
                        country_id=country_id,
                        tier=tier,
                    )
                    db.session.add(pick)
            
            # Save or update tiebreaker
            if current_user.tiebreaker:
                current_user.tiebreaker.usa_gold = usa_gold
                current_user.tiebreaker.usa_silver = usa_silver
                current_user.tiebreaker.usa_bronze = usa_bronze
            else:
                tiebreaker = Tiebreaker(
                    user_id=current_user.id,
                    usa_gold=usa_gold,
                    usa_silver=usa_silver,
                    usa_bronze=usa_bronze,
                )
                db.session.add(tiebreaker)
            
            db.session.commit()
            flash('Your picks have been saved!', 'success')
            return redirect(url_for('my_picks'))
    
    # Get countries by tier for selection
    countries_by_tier = {}
    for tier in range(1, 7):
        countries_by_tier[tier] = Country.query.filter_by(
            tier=tier,
            is_active=True
        ).order_by(Country.name).all()
    
    # Get user's current picks
    current_picks = {}
    for pick in current_user.picks:
        if pick.tier not in current_picks:
            current_picks[pick.tier] = []
        current_picks[pick.tier].append(pick.country_id)
    
    return render_template('edit_picks.html',
                         countries_by_tier=countries_by_tier,
                         current_picks=current_picks,
                         tiebreaker=current_user.tiebreaker,
                         tier_6_warning=TIER_6_WARNING)


# =============================================================================
# USER ROUTES
# =============================================================================

@app.route('/users')
def users():
    """List all registered users (names only, no picks until deadline)."""
    show_picks = is_picks_locked()

    all_users = User.query.options(
        db.load_only(User.id, User.username, User.display_name, User.created_at, User.total_points),
        db.noload(User.picks)
    ).order_by(User.created_at).all()

    users_data = []
    for user in all_users:
        pick_count = Pick.query.filter_by(user_id=user.id).count()
        tiebreaker_exists = Tiebreaker.query.filter_by(user_id=user.id).first() is not None
        ready = pick_count == TOTAL_PICKS and tiebreaker_exists
        users_data.append({
            'id': user.id,
            'display_name': user.get_display_name(),
            'created_at': user.created_at,
            'ready': ready,
            'is_current_user': current_user.is_authenticated and user.id == current_user.id,
            'total_points': user.total_points if show_picks else None,
        })

    return render_template('users.html',
                         users=users_data,
                         show_picks=show_picks)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """View a user's picks (only after deadline)."""
    user = User.query.get_or_404(user_id)
    
    if not is_picks_locked() and user.id != current_user.id:
        flash('Picks will be visible after the deadline.', 'info')
        return redirect(url_for('users'))
    
    picks_by_tier = user.get_picks_by_tier()
    
    return render_template('user_detail.html',
                         user=user,
                         picks_by_tier=picks_by_tier,
                         tiebreaker=user.tiebreaker)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password for logged-in user."""
    if request.method == 'POST':
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'error')
        elif len(new_password) < 6:
            flash('New password must be at least 6 characters.', 'error')
        elif new_password != confirm_password:
            flash('New passwords do not match.', 'error')
        else:
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!', 'success')
            return redirect(url_for('index'))
    
    return render_template('change_password.html')


# =============================================================================
# ADMIN ROUTES
# =============================================================================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard."""
    total_users = User.query.count()
    ready_users = User.query.filter(User.picks.any()).count()
    game_state = GameState.get_instance()
    
    # Get total medals entered
    total_medals = db.session.query(
        func.sum(Country.gold_count + Country.silver_count + Country.bronze_count)
    ).scalar() or 0
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         ready_users=ready_users,
                         total_medals=total_medals,
                         game_state=game_state)


@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin view of all users."""
    users = User.query.order_by(func.lower(User.username)).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/reset-password/<int:user_id>', methods=['POST'])
@admin_required
def admin_reset_password(user_id):
    """Admin password reset."""
    user = User.query.get_or_404(user_id)
    new_password = request.form.get('new_password', '').strip()
    
    if not new_password or len(new_password) < 6:
        flash('Password must be at least 6 characters.', 'error')
    else:
        user.set_password(new_password)
        db.session.commit()
        flash(f'Password reset for {user.get_display_name()}. New password: {new_password}', 'success')
    
    return redirect(url_for('admin_users'))


@app.route('/admin/medals', methods=['GET', 'POST'])
@admin_required
def admin_medals():
    """Admin medal entry/update."""
    if request.method == 'POST':
        country_id = request.form.get('country_id', type=int)
        gold = request.form.get('gold', type=int, default=0)
        silver = request.form.get('silver', type=int, default=0)
        bronze = request.form.get('bronze', type=int, default=0)
        allow_decrease = request.form.get('allow_decrease') == 'on'

        errors = []
        for label, value in [('gold', gold), ('silver', silver), ('bronze', bronze)]:
            if value is None or value < 0:
                errors.append(f"{label.title()} must be zero or greater.")

        country = Country.query.get(country_id)
        if country:
            if not allow_decrease and (
                gold < country.gold_count or
                silver < country.silver_count or
                bronze < country.bronze_count
            ):
                errors.append('Medal counts cannot decrease unless corrections are explicitly allowed.')

            if errors:
                for msg in errors:
                    flash(msg, 'error')
            elif (gold, silver, bronze) == (
                country.gold_count, country.silver_count, country.bronze_count
            ):
                flash('No changes detected for this country.', 'info')
            else:
                now = datetime.utcnow()
                audit_entry = MedalAudit(
                    country=country,
                    updated_by=current_user if current_user.is_authenticated else None,
                    source='admin_form',
                    gold_before=country.gold_count,
                    silver_before=country.silver_count,
                    bronze_before=country.bronze_count,
                    gold_after=gold,
                    silver_after=silver,
                    bronze_after=bronze,
                )

                country.gold_count = gold
                country.silver_count = silver
                country.bronze_count = bronze
                country.updated_at = now

                game_state = GameState.get_instance()
                game_state.medals_updated_at = now

                try:
                    calculate_all_scores(commit_session=False)
                    game_state.scores_calculated_at = now
                    db.session.add(audit_entry)
                    db.session.commit()
                    flash(f'Updated medals for {country.name} and recalculated scores.', 'success')
                except Exception as exc:  # pragma: no cover - defensive rollback
                    db.session.rollback()
                    flash(f'Failed to update medals: {exc}', 'error')
        else:
            flash('Country not found.', 'error')
    
    # Get all countries for the form
    countries = Country.query.filter_by(is_active=True).order_by(Country.name).all()
    
    return render_template('admin/medals.html', countries=countries)


@app.route('/admin/calculate', methods=['POST'])
@admin_required
def admin_calculate():
    """Recalculate all scores."""
    calculate_all_scores()
    
    game_state = GameState.get_instance()
    game_state.scores_calculated_at = datetime.utcnow()
    db.session.commit()
    
    flash('All scores recalculated.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/picks')
@admin_required
def admin_picks():
    """Admin view of all picks."""
    users = User.query.filter(User.picks.any()).order_by(func.lower(User.username)).all()
    
    picks_data = []
    for user in users:
        picks_data.append({
            'user': user,
            'picks_by_tier': user.get_picks_by_tier(),
            'tiebreaker': user.tiebreaker,
            'total_points': user.total_points,
        })
    
    return render_template('admin/picks.html', picks_data=picks_data)


# =============================================================================
# API ROUTES (for AJAX updates)
# =============================================================================

@app.route('/api/leaderboard')
def api_leaderboard():
    """JSON endpoint for leaderboard data."""
    if not is_picks_locked():
        return jsonify({'error': 'Picks not yet locked'}), 403
    
    leaderboard_data = get_leaderboard()
    game_state = GameState.get_instance()
    
    return jsonify({
        'leaderboard': [
            {
                'rank': entry['rank'],
                'name': entry['user'].get_display_name(),
                'points': entry['points'],
            }
            for entry in leaderboard_data
        ],
        'last_updated': game_state.medals_updated_at.isoformat() if game_state.medals_updated_at else None,
    })


@app.route('/api/medals')
def api_medals():
    """JSON endpoint for medal counts."""
    countries = Country.query.filter(
        (Country.gold_count + Country.silver_count + Country.bronze_count) > 0
    ).all()
    
    countries.sort(key=lambda c: (c.gold_count, c.silver_count, c.bronze_count), reverse=True)
    
    game_state = GameState.get_instance()
    
    return jsonify({
        'medals': [
            {
                'code': c.code,
                'name': c.name,
                'gold': c.gold_count,
                'silver': c.silver_count,
                'bronze': c.bronze_count,
                'total': c.total_medals,
            }
            for c in countries
        ],
        'last_updated': game_state.medals_updated_at.isoformat() if game_state.medals_updated_at else None,
    })


# =============================================================================
# CLI COMMANDS
# =============================================================================

@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    db.create_all()
    GameState.get_instance()  # Create game state singleton
    print('Database initialized.')


@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    import getpass
    
    username = input('Admin username: ').strip()
    email = input('Admin email: ').strip()
    password = getpass.getpass('Admin password: ')
    
    if User.query.filter(func.lower(User.username) == username.lower()).first():
        print(f'User {username} already exists.')
        return
    
    user = User(
        username=username,
        email=email,
        is_admin=True
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    print(f'Admin user {username} created.')


@app.cli.command('calculate-scores')
def calculate_scores_cmd():
    """Recalculate all user scores."""
    calculate_all_scores()
    print('Scores recalculated.')


# =============================================================================
# RUN
# =============================================================================

if __name__ == '__main__':
    app.run(debug=True)
