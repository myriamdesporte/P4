"""Handle player and tournament report generation operations."""

import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository
from infra.utils.tournament_utils import tournament_with_loaded_players


def format_french_datetime(value: datetime) -> str:
    """Format datetime in French style: DD/MM/YYYY à HHhMM."""
    if not value:
        return ""
    return value.strftime("%d/%m/%Y à %Hh%M")


class ReportController:
    def __init__(
            self,
            player_repository: IPlayerRepository,
            tournament_repository: ITournamentRepository
    ):
        """Initialize the report controller with player and tournament repositories."""
        self.player_repository = player_repository
        self.tournament_repository = tournament_repository

    def generate_player_report(
            self,
            template_dir: str,
            template_name: str,
            output_path: str
    ) -> str:
        """
        Generate an HTML report of all players and open it in the default web browser.

        Args:
            template_dir (str): Directory containing the Jinja2 template.
            template_name (str): Name of the template file.
            output_path (str): Output file path for the report.

        Returns:
            str: Path to the generated HTML report.
        """

        players = self.player_repository.load_players()

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html'])
        )
        template = env.get_template(template_name)
        rendered_html = template.render(players=players)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        return output_path

    def generate_tournaments_report(
            self,
            template_dir: str,
            template_name: str,
            output_path: str
    ) -> str:
        """
        Generate an HTML report of all tournaments and open it in the default web browser.

        Args:
            template_dir (str): Directory containing the Jinja2 template.
            template_name (str): Name of the template file.
            output_path (str): Output file path for the report.

        Returns:
            str: Path to the generated HTML report.
        """

        tournaments = self.tournament_repository.load_tournaments()

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html'])
        )
        template = env.get_template(template_name)
        rendered_html = template.render(tournaments=tournaments)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        return output_path

    def generate_tournament_details_report(
            self,
            template_dir: str,
            template_name: str,
            output_dir: str,
            tournament_id: str,
    ) -> str:
        """
        Generate an HTML detailed report for a single tournament.

        Args:
            template_dir (str): Directory containing the Jinja2 template.
            template_name (str): Template file name.
            output_dir (str): Output directory for the report.
            tournament_id (str): Tournament identifier.

        Returns:
            str: Path to the generated HTML report.
        """

        tournament = tournament_with_loaded_players(
            tournament=self.tournament_repository.get_by_id(tournament_id),
            player_repository=self.player_repository
        )

        env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html'])
        )
        env.filters["format_fr"] = format_french_datetime
        template = env.get_template(template_name)

        tournament.players = sorted(
            tournament.players,
            key=lambda p: p.last_name.lower()
        )

        sorted_scores = sorted(
            tournament.scores.items(),
            key=lambda item: item[1],
            reverse=True
        )

        ranking = []
        for player_id, score in sorted_scores:
            player = self.player_repository.get_by_id(player_id)
            if player:
                ranking.append((player, score))

        rendered_html = template.render(tournament=tournament, ranking=ranking)

        filename = f"tournament_{tournament_id}_report.html"
        output_path = os.path.normpath(os.path.join(output_dir, filename))
        os.makedirs(output_dir, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        return output_path
