"""Tournament view managing the user interface for tournament operations."""

from random import randint

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from domain.controllers.player_controller import PlayerController
from domain.controllers.round_controller import RoundController
from domain.controllers.tournament_controller import TournamentController
from domain.models.match import Match
from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository
from domain.views.components.input_view import InputView
from infra.utils.match_utils import match_with_loaded_players
from infra.utils.tournament_utils import create_pairs_for_next_round


class TournamentView:
    def __init__(
            self,
            player_repository: IPlayerRepository,
            tournament_repository: ITournamentRepository
    ):
        """
        Initialize the tournament view with controllers, console, and sub-views.
        """
        self.tournament_controller = TournamentController(
            tournament_repository=tournament_repository,
            player_repository=player_repository
        )
        self.player_controller = PlayerController(
            repository=player_repository
        )
        self.round_controller = RoundController(
            tournament_repository=tournament_repository
        )
        self.console = Console(force_terminal=True)
        self.input_view = InputView(self.console)

    def display_menu(self):
        """
        Display the tournament menu and route user choices to corresponding actions.
        Loop until user chooses to return to the main menu.
        """
        while True:
            self.console.print(Panel.fit("[bold magenta]Tournoi d'échecs - "
                                         "Bienvenue dans le gestionnaire de "
                                         "tournois[/bold magenta]"))

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
        """Display a table listing all tournaments."""
        tournaments = self.tournament_controller.list_tournaments()
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
        Prompt for new tournament details and create the tournament via the controller.
        """
        self.console.print("\n[bold blue]Entrez les informations du tournoi :[/bold blue]")

        name = self.input_view.input_name(name_type="Nom", add_on="du tournoi")
        location = self.input_view.input_name(name_type="Lieu")
        start_date = self.input_view.input_start_date()
        end_date = self.input_view.input_end_date(start_date=start_date)
        number_of_rounds = self.input_view.input_number_of_rounds()
        description = input("Description (Facultatif): ")

        tournament = self.tournament_controller.create_tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            description=description
        )
        self.console.print(f"[bold green]Le tournoi '{tournament.name}' a été créé avec succès.[/bold green]")

    def add_player_to_tournament_flow(self):
        """
        Add a player (existing or new) to a selected tournament.
        """
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()

        self.console.print("\n[bold blue]Entrez l'ID du tournoi:[/bold blue]")
        tournament_id = self.input_view.input_tournament_id()
        tournament = self.tournament_controller.get_by_id(tournament_id)

        if not tournament:
            self.console.print("[bold red]Tournoi introuvable. Veuillez d'abord créer le tournoi.[/bold red]")
            return

        if tournament.status == "Terminé":
            self.console.print("[bold yellow]Ce tournoi est terminé. Impossible d'y ajouter un joueur.[/bold yellow]")
            return

        self.console.print(f"Statut actuel : [green]{tournament.status}[/green]")

        while True:
            self.console.print("\n[bold blue]Entrez l'identifiant du joueur à ajouter au tournoi:")

            player_id = self.input_view.input_national_chess_id()
            player = self.tournament_controller.player_repository.get_by_id(player_id)

            if player is None:
                self.console.print("[bold blue]Joueur non trouvé. "
                                   "Création d'un nouveau joueur :[/bold blue]")
                last_name = self.input_view.input_name(name_type="Nom", add_on="de famille")
                first_name = self.input_view.input_name(name_type="Prénom")
                birth_date = self.input_view.input_date(date_type="Date de naissance")

                self.player_controller.create_player(
                    last_name=last_name,
                    first_name=first_name,
                    birth_date=birth_date,
                    national_chess_id=player_id
                )
                player = self.tournament_controller.player_repository.get_by_id(player_id)

            self.console.print(f"\nConfirmez-vous l'ajout du joueur [cyan]{player}[/cyan] au tournoi ?")
            confirmation = input("O/n").strip().lower()
            if confirmation in ["", "o", "oui"]:
                tournament = self.tournament_controller.tournament_repository.get_by_id(
                    tournament_id)
                players = tournament.players
                if player in players:
                    self.console.print("[yellow]Ce joueur est déjà inscrit à  ce tournoi.[/yellow]")
                else:
                    players.append(player)

                    scores = tournament.scores.copy()
                    if player.national_chess_id not in scores:
                        scores[player.national_chess_id] = 0.0

                        self.tournament_controller.update_tournament(
                            tournament_id,
                            players=players,
                            scores=scores
                        )

                self.console.print(f"[green]Joueur {player} ajouté avec succès.[/green]")

            self.console.print("[bold yellow]Voulez-vous ajouter un autre joueur à ce tournoi? (O/n): [/bold yellow] ")
            answer = input().strip().lower()
            if answer not in ["", "o", "oui"]:
                break

    def start_tournament_flow(self):
        """Start a selected tournament and generate the first round."""
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()

        self.console.print("\n[bold blue]Entrez l'ID du tournoi:[/bold blue]")
        tournament_id = self.input_view.input_tournament_id()
        tournament = self.tournament_controller.get_by_id(tournament_id)

        if not tournament:
            self.console.print("[bold red]Tournoi introuvable.[/bold red]")
            return

        if tournament.status != "Non démarré":
            self.console.print("\n[bold yellow]Ce tournoi est déjà commencé ou terminé[/bold yellow]")
            return

        if len(tournament.players) == 0:
            self.console.print("\n[bold yellow]Veuillez ajouter des joueurs au tournoi.[/bold yellow]")
            return
        elif len(tournament.players) % 2 != 0:
            self.console.print("\n[bold yellow]Le nombre de jours est impair. "
                               "Veuillez ajouter un joueur au tournoi.[/bold yellow]")
            return

        pairs = create_pairs_for_next_round(
            tournament=tournament,
            player_repository=self.tournament_controller.player_repository
        )

        matches = [Match(p1, p2) for p1, p2 in pairs]

        first_round = self.round_controller.create_round(
            tournament_id=tournament_id,
            matches=matches
        )

        rounds = tournament.rounds
        rounds.append(first_round)
        self.tournament_controller.update_tournament(
            tournament_id=tournament_id,
            rounds=rounds,
            status="En cours"
        )
        self.console.print(f"\n[bold green]Démarrage du tournoi {tournament.name}...[/bold green]")
        self.console.print(f"{first_round.name}\n")
        for match in first_round.matches:
            player1 = match.data[0][0]
            player2 = match.data[1][0]
            self.console.print(f"• {player1.first_name} {player1.last_name} contre "
                               f"{player2.first_name} {player2.last_name}")

    def input_results_flow(self):
        """Prompt results for matches in the current round of a tournament."""
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()

        self.console.print("\n[bold blue]Entrez l'ID du tournoi:[/bold blue]")
        tournament_to_be_played_id = self.input_view.input_tournament_id()
        tournament = self.tournament_controller.get_by_id(tournament_to_be_played_id)

        if tournament.status != "En cours":
            self.console.print("Ce tournoi est non démarré ou déjà terminé.")
            return

        current_round_index = tournament.current_round_number - 1
        if current_round_index >= len(tournament.rounds):
            return

        current_round = tournament.rounds[current_round_index]
        self.console.print(f"\n[bold]Saisie des résultats pour le round {current_round.name}[/bold]")

        for i, raw_match in enumerate(current_round.matches, 1):
            match = match_with_loaded_players(
                match=raw_match,
                player_repository=self.tournament_controller.player_repository
            )
            self.console.print(f"\nMatch {i} : {match.data[0][0]} contre {match.data[1][0]}")

            while True:
                self.console.print(f"1 → Le gagnant est {match.data[0][0]}")
                self.console.print(f"2 → Le gagnant est {match.data[1][0]}")
                self.console.print("3 → Match nul")
                self.console.print("4 → Choix aléatoire")

                choice = input("Votre choix : ")

                if choice == "4":
                    choice = str(randint(1, 3))

                if choice == "1":
                    match.set_scores(1.0, 0.0)
                    self.console.print(match)
                    break
                elif choice == "2":
                    match.set_scores(0.0, 1.0)
                    self.console.print(match)
                    break
                elif choice == "3":
                    match.set_scores(0.5, 0.5)
                    self.console.print(match)
                    break
                else:
                    self.console.print("[bold red]Choix invalide. "
                                       "Veuillez réessayer.[/bold red]")

            current_round.matches[i - 1] = match

            player1_id = match.data[0][0].national_chess_id
            player2_id = match.data[1][0].national_chess_id
            score1, score2 = match.get_scores()

            tournament.scores[player1_id] += score1
            tournament.scores[player2_id] += score2

        current_round.end()
        self.console.print(f"\n[bold green] Le {current_round.name} "
                           f"est maintenant terminé.[bold green]")

        if tournament.current_round_number >= tournament.number_of_rounds:
            self.tournament_controller.update_tournament(
                tournament_id=tournament_to_be_played_id,
                scores=tournament.scores,
                rounds=tournament.rounds,
                status="Terminé"
            )
            self.console.print("\n[bold green]Le tournoi est terminé![/bold green]")

        else:
            tournament.current_round_number += 1

            pairs = create_pairs_for_next_round(
                tournament=tournament,
                player_repository=self.tournament_controller.player_repository
            )

            new_matches = [Match(p1, p2) for p1, p2 in pairs]
            new_round = self.round_controller.create_round(
                tournament_id=tournament_to_be_played_id,
                matches=new_matches
            )
            tournament.rounds.append(new_round)

            self.tournament_controller.update_tournament(
                tournament_id=tournament_to_be_played_id,
                current_round_number=tournament.current_round_number,
                rounds=tournament.rounds,
                scores=tournament.scores,
            )

            self.console.print("\n[bold green]Nouveau round généré :[/bold green]")
            for match in new_round.matches:
                self.console.print(f"{match.data[0][0]} contre {match.data[1][0]}")

    def show_tournament_details_flow(self):

        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()

        self.console.print("\n[bold blue]Entrez l'ID du tournoi:[/bold blue]")
        tournament_id = self.input_view.input_tournament_id()
        tournament = self.tournament_controller.get_by_id(tournament_id)

        if not tournament:
            self.console.print("[bold red]Tournoi introuvable. Veuillez d'abord créer le tournoi.[/bold red]")
            return

        self.console.print(f"\n[cyan]{tournament.name} à {tournament.location} - "
                           f"{tournament.status}\n")

        self.console.print("\n[bold]Joueurs du tournoi:[/bold]")
        for player_id in tournament.players:
            player = self.tournament_controller.player_repository.get_by_id(player_id)
            total_score = tournament.scores.get(player_id, 0)
            self.console.print(f"- {str(player)} : {total_score} points")

        self.console.print("\n[bold]Rounds du tournoi:[/bold]")

        for chess_round in tournament.rounds:
            self.console.print(f"\n[underline]{chess_round.name}[/underline]")

            if not chess_round.matches:
                self.console.print("Aucun match pour ce round.")
                continue

            for match in chess_round.matches:
                match_data = match.to_dict()
                player1_id = match_data["player1_id"]
                player2_id = match_data["player2_id"]
                player1_score = match_data["player1_score"]
                player2_score = match_data["player2_score"]

                player1 = self.tournament_controller.player_repository.get_by_id(player1_id)
                player2 = self.tournament_controller.player_repository.get_by_id(player2_id)

                self.console.print(
                    f"{str(player1)} ({player1_score}) vs {str(player2)} ({player2_score})"
                )
