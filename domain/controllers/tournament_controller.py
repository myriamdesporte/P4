"""Handle tournament management operations."""

from typing import Optional, List, Dict

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
        """Initialize the controller with tournament and player repositories."""
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
        """
        Create and save a new tournament.

        Args:
            name (str): Tournament name.
            location (str): Tournament location.
            start_date (str): Start date, format 'DD-MM-YYYY'.
            end_date (str): End date, format 'DD-MM-YYYY'.
            number_of_rounds (int): Total rounds (default 4).
            description (str): Optional description.

        Returns:
            Tournament: The created tournament instance.
        """
        tournaments = self.tournament_repository.load_tournaments()

        new_id_number = len(tournaments) + 1
        new_id = f"T{new_id_number:03d}"

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

    def list_tournaments(self) -> List[Tournament]:
        """Return all tournaments from the repository with players loaded."""
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
                          name: Optional[str] = None,
                          location: Optional[str] = None,
                          start_date: Optional[str] = None,
                          end_date: Optional[str] = None,
                          number_of_rounds: Optional[int] = None,
                          current_round_number: Optional[int] = None,
                          rounds: Optional[List[Round]] = None,
                          players: Optional[List[Player]] = None,
                          scores: Optional[Dict[str, float]] = None,
                          description: Optional[str] = None,
                          status: Optional[str] = None,
                          ) -> bool:
        """Update a tournament identified by its ID."""
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
        """Return a tournament by its ID, or None if not found."""
        return self.tournament_repository.get_by_id(tournament_id)

    def get_tournament_by_id_with_loaded_players(
            self,
            tournament_id: str
    ) -> Optional[Tournament]:
        """Return a tournament with players loaded by its ID, or None if not found."""
        tournament = self.tournament_repository.get_by_id(tournament_id)
        if tournament is None:
            return None

        return tournament_with_loaded_players(
            tournament=tournament,
            player_repository=self.player_repository
        )
