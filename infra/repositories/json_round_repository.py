"""Implementation of IRoundRepository using JSON storage."""
import json
import os
from datetime import datetime
from typing import List, Optional
from domain.models.match import Match
from domain.models.round import Round
from domain.ports.round_repository import IRoundRepository


class JSONRoundRepository(IRoundRepository):
    ROUNDS_DATA_FILE = "data/rounds/rounds.json"

    def load_rounds(self) -> List[Round]:
        """
        Load all rounds from the JSON file.

        Returns:
            List[Round]: List of all saved rounds.
        """
        if not os.path.exists(self.ROUNDS_DATA_FILE):
            return []
        with open(self.ROUNDS_DATA_FILE, "r", encoding="utf-8") as file:
            rounds_data = json.load(file)
            return [
                Round.from_dict(round_data) for round_data in rounds_data
            ]

    def save_rounds(self, rounds: List[Round]) -> None:
        """
        Save all rounds to the JSON file.

        Args:
            rounds (List[Round]): List of Round instances to save.
        """
        os.makedirs(os.path.dirname(self.ROUNDS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [r.to_dict() for r in rounds], indent=2, ensure_ascii=False

        )
        with open(self.ROUNDS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)


    def update_round_by_id(self,
                           round_id: str,
                           name: str = None,
                           start_datetime: datetime = None,
                           end_datetime: datetime = None,
                           matches: Optional[List[Match]] = None
                           ) -> bool:
        rounds = self.load_rounds()
        for r in rounds:
            if r.round_id == round_id:
                if name:
                    r.name = name
                if start_datetime:
                    r.start_datetime = start_datetime
                if end_datetime:
                    r.end_datetime = end_datetime
                if matches:
                    r.matches = matches
                self.save_rounds(rounds)
                return True
        return False

    def get_by_id(self, round_id: str) -> Optional[Round]:
        """Return a round by ID or None if not found."""
        rounds = self.load_rounds()
        for r in rounds:
            if r.round_id == round_id:
                return r
        return None