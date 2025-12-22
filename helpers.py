"""
2026 Milano-Cortina Winter Olympics Pool - Template Helpers
============================================================
Utility functions for flags and display formatting.
"""

from data.countries import COUNTRIES_BY_TIER, IOC_TO_ISO


def get_iso_code(ioc_code: str) -> str:
    """
    Get ISO 3166-1 alpha-2 code from IOC code.
    
    Uses the complete IOC_TO_ISO mapping from data/countries.py.
    Returns lowercase ISO code for use with flag services.

    Args:
        ioc_code: Three-letter IOC country code (e.g., 'USA', 'GER', 'SUI')

    Returns:
        Two-letter ISO code (lowercase) for flag services
    """
    if not ioc_code:
        return ''
    
    ioc_upper = ioc_code.upper()
    
    # Look up in the complete mapping
    if ioc_upper in IOC_TO_ISO:
        return IOC_TO_ISO[ioc_upper]
    
    # Fallback: log warning and return empty (better than wrong flag)
    print(f"WARNING: Unknown IOC code '{ioc_code}' - no ISO mapping found")
    return ''


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
    if not ioc_code:
        return ''

    # Get the correct ISO code first
    iso_code = get_iso_code(ioc_code)
    
    if not iso_code:
        return ''

    try:
        flag = ''
        for char in iso_code.upper():
            code_point = 0x1F1E6 + ord(char) - ord('A')
            flag += chr(code_point)
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
    iso_code = get_iso_code(ioc_code)
    if not iso_code:
        return ''
    return f'fi fi-{iso_code}'


def get_flag_url(ioc_code: str, width: int = 80) -> str:
    """
    Get the flagcdn.com URL for a country flag.
    
    Args:
        ioc_code: Three-letter IOC country code
        width: Image width in pixels (default 80)
    
    Returns:
        URL to flag image, or empty string if mapping not found
    """
    iso_code = get_iso_code(ioc_code)
    if not iso_code:
        return ''
    return f'https://flagcdn.com/w{width}/{iso_code}.png'


def register_template_helpers(app):
    """Register Jinja2 template filters and globals."""

    from markupsafe import Markup

    @app.template_filter('flag')
    def flag_filter(ioc_code):
        """
        Jinja2 filter to convert IOC code to flag emoji.
        Usage: {{ 'USA'|flag }} -> 🇺🇸
        """
        return ioc_to_flag_emoji(ioc_code)

    @app.template_filter('flag_class')
    def flag_class_filter(ioc_code):
        """Jinja2 filter to get flag-icons CSS class."""
        return get_flag_class(ioc_code)

    @app.template_filter('iso')
    def iso_code_filter(ioc_code):
        """
        Convert IOC code to ISO 3166-1 alpha-2 code for flag assets.
        Usage: {{ 'GER'|iso }} -> 'de'
        """
        return get_iso_code(ioc_code)

    @app.template_filter('flag_img')
    def flag_img_filter(ioc_code, height='1.5rem'):
        """
        Jinja2 filter to generate a complete flag <img> tag.
        Usage: {{ 'USA'|flag_img }} or {{ 'USA'|flag_img('2rem') }}
        
        Returns an img tag with the country flag, or empty string if not found.
        """
        iso_code = get_iso_code(ioc_code)
        if not iso_code:
            return ''
        
        url = f'https://flagcdn.com/w80/{iso_code}.png'
        return Markup(
            f'<img src="{url}" alt="{ioc_code}" '
            f'style="height: {height}; width: auto; border-radius: 2px; '
            f'box-shadow: 0 1px 3px rgba(0,0,0,0.2); vertical-align: middle;">'
        )

    @app.template_filter('medal_count')
    def medal_count_filter(country):
        """
        Display medal count with icons.
        Usage: {{ country|medal_count }}
        """
        if not country:
            return ''

        return Markup(
            f"🥇 {country.gold_count} | 🥈 {country.silver_count} | 🥉 {country.bronze_count}"
        )

    @app.template_global()
    def medal_points(country):
        """
        Get total medal points for a country.
        """
        if not country:
            return 0
        return country.calculate_points()

    @app.template_global()
    def medal_breakdown(country):
        """
        Get detailed medal points breakdown for a country.
        Returns dict with counts and totals per medal type.
        """
        if not country:
            return {}
        return country.get_medal_points_breakdown()

    @app.template_filter('medal_status')
    def medal_status_filter(has_medaled):
        """
        Display medal history indicator for Tier 6 countries.
        Returns ⚫ if medaled recently, ⚪ otherwise.
        """
        return '⚫' if has_medaled else '⚪'
