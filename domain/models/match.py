"""Define the chess matches."""

from __future__ import annotations

from typing import Tuple

from domain.models.player import Player


class Match:
    def __init__(
            self,
            player1: Player | str,  # Player instance or player ID string
            player2: Player | str,
            player1_score: float = 0.0,
            player2_score: float = 0.0
    ):
        """
        Initialize a Match with player references and their scores.

        Note:
            The match is stored as a tuple of two lists:
            one per player, each containing [player_ref, score].
        """
        self.data = ([player1, player1_score], [player2, player2_score])

    def get_players(self) -> Tuple[Player, Player]:
        """Return the two players of a match."""
        return self.data[0][0], self.data[1][0]

    def get_scores(self) -> Tuple[float, float]:
        """Return the score of both players."""
        return self.data[0][1], self.data[1][1]

    def set_scores(self, player1_score: float, player2_score: float):
        """Update the scores for both players."""
        self.data[0][1] = player1_score
        self.data[1][1] = player2_score

    def to_dict(self) -> dict:
        """Convert the match instance into a dictionary format using player IDs."""
        return {
            "player1_id": self.data[0][0].national_chess_id
            if isinstance(self.data[0][0], Player) else self.data[0][0],
            "player2_id": self.data[1][0].national_chess_id
            if isinstance(self.data[1][0], Player) else self.data[1][0],
            "player1_score": self.data[0][1],
            "player2_score": self.data[1][1],
        }

    @classmethod
    def from_dict(cls, match_data: dict) -> Match:
        """
        Create a Match instance from a dictionary containing player IDs and scores.

        Note:
            player1 and player2 are expected to be strings (IDs) here.
        """
        return cls(
            player1=match_data["player1_id"],
            player2=match_data["player2_id"],
            player1_score=match_data.get("player1_score", 0.0),
            player2_score=match_data.get("player2_score", 0.0),
        )
