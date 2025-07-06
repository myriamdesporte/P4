"""Define the report view."""

import os
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from domain.controllers.report_controller import ReportController
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.repositories.json_tournament_repository import JSONTournamentRepository

TEMPLATE_DIR = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "templates")
)

PLAYERS_TEMPLATE_NAME = "players_report_template.html"

PLAYERS_REPORT_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "generated_reports",
        "players_report.html"
    )
)

TOURNAMENTS_TEMPLATE_NAME = "tournaments_report_template.html"

TOURNAMENTS_REPORT_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "..",
        "generated_reports",
        "tournaments_report.html"
    )
)

class ReportView:
    def __init__(self):
        """
        Initialize the view with a ReportController instance and Rich Console.
        """
        self.controller = ReportController(
            player_repository=JSONPlayerRepository(),
            tournament_repository=JSONTournamentRepository()
        )
        self.console = Console(force_terminal=True)

    def display_menu(self):
        """
        Display the main menu and route user choices to corresponding actions.
        """
        while True:
            self.console.print(Panel.fit("[bold magenta]Tournoi d'échecs - "
                                         "Bienvenue dans le gestionnaire de "
                                         "joueurs[/bold magenta]"))

            table = Table(box=None)
            table.add_column("Option", justify="center", style="bold")
            table.add_column("Action", style="bold blue")

            table.add_row("1", "Afficher la liste des joueurs (ordre alphabétique)")
            table.add_row("2", "Afficher la liste de tous les tournois")
            table.add_row("3", "Afficher les informations d'un tournoi")
            table.add_row("4", "Retourner au menu principal")

            self.console.print(table)

            choice = input("\nEntrez votre choix: ")

            if choice == "1":
                self.list_players_flow()
            elif choice == "2":
                self.list_tournaments_flow()
            elif choice == "3":
                self.show_tournament_details_flow()
            elif choice == "4":
                break
            else:
                self.console.print("[bold red]Choix invalide. Veuillez réessayer.[/bold red]")

    def list_players_flow(self):
        players_report_path = self.controller.generate_player_report(
            template_dir=TEMPLATE_DIR,
            template_name=PLAYERS_TEMPLATE_NAME,
            output_path=PLAYERS_REPORT_PATH
        )
        report_name = Path(players_report_path).name
        webbrowser.open(f"file://{players_report_path}")
        self.console.print(f"\n[bold green] 📄Rapport {report_name} généré et ouvert dans le navigateur.[/bold green]")

    def list_tournaments_flow(self):
        tournaments_report_path = self.controller.generate_tournaments_report(
            template_dir=TEMPLATE_DIR,
            template_name=TOURNAMENTS_TEMPLATE_NAME,
            output_path=TOURNAMENTS_REPORT_PATH
        )
        report_name = Path(tournaments_report_path).name
        webbrowser.open(f"file://{tournaments_report_path}")
        self.console.print(f"\n[bold green] 📄Rapport {report_name} généré et ouvert dans le navigateur.[/bold green]")

    def show_tournament_details_flow(self):
        self.console.print(f"\n[bold green] 📄Rapport généré et ouvert dans le navigateur.[/bold green]")
