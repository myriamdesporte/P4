"""Define the player view."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from domain.controllers.player_controller import PlayerController
from infra.repositories.json_player_repository import JSONPlayerRepository


class PlayerView:
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

            table.add_row("1", "Afficher la liste des joueurs")
            table.add_row("2", "Ajouter un nouveau joueur")
            table.add_row("3", "Mettre à jour les informations d'un joueur")
            table.add_row("4", "Supprimer un joueur")
            table.add_row("5", "Quitter")

            self.console.print(table)

            choice = input("\nEntrez votre choix: ")

            if choice == "1":
                self.list_players_flow()
            elif choice == "2":
                self.add_player_flow()
            elif choice == "3":
                self.update_player_flow()
            elif choice == "4":
                self.delete_player_flow()
            elif choice == "5":
                self.console.print("[bold blue]A bientôt![/bold blue]")
                break
            else:
                self.console.print("[bold red]Choix invalide. "
                                   "Veuillez réessayer.[/bold red]")

    def list_players_flow(self):
        """
        Display all saved players from the controller.
        """
        players = self.controller.list_players()
        if not players:
            self.console.print("[bold yellow]No players found.[/bold yellow]")
            return

        table = Table(title="Liste des joueurs",
                      show_header=True,
                      header_style="bold magenta")
        table.add_column("Nom", style="bold blue")
        table.add_column("Prénom", style="blue")
        table.add_column("Date de naissance",
                         justify="center",
                         style="white")
        table.add_column("INE", justify="center", style="green")

        for player in players:
            table.add_row(
                player.last_name,
                player.first_name,
                player.birth_date,
                player.national_chess_id
            )

        self.console.print(table)

    def add_player_flow(self):
        """
        Prompt the user to enter information for a new player
        and delegate player creation to the controller.
        """
        self.console.print("\n[bold blue]Entrez les informations "
                           "du joueur:[/bold blue]")
        last_name = input("Nom de famille: ")
        first_name = input("Prénom: ")
        birth_date = input("Date de naissance (format AAAA-MM-JJ): ")
        national_chess_id = input("Identifiant national d'échecs "
                                  "(ex: AB12345): ")

        player = self.controller.create_player(
            last_name, first_name, birth_date, national_chess_id
        )
        self.console.print(f"[bold green]"
                           f"Le joueur {player.first_name} {player.last_name} "
                           f"a été ajouté.[/bold green]")

    def update_player_flow(self):
        """
        Update the information of a player.
        """
        self.console.print("\n[bold blue]Entrez l'identifiant national "
                           "d'échecs du joueur à mettre à jour: [/bold blue]")
        national_id = input()
        self.console.print("[bold blue]Laissez vide les champs "
                           "à conserver.[/bold blue]")
        new_last_name = input("Nom de famille: ")
        new_first_name = input("Prénom: ")
        new_birth_date = input("Date de naissance (AAAA-MM-JJ): ")

        success = self.controller.update_player(
            national_id,
            new_last_name or None,
            new_first_name or None,
            new_birth_date or None
        )

        if success:
            self.console.print(f"[bold green]Le joueur {national_id} "
                               f"a été mis à jour avec succès.[/bold green]")
        else:
            self.console.print(f"[bold red]L'identifiant {national_id} "
                               f"n'a pas été trouvé.[/bold red]")

    def delete_player_flow(self):
        """
        Delete a player.
        """
        self.console.print("\n[bold blue]Entrez l'identifiant national "
                           "d'échecs du joueur à supprimer: [/bold blue]")
        national_id = input()
        success = self.controller.delete_player(national_id)

        if success:
            self.console.print(f"[bold green]Le joueur {national_id} "
                               f"a été supprimé avec succès.[/bold green]")
        else:
            self.console.print(f"[bold red]L'identifiant {national_id} "
                               f"n'a pas été trouvé.[/bold red]")
