"""Define the tournaments."""
from __future__ import annotations
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
            current_round_number: int = 0,
            rounds: Optional[List] = None, #TODO: fill with Round instances later
            players: Optional[List[Player]] = None,
            description: Optional[str] = None
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round_number = current_round_number
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.description = description

    def __str__(self) -> str:
        """
        Return a string representation of the tournament.
        """
        return (f"Tournoi: {self.name} à {self.location} "
                f"du {self.start_date} au {self.end_date} "
                f"({len(self.players)} joueurs, "
                f"tour {self.current_round_number}/{self.number_of_rounds})")

    def to_dict(self) -> dict:
        """
        Convert the tournament instance into a dictionary.
        Only stores player IDs (not objects).
        Returns:
            dict: Dictionary containing tournament data with players as ID strings
        """
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_rounds": self.number_of_rounds,
            "current_round_number": self.current_round_number,
            "rounds": self.rounds,
            "players": [player.national_chess_id for player in self.players],
            "description": self.description
        }

    @classmethod
    def from_dict(cls, tournament_data: dict) -> Tournament:
        """
        Create a Tournament instance from a dictionary.

        Args:
            tournament_data (dict): Dictionary containing tournament data.

        Returns:
            Tournament: A new Tournament instance with players as a list of IDs.
        """
        return cls(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            number_of_rounds=tournament_data.get("number_of_rounds", 4),
            description=tournament_data.get("description"),
            current_round_number=tournament_data.get("current_round_number", 0),
            rounds=tournament_data.get("rounds", []),
            players=tournament_data.get("players", [])
        )
