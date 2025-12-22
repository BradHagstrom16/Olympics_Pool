"""Canonical country and tier definitions for the Olympics Pool app."""

from __future__ import annotations

# Format: tier_number -> {IOC code: (name, has_medaled_2010_2022)}
COUNTRIES_BY_TIER = {
    1: {
        'NOR': ('Norway', True),
        'GER': ('Germany', True),
        'USA': ('United States', True),
        'CAN': ('Canada', True),
    },
    2: {
        'NED': ('Netherlands', True),
        'AUT': ('Austria', True),
        'SWE': ('Sweden', True),
        'FRA': ('France', True),
        'SUI': ('Switzerland', True),
        'KOR': ('South Korea', True),
    },
    3: {
        'CHN': ('China', True),
        'JPN': ('Japan', True),
        'ITA': ('Italy', True),
    },
    4: {
        'FIN': ('Finland', True),
        'CZE': ('Czech Republic', True),
        'SLO': ('Slovenia', True),
    },
    5: {
        'POL': ('Poland', True),
        'GBR': ('Great Britain', True),
        'AUS': ('Australia', True),
        'SVK': ('Slovakia', True),
        'LAT': ('Latvia', True),
    },
    6: {
        # Tier 6: Countries that have medaled 2010-2022
        'NZL': ('New Zealand', True),
        'UKR': ('Ukraine', True),
        'HUN': ('Hungary', True),
        'KAZ': ('Kazakhstan', True),
        'CRO': ('Croatia', True),
        'BEL': ('Belgium', True),
        'ESP': ('Spain', True),
        'EST': ('Estonia', True),
        'LIE': ('Liechtenstein', True),
        # Tier 6: Known participants without recent medals
        'AND': ('Andorra', False),
        'ARG': ('Argentina', False),
        'ARM': ('Armenia', False),
        'AZE': ('Azerbaijan', False),
        'BIH': ('Bosnia and Herzegovina', False),
        'BRA': ('Brazil', False),
        'BUL': ('Bulgaria', False),
        'CHI': ('Chile', False),
        'COL': ('Colombia', False),
        'CYP': ('Cyprus', False),
        'DEN': ('Denmark', False),
        'GEO': ('Georgia', False),
        'GRE': ('Greece', False),
        'HKG': ('Hong Kong', False),
        'IND': ('India', False),
        'IRI': ('Iran', False),
        'IRL': ('Ireland', False),
        'ISR': ('Israel', False),
        'JAM': ('Jamaica', False),
        'KGZ': ('Kyrgyzstan', False),
        'LBN': ('Lebanon', False),
        'LTU': ('Lithuania', False),
        'LUX': ('Luxembourg', False),
        'MDA': ('Moldova', False),
        'MEX': ('Mexico', False),
        'MGL': ('Mongolia', False),
        'MKD': ('North Macedonia', False),
        'MNE': ('Montenegro', False),
        'MAR': ('Morocco', False),
        'PAK': ('Pakistan', False),
        'PER': ('Peru', False),
        'PHI': ('Philippines', False),
        'POR': ('Portugal', False),
        'ROU': ('Romania', False),
        'RSA': ('South Africa', False),
        'SRB': ('Serbia', False),
        'SMR': ('San Marino', False),
        'TPE': ('Chinese Taipei', False),
        'THA': ('Thailand', False),
        'TUR': ('Turkey', False),
        'UZB': ('Uzbekistan', False),
    },
}

# Countries that cannot be selected
EXCLUDED_COUNTRIES = {
    'RUS': 'Russia',
    'BLR': 'Belarus',
    'AIN': 'Individual Neutral Athletes',
}


def iter_countries():
    """Yield (tier, code, name, has_medaled) tuples for all selectable countries."""
    for tier, countries in COUNTRIES_BY_TIER.items():
        for code, (name, has_medaled) in countries.items():
            yield tier, code, name, has_medaled


def all_country_codes() -> set[str]:
    """Return a set of all IOC codes for selectable countries."""
    return {code for _, code, _, _ in iter_countries()}


# =============================================================================
# IOC TO ISO 3166-1 ALPHA-2 MAPPINGS
# =============================================================================
# IOC codes (3-letter) used by Olympics differ from ISO codes (2-letter)
# used by flag services like flagcdn.com
#
# This is a COMPLETE mapping of all IOC codes to their correct ISO codes.
# The fallback of "take first 2 letters" does NOT work for most countries.
# =============================================================================

