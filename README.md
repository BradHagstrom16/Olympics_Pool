# 🏔️ Winter Olympics Pool - Flags & Olympic Rings Enhancement

This package adds country flags (as emoji) and CSS-based Olympic rings to your Winter Olympics pool website.

## Files Included

```
olympics_pool_enhancements/
├── helpers.py                 # IOC→flag emoji conversion functions
├── APP_MODIFICATIONS.py       # Code to add to your app.py
├── demo_flags_rings.html      # Standalone demo (open in browser!)
├── static/
│   └── css/
│       └── style.css          # Enhanced CSS with Olympic rings
└── templates/
    ├── base.html              # Updated base template with rings
    ├── medals.html            # Medal table with flags
    ├── countries.html         # Country browser with flags
    └── country_detail.html    # Country detail with prominent flag
```

## Quick Start

### 1. Add the Flag Helper to app.py

Add this code near the top of your `app.py`:

```python
# IOC Code to ISO 3166-1 alpha-2 mapping for flag emoji
IOC_TO_ISO = {
    'NOR': 'NO', 'GER': 'DE', 'USA': 'US', 'CAN': 'CA',
    'NED': 'NL', 'AUT': 'AT', 'SWE': 'SE', 'FRA': 'FR', 
    'SUI': 'CH', 'KOR': 'KR', 'CHN': 'CN', 'JPN': 'JP', 
    'ITA': 'IT', 'FIN': 'FI', 'CZE': 'CZ', 'SLO': 'SI',
    'POL': 'PL', 'GBR': 'GB', 'AUS': 'AU', 'SVK': 'SK', 
    'LAT': 'LV', 'NZL': 'NZ', 'UKR': 'UA', 'HUN': 'HU',
    'KAZ': 'KZ', 'CRO': 'HR', 'BEL': 'BE', 'ESP': 'ES', 
    'EST': 'EE', 'LIE': 'LI',
    # Add more as needed...
}

def ioc_to_flag_emoji(ioc_code: str) -> str:
    """Convert IOC code to flag emoji."""
    if not ioc_code:
        return ''
    iso_code = IOC_TO_ISO.get(ioc_code.upper(), ioc_code[:2].upper())
    try:
        return ''.join(chr(0x1F1E6 + ord(c) - ord('A')) for c in iso_code.upper())
    except (ValueError, TypeError):
        return ''
```

Then add this **after** `app = Flask(__name__)`:

```python
@app.template_filter('flag')
def flag_filter(ioc_code):
    """Jinja2 filter: {{ country.code|flag }} -> 🇺🇸"""
    return ioc_to_flag_emoji(ioc_code)
```

### 2. Update Your CSS

Replace or merge `static/css/style.css` with the provided file.

### 3. Update Your Templates

The key changes in templates:

#### Olympic Rings in Navbar
```html
<div class="olympic-rings olympic-rings-sm me-2">
    <div class="ring ring-blue"></div>
    <div class="ring ring-yellow"></div>
    <div class="ring ring-black"></div>
    <div class="ring ring-green"></div>
    <div class="ring ring-red"></div>
</div>
```

#### Country with Flag
```html
<span class="country-with-flag">
    <span class="flag-emoji">{{ country.code|flag }}</span>
    {{ country.name }}
</span>
```

#### In Tables
```html
<td>
    <span class="flag-emoji">{{ country.code|flag }}</span>
    <a href="...">{{ country.name }}</a>
</td>
```

## How the Flags Work

Flag emoji are created by combining two **Regional Indicator Symbols**. For example:
- US → 🇺 + 🇸 = 🇺🇸
- The Unicode range starts at U+1F1E6 (🇦)

The `ioc_to_flag_emoji()` function:
1. Looks up the IOC code (e.g., "USA") in the mapping
2. Gets the ISO code (e.g., "US")
3. Converts each letter to its Regional Indicator Symbol
4. Returns the combined emoji

## How the Olympic Rings Work

The rings are pure CSS - no images needed! Each ring is:
- An absolutely positioned div
- With `border-radius: 50%` for the circle
- With a colored border matching official Olympic colors
- Positioned to create the interlocking effect via `z-index`

Three sizes available:
- `.olympic-rings-sm` - Small (navbar)
- `.olympic-rings` - Default
- `.olympic-rings-lg` - Large (footer/hero)

## Tier Badge Styling

```html
<span class="tier-badge tier-badge-1">Tier 1</span>
<span class="tier-badge tier-badge-2">Tier 2</span>
<!-- ... etc -->
```

Each tier has a gradient background matching its prestige level (gold → silver → bronze → blue → purple → teal).

## Testing

Open `demo_flags_rings.html` in any browser to see everything working without running Flask!

## Notes

- Flag emoji work in all modern browsers and mobile devices
- The CSS rings are scalable and look sharp at any size
- No external dependencies required (besides Bootstrap/icons you already use)
- IOC→ISO mapping includes 40+ common countries; add more as needed

---

*Created for the 2026 Milano-Cortina Winter Olympics Pool*
