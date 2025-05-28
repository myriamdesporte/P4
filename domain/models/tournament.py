"""Define the tournaments."""

from typing import List, Optional
from domain.models.player import Player


class Tournament:
    def __init__(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            number_of_rounds: int = 4,
            description: Optional[str] = None
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round_number = 0
        self.rounds: List = []  # Liste de tours
        self.players: List[Player] = []  # Liste de joueurs
        self.description = description
