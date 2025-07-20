"""
Validation helpers for input fields such as names, dates, and IDs.
Used across CLI views to ensure clean and consistent data entry.
"""

import re
from datetime import datetime


def is_valid_name(name: str) -> bool:
    """
    Check if the name contains only letters, spaces, or hyphens.
    """
    return bool(re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9\- ]+", name))


def is_valid_date(date_str: str) -> bool:
    """Check if the date of birth is in DD-MM-YYYY format."""
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def is_valid_number(value: str, min_value: int = 1, max_value: int = 10) -> bool:
    """Check if the value is a digit between min_value and max_value."""
    if not value.isdigit():
        return False
    number = int(value)
    return min_value <= number <= max_value


def is_valid_national_chess_id(national_chess_id: str) -> bool:
    """Check if the national chess ID matches format: 2 uppercase letters + 5 digits."""
    return bool(re.fullmatch(r"[A-Z]{2}\d{5}", national_chess_id))


def is_valid_tournament_id(tournament_id: str) -> bool:
    """Check if the tournament ID matches the format: 'T' followed by 3 digits."""
    return bool(re.fullmatch(r"T\d{3}", tournament_id))
