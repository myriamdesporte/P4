"""Define the tournaments."""
from __future__ import annotations
from typing import List, Optional
from domain.models.player import Player
from domain.models.round import Round


class Tournament:
    def __init__(
            self,
            name: str,
            location: str,
            start_date: str,
            end_date: str,
            number_of_rounds: int = 4,
            current_round_number: int = 1,
            status: str = "Non démarré",
            rounds: Optional[List[Round]] = None,
            players: Optional[List[Player]] = None,
            description: Optional[str] = None,
            tournament_id: Optional[str] = None,

    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.number_of_rounds = number_of_rounds
        self.current_round_number = current_round_number
        self.status = status
        self.rounds = rounds if rounds is not None else []
        self.players = players if players is not None else []
        self.description = description
        self.tournament_id = tournament_id

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
            "status": self.status,
            "rounds": [round_.to_dict() for round_ in self.rounds],
            "players": [p.national_chess_id if isinstance(p, Player) else p for p in self.players],
            "description": self.description,
            "tournament_id": self.tournament_id
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
            current_round_number=tournament_data.get("current_round_number", 1),
            status=tournament_data.get("status", "Non démarré"),
            rounds=[Round.from_dict(round_) for round_ in tournament_data.get("rounds", [])],
            players=tournament_data.get("players", []),
            description=tournament_data.get("description"),
            tournament_id=tournament_data.get("tournament_id")
        )
