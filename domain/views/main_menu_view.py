"""Define the view of the main menu."""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from domain.views.player_view import PlayerView
from domain.views.tournament_view import TournamentView


class MainMenuView:
    def __init__(self):
        self.player_view = PlayerView()
        self.tournament_view = TournamentView()
        self.console = Console(force_terminal=True)

    def display_menu(self):
        while True:
            self.console.print(Panel.fit("[bold magenta]Tournoi d'échecs - "
                                         "Menu principal[/bold magenta]"))

            table = Table(box=None)
            table.add_column("Option", justify="center", style="bold")
            table.add_column("Action", style="bold blue")

            table.add_row("1", "Gestionnaire de joueurs")
            table.add_row("2", "Gestionnaire de tournois")
            table.add_row("3", "Quitter")

            self.console.print(table)

            choice = input("\nEntrez votre choix: ")

            if choice == "1":
                self.player_view.display_menu()
            elif choice == "2":
                self.tournament_view.display_menu()
            elif choice == "3":
                self.console.print("[bold blue]Au revoir ![/bold blue]")
                break
            else:
                self.console.print("[bold red]Choix invalide, veuillez réessayer.[/bold red]")
