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
        # Uncomment or extend as official participant lists are confirmed
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


# Optional ISO overrides (non-standard IOC→ISO differences or legacy codes)
IOC_TO_ISO_OVERRIDES = {
    'GRE': 'GR',
    'DEN': 'DK',
    'POR': 'PT',
}
