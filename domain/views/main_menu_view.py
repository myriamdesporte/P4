"""Main menu view to navigate between players, tournaments, and reports."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository
from domain.views.player_view import PlayerView
from domain.views.report_view import ReportView
from domain.views.tournament_view import TournamentView


class MainMenuView:
    def __init__(
            self,
            player_repository: IPlayerRepository,
            tournament_repository: ITournamentRepository
    ):
        """Initialize with subviews and Rich console."""
        self.player_view = PlayerView(
            repository=player_repository
        )
        self.tournament_view = TournamentView(
            player_repository=player_repository,
            tournament_repository=tournament_repository
        )
        self.report_view = ReportView(
            player_repository=player_repository,
            tournament_repository=tournament_repository
        )
        self.console = Console(force_terminal=True)

    def run(self):
        """
        Display the main menu and route user commands to corresponding views.
        Loop until user chooses to quit.
        """
        while True:
            self.console.print(Panel.fit("[bold magenta]Tournoi d'échecs - "
                                         "Menu principal[/bold magenta]"))

            table = Table(box=None)
            table.add_column("Option", justify="center", style="bold")
            table.add_column("Action", style="bold blue")

            table.add_row("1", "Gestionnaire de joueurs")
            table.add_row("2", "Gestionnaire de tournois")
            table.add_row("3", "Rapports")
            table.add_row("4", "Quitter")

            self.console.print(table)

            choice = input("\nEntrez votre choix: ")

            if choice == "1":
                self.player_view.display_menu()
            elif choice == "2":
                self.tournament_view.display_menu()
            elif choice == "3":
                self.report_view.display_menu()
            elif choice == "4":
                self.console.print("[bold blue]Au revoir ![/bold blue]")
                break
            else:
                self.console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")
