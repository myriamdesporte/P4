"""Define the tournament view."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from domain.controllers.tournament_controller import TournamentController
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.repositories.json_tournament_repository import JSONTournamentRepository


class TournamentView:
    def __init__(self):
        """
        Initialize the view with a TournamentController instance and Rich Console
        """
        tournament_repository = JSONTournamentRepository()
        player_repository = JSONPlayerRepository()
        self.controller = TournamentController(
            tournament_repository,
            player_repository
        )
        self.console = Console(force_terminal=True)

    def display_menu(self):
        """
        Display the main menu and route user choices to corresponding actions.
        """
        while True:
            self.console.print(Panel.fit("[bold magenta]Tournoi d'échecs - "
                                         "Bienvenue dans le gestionnaire de "
                                         "tournois[/bold magenta]"))
            table = Table(box=None)
            table.add_column("Option", justify="center", style="bold")
            table.add_column("Action", style="bold blue")
            table.add_row("1", "Afficher la liste des tournois")
            table.add_row("2", "Créer un nouveau tournoi")
            table.add_row("3", "Retourner au menu principal")
            self.console.print(table)
            choice = input("\nEntrez votre choix: ")
            if choice == "1":
                self.list_tournaments_flow()
            elif choice == "2":
                self.add_tournament_flow()
            elif choice == "3":
                break
            else:
                self.console.print("[bold red]Choix invalide. "
                                   "Veuillez réessayer.[/bold red]")

    def list_tournaments_flow(self):
        """
        Display all saved tournaments from the controller.
        """
        tournaments = self.controller.list_tournaments()
        if not tournaments:
            self.console.print("[bold yellow]Aucun tournoi trouvé.[/bold yellow]")
            return
        table = Table(title="Liste des tournois",
                      show_header=True,
                      header_style="bold magenta")
        table.add_column("Nom", style="bold blue")
        table.add_column("Lieu", style="cyan")
        table.add_column("Date début", style="white", justify="center")
        table.add_column("Date fin", style="white", justify="center")
        table.add_column("Description", style="dim")
        for tournament in tournaments:
            table.add_row(
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                tournament.description
            )
        self.console.print(table)

    def add_tournament_flow(self):
        """
        Prompt the user to enter information for a new tournament.
        """
        self.console.print("\n[bold blue]Entrez les informations du tournoi :[/bold blue]")
        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date = input("Date de début (format AAAA-MM-JJ) : ")
        end_date = input("Date de fin (format AAAA-MM-JJ) : ")
        description = input("Description : ")
        tournament = self.controller.create_tournament(
            name, location, start_date, end_date, description=description
        )
        self.console.print(f"[bold green]Le tournoi '{tournament.name}' a été créé avec succès.[/bold green]")