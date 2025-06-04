"""Implementation of ITournamentRepository using JSON storage."""

import json
import os
from typing import List

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
            [tournament.to_dict() for tournament in tournaments], indent=2
        )
        with open(self.TOURNAMENTS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)
