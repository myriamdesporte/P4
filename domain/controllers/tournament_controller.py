"""Define the tournament controller."""
from typing import Optional, List, Dict

from domain.models.match import Match
from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository
from domain.ports.tournament_repository import ITournamentRepository
from infra.utils.tournament_utils import tournament_with_loaded_players


class TournamentController:
    def __init__(
            self,
            tournament_repository: ITournamentRepository,
            player_repository: IPlayerRepository
    ):
        """
        Initialize the controller by setting the repository.
        """
        self.tournament_repository = tournament_repository
        self.player_repository = player_repository

    def create_tournament(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            number_of_rounds: int = 4,
            description: str = ""
    ) -> Tournament:
        # Charger tous les tournois
        tournaments = self.tournament_repository.load_tournaments()

        # Créé le nouvel id de tournoi
        new_id_number = len(tournaments) + 1
        new_id = f"T{new_id_number:03d}"

        # Créer le tournoi avec ce nouvel ID
        tournament = Tournament(
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            description=description,
            tournament_id=new_id,
        )
        tournaments.append(tournament)
        self.tournament_repository.save_tournaments(tournaments)
        return tournament

    def list_tournaments(self):
        """
        Retrieve all tournaments from the repository with loaded players.

        Returns:
            List[Tournament]: A list of all saved tournaments.
        """
        tournaments = self.tournament_repository.load_tournaments()
        return [
            tournament_with_loaded_players(
                tournament,
                self.player_repository
            )
            for tournament in tournaments
        ]

    def update_tournament(self,
                          tournament_id: str,
                          name: str = None,
                          location: str = None,
                          start_date: str = None,
                          end_date: str = None,
                          number_of_rounds: int = None,
                          current_round_number: int = None,
                          rounds: Optional[List[Round]] = None,
                          players: Optional[List[Player]] = None,
                          scores: Optional[Dict[str, float]] = None,
                          description: Optional[str] = None,
                          status: str = None,
                          ) -> bool:
        """Update an existing tournament's information."""
        return self.tournament_repository.update_tournament_by_id(
            tournament_id=tournament_id,
            name=name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            number_of_rounds=number_of_rounds,
            current_round_number=current_round_number,
            rounds=rounds,
            players=players,
            scores=scores,
            description=description,
            status=status
        )

    def get_by_id(self, tournament_id: str) -> Optional[Tournament]:
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is not None:
            return tournament
        return None

    def get_tournament_by_id_with_loaded_players(
            self,
            tournament_id: str
    ) -> Optional[Tournament]:
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is not None:
            return tournament_with_loaded_players(
                tournament,
                self.player_repository
            )
        return None
