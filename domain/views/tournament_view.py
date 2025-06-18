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
        table.add_column("ID", style="bold blue")
        table.add_column("Status", style="bold blue")
        for tournament in tournaments:
            table.add_row(
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                tournament.description,
                tournament.tournament_id,
                tournament.status
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

    def add_player_to_tournament_flow(self):
        """
        Add player to a tournament.
        If the player is not registered in the list of players, he is added
        to the player repository and then added to the tournament.
        """
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()
        tournament_to_be_played_id = input("Entrez un ID de tournoi:")
        tournaments = self.controller.list_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_to_be_played_id:
                if tournament.status == "Terminé":
                    print("\nCe tournoi est terminé")
                    return
                print(f"\nCe tournoi est {tournament.status}")

        player_to_add_id = input("Entrez l'identifiant du joueur à ajouter au tournoi:")
        player_to_add = self.controller.player_repository.get_by_id(player_to_add_id)

        if player_to_add is None:
            self.console.print("\n[bold blue]Entrez les informations "
                               "du joueur:[/bold blue]")
            last_name = input("Nom de famille: ")
            first_name = input("Prénom: ")
            birth_date = input("Date de naissance (format AAAA-MM-JJ): ")

            self.player_controller.create_player(
                last_name=last_name,
                first_name=first_name,
                birth_date=birth_date,
                national_chess_id=player_to_add_id
            )
            player_to_add = self.controller.player_repository.get_by_id(player_to_add_id)

        print(f"\nConfirmez-vous l'ajout du joueur {str(player_to_add)} au tournoi?")
        answer = input("O/n")
        if answer == "O":
            tournament_to_be_played = self.controller.tournament_repository.get_by_id(tournament_to_be_played_id)
            players = tournament_to_be_played.players
            players.append(player_to_add)

            self.controller.update_tournament(
                tournament_to_be_played_id,
                players=players
            )

    def start_tournament_flow(self):
        print("Démarrer un tournoi")

    def input_results_flow(self):
        print("Saisir des résultats d'un round")

    def show_tournament_details_flow(self):
        print("Afficher les infos d'un tournoi")
