"""Implementation of ITournamentRepository using JSON storage."""

import json
import os
from typing import List, Optional

from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament
from domain.ports.tournament_repository import ITournamentRepository


class JSONTournamentRepository(ITournamentRepository):
    TOURNAMENTS_DATA_FILE = "data/tournaments/tournaments.json"

    def load_tournaments(self) -> List[Tournament]:
        """
        Load all tournaments from the JSON file.

        Returns:
            List[Tournament]: List of all saved tournaments.
        """
        if not os.path.exists(self.TOURNAMENTS_DATA_FILE):
            return []
        with open(self.TOURNAMENTS_DATA_FILE, "r", encoding="utf-8") as file:
            tournaments_data = json.load(file)
            return [
                Tournament.from_dict(tournament_data) for tournament_data in tournaments_data
            ]

    def save_tournaments(self, tournaments: List[Tournament]) -> None:
        """
        Save all tournaments to the JSON file.

        Args:
            tournaments (List[Tournament]): List of Tournament instances to save.
        """
        os.makedirs(os.path.dirname(self.TOURNAMENTS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [tournament.to_dict() for tournament in tournaments], indent=2, ensure_ascii=False

        )
        with open(self.TOURNAMENTS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)

    def update_tournament_by_id(
            self,
            tournament_id: str,
            name: str = None,
            location: str = None,
            start_date: str = None,
            end_date: str = None,
            number_of_rounds: int = 4,
            current_round_number: int = 1,
            rounds: Optional[List[Round]] = None,
            players: Optional[List[Player]] = None,
            description: Optional[str] = None,
            status: str = "Non démarré"
    ) -> bool:
        tournaments = self.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                if name:
                    tournament.name = name
                if location:
                    tournament.location = location
                if start_date:
                    tournament.start_date = start_date
                if end_date:
                    tournament.end_date = end_date
                if number_of_rounds:
                    tournament.number_of_rounds = number_of_rounds
                if current_round_number:
                    tournament.current_round_number = current_round_number
                if rounds:
                    tournament.rounds = rounds
                if players:
                    tournament.players = players
                if description:
                    tournament.description = description
                if status:
                    tournament.status = status
                self.save_tournaments(tournaments)
                return True
        return False

    def get_by_id(self, tournament_id: str) -> Optional[Tournament]:
        tournaments = self.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        return None
