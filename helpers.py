"""
2026 Milano-Cortina Winter Olympics Pool - Template Helpers
============================================================
Utility functions for flags and display formatting.
"""

# IOC Code to ISO 3166-1 alpha-2 mapping
# (Flag emoji use ISO codes, not IOC codes)
IOC_TO_ISO = {
    # Tier 1 - Elite
    'NOR': 'NO',  # Norway
    'GER': 'DE',  # Germany
    'USA': 'US',  # United States
    'CAN': 'CA',  # Canada
    
    # Tier 2 - Strong
    'NED': 'NL',  # Netherlands
    'AUT': 'AT',  # Austria
    'SWE': 'SE',  # Sweden
    'FRA': 'FR',  # France
    'SUI': 'CH',  # Switzerland
    'KOR': 'KR',  # South Korea
    
    # Tier 3 - Competitive
    'CHN': 'CN',  # China
    'JPN': 'JP',  # Japan
    'ITA': 'IT',  # Italy (Host!)
    
    # Tier 4 - Emerging
    'FIN': 'FI',  # Finland
    'CZE': 'CZ',  # Czech Republic
    'SLO': 'SI',  # Slovenia
    
    # Tier 5 - Occasional
    'POL': 'PL',  # Poland
    'GBR': 'GB',  # Great Britain
    'AUS': 'AU',  # Australia
    'SVK': 'SK',  # Slovakia
    'LAT': 'LV',  # Latvia
    
    # Tier 6 - Wildcard (Medaled 2010-2022)
    'NZL': 'NZ',  # New Zealand
    'UKR': 'UA',  # Ukraine
    'HUN': 'HU',  # Hungary
    'KAZ': 'KZ',  # Kazakhstan
    'CRO': 'HR',  # Croatia
    'BEL': 'BE',  # Belgium
    'ESP': 'ES',  # Spain
    'EST': 'EE',  # Estonia
    'LIE': 'LI',  # Liechtenstein
    
    # Additional Tier 6 countries (common participants)
    'AND': 'AD',  # Andorra
    'ARG': 'AR',  # Argentina
    'ARM': 'AM',  # Armenia
    'AZE': 'AZ',  # Azerbaijan
    'BIH': 'BA',  # Bosnia and Herzegovina
    'BRA': 'BR',  # Brazil
    'BUL': 'BG',  # Bulgaria
    'CHI': 'CL',  # Chile
    'COL': 'CO',  # Colombia
    'CYP': 'CY',  # Cyprus
    'DEN': 'DK',  # Denmark
    'GEO': 'GE',  # Georgia
    'GRE': 'GR',  # Greece
    'HKG': 'HK',  # Hong Kong
    'IND': 'IN',  # India
    'IRI': 'IR',  # Iran
    'IRL': 'IE',  # Ireland
    'ISR': 'IL',  # Israel
    'JAM': 'JM',  # Jamaica
    'KGZ': 'KG',  # Kyrgyzstan
    'LBN': 'LB',  # Lebanon
    'LTU': 'LT',  # Lithuania
    'LUX': 'LU',  # Luxembourg
    'MDA': 'MD',  # Moldova
    'MEX': 'MX',  # Mexico
    'MGL': 'MN',  # Mongolia
    'MKD': 'MK',  # North Macedonia
    'MNE': 'ME',  # Montenegro
    'MAR': 'MA',  # Morocco
    'PAK': 'PK',  # Pakistan
    'PER': 'PE',  # Peru
    'PHI': 'PH',  # Philippines
    'POR': 'PT',  # Portugal
    'ROU': 'RO',  # Romania
    'RSA': 'ZA',  # South Africa
    'SRB': 'RS',  # Serbia
    'SMR': 'SM',  # San Marino
    'TPE': 'TW',  # Chinese Taipei
    'THA': 'TH',  # Thailand
    'TUR': 'TR',  # Turkey
    'UZB': 'UZ',  # Uzbekistan
}


def ioc_to_flag_emoji(ioc_code: str) -> str:
    """
    Convert IOC country code to flag emoji.
    
    Flag emoji are created by combining regional indicator symbols.
    For example: US -> 🇺🇸
    
    Args:
        ioc_code: Three-letter IOC country code (e.g., 'USA', 'NOR')
    
    Returns:
        Flag emoji string, or empty string if not found
    """
    iso_code = IOC_TO_ISO.get(ioc_code.upper())
    
    if not iso_code:
        # Try using first two letters of IOC code as fallback
        iso_code = ioc_code[:2].upper()
    
    try:
        # Convert ISO code to flag emoji
        # Regional indicator symbols start at U+1F1E6 (🇦)
        # A = 0, B = 1, etc.
        flag = ''
        for char in iso_code.upper():
            # 0x1F1E6 is the Unicode code point for regional indicator A
            flag += chr(0x1F1E6 + ord(char) - ord('A'))
        return flag
    except (ValueError, TypeError):
        return ''


def get_flag_class(ioc_code: str) -> str:
    """
    Get CSS class for flag-icons library.
    
    Args:
        ioc_code: Three-letter IOC country code
    
    Returns:
        CSS class string for flag-icons (e.g., 'fi fi-us')
    """
    iso_code = IOC_TO_ISO.get(ioc_code.upper(), ioc_code[:2]).lower()
    return f'fi fi-{iso_code}'


# Pre-generate flag lookup for all countries
FLAG_EMOJI_LOOKUP = {
    code: ioc_to_flag_emoji(code)
    for code in IOC_TO_ISO.keys()
}


def register_template_helpers(app):
    """Register Jinja2 template filters and globals."""
    
    @app.template_filter('flag')
    def flag_filter(ioc_code):
        """Jinja2 filter to convert IOC code to flag emoji."""
        return ioc_to_flag_emoji(ioc_code)
    
    @app.template_filter('flag_class')
    def flag_class_filter(ioc_code):
        """Jinja2 filter to get flag-icons CSS class."""
        return get_flag_class(ioc_code)
    
    # Add to template globals
    app.jinja_env.globals['flag_emoji'] = ioc_to_flag_emoji
    app.jinja_env.globals['FLAG_LOOKUP'] = FLAG_EMOJI_LOOKUP
