from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from domain.controllers.player_controller import PlayerController
from domain.controllers.tournament_controller import TournamentController
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.repositories.json_tournament_repository import JSONTournamentRepository


class TournamentView:
    def __init__(self):
        """
        Initialize the view with a TournamentController instance and Rich Console
        """
        self.controller = TournamentController(
            tournament_repository=JSONTournamentRepository(),
            player_repository=JSONPlayerRepository()
        )
        self.player_controller = PlayerController(
            repository=JSONPlayerRepository()
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

            table.add_row("1", "Voir la liste des tournois")
            table.add_row("2", "Créer un nouveau tournoi")
            table.add_row("3", "Ajouter un joueur à un tournoi")
            table.add_row("4", "Débuter un tournoi")
            table.add_row("5", "Saisir les résultats d'un tour")
            table.add_row("6", "Voir les informations d'un tournoi")
            table.add_row("7", "Retourner au menu principal")

            self.console.print(table)

            choice = input("\nEntrez votre choix: ")

            if choice == "1":
                self.list_tournaments_flow()
            elif choice == "2":
                self.add_tournament_flow()
            elif choice == "3":
                self.add_player_to_tournament_flow()
            elif choice == "4":
                self.start_tournament_flow()
            elif choice == "5":
                self.input_results_flow()
            elif choice == "6":
                self.show_tournament_details_flow()
            elif choice == "7":
                break
            else:
                self.console.print("[bold red]Choix invalide. "
                                   "Veuillez réessayer.[/bold red]")

    def list_tournaments_flow(self):
        print("Afficher la liste des tournois")

    def add_tournament_flow(self):
        print("Créer un nouveau tournoi")

    def add_player_to_tournament_flow(self):
        print("Ajouter un joueur à un tournoi")

    def start_tournament_flow(self):
        print("Démarrer un tournoi")

    def input_results_flow(self):
        print("Saisir des résultats d'un round")

    def show_tournament_details_flow(self):
        print("Afficher les infos d'un tournoi")
