"""Define the report controller"""
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository


class ReportController:
    def __init__(
            self,
            player_repository: IPlayerRepository,
            tournament_repository: ITournamentRepository
    ):
        self.player_repository = player_repository
        self.tournament_repository = tournament_repository

    def generate_player_report(
            self,
            template_dir: str,
            template_name: str,
            output_path: str
    ):
        """
        Generate an HTML report of all players and open it in the default web browser.
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
    ):
        """
        Generate an HTML report of all tournaments and open it in the default web browser.
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