IOC_TO_ISO = {
    # Tier 1 - Elite
    'NOR': 'no',  # Norway
    'GER': 'de',  # Germany (NOT 'ge' which is Georgia!)
    'USA': 'us',  # United States
    'CAN': 'ca',  # Canada
    
    # Tier 2 - Strong
    'NED': 'nl',  # Netherlands (NOT 'ne')
    'AUT': 'at',  # Austria (NOT 'au' which is Australia!)
    'SWE': 'se',  # Sweden (NOT 'sw')
    'FRA': 'fr',  # France
    'SUI': 'ch',  # Switzerland (NOT 'su')
    'KOR': 'kr',  # South Korea (NOT 'ko')
    
    # Tier 3 - Competitive
    'CHN': 'cn',  # China
    'JPN': 'jp',  # Japan
    'ITA': 'it',  # Italy
    
    # Tier 4 - Emerging
    'FIN': 'fi',  # Finland
    'CZE': 'cz',  # Czech Republic
    'SLO': 'si',  # Slovenia (NOT 'sl')
    
    # Tier 5 - Occasional
    'POL': 'pl',  # Poland
    'GBR': 'gb',  # Great Britain
    'AUS': 'au',  # Australia
    'SVK': 'sk',  # Slovakia
    'LAT': 'lv',  # Latvia (NOT 'la')
    
    # Tier 6 - Wildcard (medaled 2010-2022)
    'NZL': 'nz',  # New Zealand
    'UKR': 'ua',  # Ukraine (NOT 'uk' which is United Kingdom!)
    'HUN': 'hu',  # Hungary
    'KAZ': 'kz',  # Kazakhstan
    'CRO': 'hr',  # Croatia (NOT 'cr')
    'BEL': 'be',  # Belgium
    'ESP': 'es',  # Spain
    'EST': 'ee',  # Estonia (NOT 'es' which is Spain!)
    'LIE': 'li',  # Liechtenstein
    
    # Tier 6 - Wildcard (no recent medals)
    'AND': 'ad',  # Andorra
    'ARG': 'ar',  # Argentina
    'ARM': 'am',  # Armenia
    'AZE': 'az',  # Azerbaijan
    'BIH': 'ba',  # Bosnia and Herzegovina
    'BRA': 'br',  # Brazil
    'BUL': 'bg',  # Bulgaria (NOT 'bu')
    'CHI': 'cl',  # Chile (NOT 'ch' which is Switzerland!)
    'COL': 'co',  # Colombia
    'CYP': 'cy',  # Cyprus
    'DEN': 'dk',  # Denmark (NOT 'de' which is Germany!)
    'GEO': 'ge',  # Georgia
    'GRE': 'gr',  # Greece
    'HKG': 'hk',  # Hong Kong
    'IND': 'in',  # India
    'IRI': 'ir',  # Iran
    'IRL': 'ie',  # Ireland (NOT 'ir' which is Iran!)
    'ISR': 'il',  # Israel (NOT 'is' which is Iceland!)
    'JAM': 'jm',  # Jamaica
    'KGZ': 'kg',  # Kyrgyzstan
    'LBN': 'lb',  # Lebanon
    'LTU': 'lt',  # Lithuania
    'LUX': 'lu',  # Luxembourg
    'MDA': 'md',  # Moldova
    'MEX': 'mx',  # Mexico (NOT 'me' which is Montenegro!)
    'MGL': 'mn',  # Mongolia (NOT 'mg' which is Madagascar!)
    'MKD': 'mk',  # North Macedonia
    'MNE': 'me',  # Montenegro
    'MAR': 'ma',  # Morocco
    'PAK': 'pk',  # Pakistan
    'PER': 'pe',  # Peru
    'PHI': 'ph',  # Philippines
    'POR': 'pt',  # Portugal (NOT 'po')
    'ROU': 'ro',  # Romania
    'RSA': 'za',  # South Africa (NOT 'rs' which is Serbia!)
    'SRB': 'rs',  # Serbia
    'SMR': 'sm',  # San Marino
    'TPE': 'tw',  # Chinese Taipei (Taiwan)
    'THA': 'th',  # Thailand
    'TUR': 'tr',  # Turkey
    'UZB': 'uz',  # Uzbekistan
}

# Legacy alias for backwards compatibility
IOC_TO_ISO_OVERRIDES = IOC_TO_ISO
