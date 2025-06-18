"""Define the round controller"""
from typing import List

from domain.models.match import Match
from domain.models.round import Round
from domain.ports.round_repository import IRoundRepository
from domain.ports.tournament_repository import ITournamentRepository


class RoundController:
    def __init__(self,
                 round_repository: IRoundRepository,
                 tournament_repository: ITournamentRepository):
        """
        Initialize the controller by loading existing rounds and
        tournaments from storage.
        """
        self.round_repository = round_repository
        self.tournament_repository = tournament_repository

    def create_round_in_tournament(
            self,
            tournament_id: str,
            matches: List[Match] | None = None,
    ) -> Round:
        # Chargement de tous les rounds
        rounds = self.round_repository.load_rounds()

        # On récupère l'objet tournoi correspondant au tournament_id
        tournament = self.tournament_repository.get_by_id(tournament_id)

        # On crée le nouvel id de round et le nom de round
        round_number = len(tournament.rounds)
        round_name = f"Round{round_number}"
        round_id = f"{tournament_id}{round_name}"

        # On crée le round et on l'ajoute au repo
        r = Round(
            name=round_name,
            matches=matches,
            round_id=round_id
        )
        r.start()
        rounds.append(r)
        self.round_repository.save_rounds(rounds)
        return r
