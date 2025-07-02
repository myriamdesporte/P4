"""Define the report view."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from domain.controllers.player_controller import PlayerController
from infra.reports.players_report_generator import generate_player_report
from infra.repositories.json_player_repository import JSONPlayerRepository


class ReportView:
    def __init__(self):
        """
        Initialize the view with a PlayerController instance and Rich Console.
        """
        self.controller = PlayerController(JSONPlayerRepository())
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
        generate_player_report()
        self.console.print("[bold green]Rapport HTML généré et ouvert dans le navigateur.[/bold green]")

    def list_tournaments_flow(self):
        self.console.print("[bold green]Rapport HTML: liste de tous les tournois.[/bold green]")

    def show_tournament_details_flow(self):
        self.console.print("[bold green]Rapport HTML: détails d'un tournoi (nom, dates, liste des joueurs et détails des rounds).[/bold green]")