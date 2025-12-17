"""
2026 Milano-Cortina Winter Olympics Pool - Template Helpers
============================================================
Utility functions for flags and display formatting.
"""

from data.countries import COUNTRIES_BY_TIER, IOC_TO_ISO_OVERRIDES


def _build_ioc_to_iso_map():
    """Build IOC→ISO map from canonical country data with optional overrides."""
    mapping = {}
    for tier_countries in COUNTRIES_BY_TIER.values():
        for code in tier_countries.keys():
            mapping[code] = code[:2].upper()

    mapping.update(IOC_TO_ISO_OVERRIDES)
    return mapping


# IOC Code to ISO 3166-1 alpha-2 mapping
IOC_TO_ISO = _build_ioc_to_iso_map()


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

    iso_code = IOC_TO_ISO.get(ioc_code.upper())

    if not iso_code:
        iso_code = ioc_code[:2].upper()

    try:
        flag = ''
        for char in iso_code.upper():
            code_point = 0x1F1E6 + ord(char) - ord('A')
            flag += chr(code_point)
        return flag
    except (ValueError, TypeError):
        return ''


def get_iso_code(ioc_code: str) -> str:
    """
    Get ISO code from IOC code.

    Args:
        ioc_code: Three-letter IOC country code

    Returns:
        Two-letter ISO code (lowercase)
    """
    if not ioc_code:
        return ''
    return IOC_TO_ISO.get(ioc_code.upper(), ioc_code[:2]).lower()


def get_flag_class(ioc_code: str) -> str:
    """
    Get CSS class for flag-icons library.

    Args:
        ioc_code: Three-letter IOC country code

    Returns:
        CSS class string for flag-icons (e.g., 'fi fi-us')
    """
    iso_code = get_iso_code(ioc_code)
    return f'fi fi-{iso_code}'


# Pre-generate flag lookup for all countries
FLAG_EMOJI_LOOKUP = {
    code: ioc_to_flag_emoji(code)
    for code in IOC_TO_ISO.keys()
}


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
