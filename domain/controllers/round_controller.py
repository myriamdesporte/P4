"""Define the round controller"""
from typing import List

from domain.models.match import Match
from domain.models.round import Round
from domain.ports.tournament_repository import ITournamentRepository


class RoundController:
    def __init__(self,
                 tournament_repository: ITournamentRepository):
        """
        Initialize the controller by loading existing rounds and
        tournaments from storage.
        """
        self.tournament_repository = tournament_repository

    def create_round(
            self,
            tournament_id: str,
            matches: List[Match] | None = None,
    ) -> Round:
        tournament = self.tournament_repository.get_by_id(tournament_id)

        round_number = len(tournament.rounds)+1
        round_name = f"Round{round_number}"
        round_id = f"{tournament_id}{round_name}"

        r = Round(
            name=round_name,
            matches=matches,
            round_id=round_id
        )
        r.start()
        return r
