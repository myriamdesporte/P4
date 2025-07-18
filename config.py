"""Configuration constants and paths used across the application."""

import os

BASE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)))
)

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
GENERATED_REPORTS_DIR = os.path.join(BASE_DIR, "generated_reports")

# HTML Templates
PLAYERS_TEMPLATE_NAME = "players_report_template.html"
TOURNAMENTS_TEMPLATE_NAME = "tournaments_report_template.html"
TOURNAMENT_DETAILS_TEMPLATE_NAME = "tournament_details_report_template.html"

# Output files
PLAYERS_REPORT_PATH = os.path.join(GENERATED_REPORTS_DIR, "players_report.html")
TOURNAMENTS_REPORT_PATH = os.path.join(GENERATED_REPORTS_DIR, "tournaments_report.html")
