from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from domain.controllers.player_controller import PlayerController
from domain.controllers.round_controller import RoundController
from domain.controllers.tournament_controller import TournamentController
from domain.models.match import Match
from infra.repositories.json_player_repository import JSONPlayerRepository
from infra.repositories.json_tournament_repository import JSONTournamentRepository
from infra.utils.match_utils import match_with_loaded_players, input_result
from infra.utils.tournament_utils import create_pairs_for_next_round
from test import repository


class TournamentView:
    def __init__(self):
        """
        Initialize the view with a TournamentController instance and Rich Console
        """
        self.tournament_controller = TournamentController(
            tournament_repository=JSONTournamentRepository(),
            player_repository=JSONPlayerRepository()
        )
        self.player_controller = PlayerController(
            repository=JSONPlayerRepository()
        )
        self.round_controller = RoundController(
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
        Prompt the user to enter information for a new tournament.
        """
        self.console.print("\n[bold blue]Entrez les informations du tournoi :[/bold blue]")
        name = input("Nom du tournoi : ").strip()
        location = input("Lieu : ").strip()
        start_date = input("Date de début (format AAAA-MM-JJ) : ").strip()
        end_date = input("Date de fin (format AAAA-MM-JJ) : ").strip()
        nb= input("Nombre de rounds (4 par défaut) : ")
        number_of_rounds = int(nb) if nb != "" else 4
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
        Add player to a tournament.
        If the player is not registered in the list of players, he is added
        to the player repository and then added to the tournament.
        """
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()

        tournament_id = input("Entrez l'ID du tournoi:")
        tournament = self.tournament_controller.get_by_id(tournament_id)

        if not tournament:
            self.console.print("[bold red]Tournoi introuvable. Veuillez d'abord créer le tournoi.[/bold red]")
            return

        if tournament.status == "Terminé":
            self.console.print("[bold yellow]Ce tournoi est terminé. Impossible d'y ajouter un joueur.[/bold yellow]")
            return

        self.console.print(f"Statut actuel : [green]{tournament.status}[/green]")

        while True:
            player_id = input("Entrez l'identifiant du joueur à ajouter au tournoi:")
            player = self.tournament_controller.player_repository.get_by_id(player_id)

            if player is None:
                self.console.print("[bold blue]Joueur non trouvé. "
                                   "Création d'un nouveau joueur :[/bold blue]")
                last_name = input("Nom de famille: ").strip()
                first_name = input("Prénom: ").strip()
                birth_date = input("Date de naissance (format AAAA-MM-JJ): ").strip()

                self.player_controller.create_player(
                    last_name=last_name,
                    first_name=first_name,
                    birth_date=birth_date,
                    national_chess_id=player_id
                )
                player= self.tournament_controller.player_repository.get_by_id(player_id)

            self.console.print(f"\nConfirmez-vous l'ajout du joueur [cyan]{player}[/cyan] au tournoi ?")
            confirmation = input("O/n").strip().lower()
            if confirmation in ["", "o", "oui"]:
                tournament = self.tournament_controller.tournament_repository.get_by_id(
                    tournament_id)
                players = tournament.players
                if player in players:
                    self.console.print("[yellow]Ce joueur est déjà inscrit à  ce tournoi.[/yellow")
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

            add_another = input("Voulez-vous ajouter un autre joueur à ce tournoi? (O/n): ").strip().lower()
            if add_another not in ["", "o", "oui"]:
                break

    def start_tournament_flow(self):
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()
        tournament_id = input("Entrez un ID de tournoi:")
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
        elif len(tournament.players)%2 != 0:
            self.console.print("\n[bold yellow]Le nombre de jours est impair. "
                               "Veuillez ajouter un joueur au tournoi.[/bold yellow]")
            return

        pairs = create_pairs_for_next_round(
            tournament=tournament,
            player_repository=self.tournament_controller.player_repository
        )

        matches = [Match(p1,p2) for p1, p2 in pairs]

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
        self.console.print("\n[bold green]Démarrage du tournoi {tournament}...[/bold green]")
        self.console.print(f"{first_round.name}\n")
        for match in first_round.matches:
            player1 = match.data[0][0]
            player2 = match.data[1][0]
            self.console.print(f"• {player1.first_name} {player1.last_name} contre "
                               f"{player2.first_name} {player2.last_name}")

    def input_results_flow(self):
        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()
        tournament_to_be_played_id = input("Entrez un ID de tournoi:")
        tournament = self.tournament_controller.get_by_id(tournament_to_be_played_id)

        if tournament.status != "En cours":
            print(f"Ce tournoi est non démarré ou déjà terminé.")
            return

        current_round_index = tournament.current_round_number - 1
        if current_round_index >= len(tournament.rounds):
            return

        current_round = tournament.rounds[current_round_index]
        self.console.print(f"\n[bold]Saisie des résultats pour le round {current_round.name}[/bold]")

        for i, raw_match in enumerate(current_round.matches, 1):
            match = match_with_loaded_players(
                match= raw_match,
                player_repository=self.tournament_controller.player_repository
            )
            self.console.print(f"\nMatch {i} : {match.data[0][0]} contre {match.data[1][0]}")

            input_result(match=match)

            current_round.matches[i - 1] = match

            player1_id = match.data[0][0].national_chess_id
            player2_id = match.data[1][0].national_chess_id
            score1, score2 = match.get_scores()

            tournament.scores[player1_id] += score1
            tournament.scores[player2_id] += score2

        current_round.end()


        if tournament.current_round_number >= tournament.number_of_rounds:
            self.tournament_controller.update_tournament(
                tournament_id=tournament_to_be_played_id,
                scores=tournament.scores,
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
            rounds = tournament.rounds
            rounds.append(new_round)

            self.tournament_controller.update_tournament(
                tournament_id=tournament_to_be_played_id,
                current_round_number=tournament.current_round_number,
                rounds=rounds,
                scores=tournament.scores,
            )

            self.console.print("\n[bold green]Nouveau round généré :[/bold green]")
            for match in new_round.matches:
                print(f"{match.data[0][0]} contre {match.data[1][0]}")

    def show_tournament_details_flow(self):

        self.console.print("\n[bold blue]Voici l'ensemble des tournois:[/bold blue]")
        self.list_tournaments_flow()
        tournament_id = input("Entrez un ID de tournoi: ")
        tournament = self.tournament_controller.get_by_id(tournament_id)

        self.console.print(f"\n[cyan]{tournament.name} à {tournament.location} - "
                           f"{tournament.status}\n")

        self.console.print(f"\n[bold]Joueurs du tournoi:[/bold]")
        for player_id in tournament.players:
            player = self.tournament_controller.player_repository.get_by_id(player_id)
            total_score = tournament.scores.get(player_id, 0)
            self.console.print(f"- {str(player)} : {total_score} points")

        self.console.print(f"\n[bold]Rounds du tournoi:[/bold]")

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
