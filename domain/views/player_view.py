"""Player view managing the user interface for player CRUD operations."""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from domain.controllers.player_controller import PlayerController
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.utils.validators import is_valid_name, is_valid_birth_date, is_valid_national_chess_id


class PlayerView:
    def __init__(self):
        """
        Initialize the view with a PlayerController instance and Rich Console.
        """
        self.controller = PlayerController(JSONPlayerRepository())
        self.console = Console(force_terminal=True)

    def display_menu(self):
        """
        Display the player menu and route user choices to corresponding actions.
        Loop until user chooses to return to the main menu.
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
            table.add_row("5", "Retourner au menu principal")

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
                break
            else:
                self.console.print("[bold red]Choix invalide. "
                                   "Veuillez réessayer.[/bold red]")

    def list_players_flow(self):
        """Display a table listing all players."""

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
        """Prompt for new player details and create the player via the controller."""
        self.console.print("\n[bold blue]Entrez les informations du joueur:[/bold blue]")

        while True:
            last_name = input("Nom de famille: ").strip()
            if is_valid_name(last_name):
                break
            self.console.print("[bold red]Nom invalide. Veuillez réessayer.[/bold red]")

        while True:
            first_name = input("Prénom: ").strip()
            if is_valid_name(first_name):
                break
            self.console.print("[bold red]Prénom invalide. Veuillez réessayer.[/bold red]")

        while True:
            birth_date = input("Date de naissance (format JJ-MM-AAAA): ").strip()
            if is_valid_birth_date(birth_date):
                break
            self.console.print("[bold red]Format invalide. Utilisez JJ-MM-AAAA.")

        while True:
            national_chess_id = input("Identifiant national d'échecs (ex: AB12345): ").strip()
            if is_valid_national_chess_id(national_chess_id):
                break
            self.console.print("[bold red]Identifiant invalide. Veuillez réessayer."
                               "Format attendu : 2 lettres suivies de 5 chiffres (ex: AB12345).[/bold red]")

        player = self.controller.create_player(
            last_name, first_name, birth_date, national_chess_id
        )
        self.console.print(f"[bold green]"
                           f"Le joueur {player.first_name} {player.last_name} "
                           f"a été ajouté.[/bold green]")

    def update_player_flow(self):
        """
        Prompt for player ID and new data, then update the player via the controller.
        """
        self.console.print("\n[bold blue]Entrez l'identifiant national "
                           "d'échecs du joueur à mettre à jour: [/bold blue]")

        while True:
            national_chess_id = input()
            if is_valid_national_chess_id(national_chess_id):
                break
            self.console.print("[bold red]Identifiant invalide. "
                               "Veuillez réessayer.[/bold red]")

        player = self.controller.get_by_id(national_chess_id)
        if not player:
            self.console.print(f"[bold red]Aucun joueur trouvé pour l'identifiant "
                               f"{national_chess_id}.[/bold red]")
            return

        table = Table(title="Joueur à mettre à jour", show_header=True, header_style="bold magenta")
        table.add_column("Champ", style="bold cyan")
        table.add_column("Valeur actuelle", style="white")
        table.add_row("Nom", player.last_name)
        table.add_row("Prénom", player.first_name)
        table.add_row("Date de naissance", player.birth_date)
        self.console.print(table)

        self.console.print("[bold blue]Laissez vide les champs à conserver.[/bold blue]")

        while True:
            new_last_name = input("Nom de famille: ").strip()
            if not new_last_name or is_valid_name(new_last_name):
                break
            self.console.print(
                "[bold red]Nom invalide. Veuillez réessayer.[/bold red]")

        while True:
            new_first_name = input("Prénom: ").strip()
            if not new_first_name or is_valid_name(new_first_name):
                break
            self.console.print(
                "[bold red]Prénom invalide. Veuillez réessayer.[/bold red]")

        while True:
            new_birth_date = input("Date de naissance (JJ-MM-AAAA): ").strip()
            if not new_birth_date or is_valid_birth_date(new_birth_date):
                break
            self.console.print("[bold red]Format invalide. Utilisez JJ-MM-AAAA.[/bold red]")

        success = self.controller.update_player(
            national_chess_id,
            new_last_name or None,
            new_first_name or None,
            new_birth_date or None
        )

        if success:
            self.console.print(f"[bold green]Le joueur {national_chess_id} a été mis à jour avec succès.[/bold green]")
        else:
            self.console.print(f"[bold red]Erreur lors de la mise à jour du joueur {national_chess_id}.[/bold red]")

    def delete_player_flow(self):
        """
        Prompt for player ID and delete the player via the controller.
        """
        self.console.print("\n[bold blue]Entrez l'identifiant national "
                           "d'échecs du joueur à supprimer: [/bold blue]")

        while True:
            national_chess_id = input()
            if is_valid_national_chess_id(national_chess_id):
                break
            self.console.print("[bold red]Identifiant invalide. "
                               "Veuillez réessayer.[/bold red]")

        player = self.controller.get_by_id(national_chess_id)
        if not player:
            self.console.print(f"[bold red]Aucun joueur trouvé pour l'identifiant "
                               f"{national_chess_id}.[/bold red]")
            return

        table = Table(title="Joueur à supprimer", show_header=True, header_style="bold magenta")
        table.add_column("Champ", style="bold cyan")
        table.add_column("Valeur", style="white")
        table.add_row("Nom", player.last_name)
        table.add_row("Prénom", player.first_name)
        table.add_row("Date de naissance", player.birth_date)
        self.console.print(table)

        answer = input("Confirmez la suppression ? [O/n]: ").strip().lower()
        if answer not in ("", "o", "oui"):
            self.console.print("[bold yellow]Suppression annulée.[/bold yellow]")
            return

        success = self.controller.delete_player(national_chess_id)

        if success:
            self.console.print(f"[bold green]Le joueur {national_chess_id} "
                               f"a été supprimé avec succès.[/bold green]")
        else:
            self.console.print(f"[bold red]L'identifiant {national_chess_id} "
                               f"n'a pas été trouvé.[/bold red]")
