"""Implementation of ITournamentRepository using JSON storage."""

import json
import os
from typing import List, Optional, Dict

from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament
from domain.ports.tournament_repository import ITournamentRepository


class JSONTournamentRepository(ITournamentRepository):
    TOURNAMENTS_DATA_FILE = "data/tournaments/tournaments.json"

    def load_tournaments(self) -> List[Tournament]:
        """Load all tournaments from the JSON file."""
        if not os.path.exists(self.TOURNAMENTS_DATA_FILE):
            return []

        with open(self.TOURNAMENTS_DATA_FILE, "r", encoding="utf-8") as file:
            tournaments_data = json.load(file)

            return [
                Tournament.from_dict(tournament_data) for tournament_data in tournaments_data
            ]

    def save_tournaments(self, tournaments: List[Tournament]) -> None:
        """Save all tournaments to the JSON file."""
        os.makedirs(os.path.dirname(self.TOURNAMENTS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [tournament.to_dict() for tournament in tournaments], indent=2, ensure_ascii=False

        )

        with open(self.TOURNAMENTS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)

    def update_tournament_by_id(
            self,
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
            status: Optional[str] = None
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
                if scores:
                    tournament.scores = scores
                if description:
                    tournament.description = description
                if status:
                    tournament.status = status

                self.save_tournaments(tournaments)
                return True
        return False

    def get_by_id(self, tournament_id: str) -> Optional[Tournament]:
        """Return a tournament by ID or None if not found.

        Args:
            tournament_id (str): The ID of the tournament to return.

        Returns:
            Optional[Tournament]: The Tournament instance if found, None otherwise.
        """
        tournaments = self.load_tournaments()
        for tournament in tournaments:
            if tournament.tournament_id == tournament_id:
                return tournament
        return None
