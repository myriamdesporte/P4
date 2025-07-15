"""Handle round management operations."""

from typing import List, Optional

from domain.models.match import Match
from domain.models.round import Round
from domain.ports.tournament_repository import ITournamentRepository


class RoundController:
    def __init__(self,
                 tournament_repository: ITournamentRepository):
        """Initialize the controller with a tournament repository."""
        self.tournament_repository = tournament_repository

    def create_round(
            self,
            tournament_id: str,
            matches: Optional[List[Match]] = None,
    ) -> Round:
        """
        Create and start a new round for the given tournament.

        Args:
            tournament_id (str): ID of the tournament.
            matches (List[Match], optional): List of matches to initialize the round.

        Returns:
            Round: The newly created and started round.
        """
        tournament = self.tournament_repository.get_by_id(tournament_id)

        round_number = len(tournament.rounds) + 1
        round_name = f"Round{round_number}"
        round_id = f"{tournament_id}{round_name}"

        new_round = Round(
            name=round_name,
            matches=matches,
            round_id=round_id
        )
        new_round.start()
        return new_round
