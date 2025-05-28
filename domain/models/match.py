"""Define the chess matches."""

from domain.models.player import Player


class Match:
    def __init__(
            self,
            player1: Player,
            player2: Player,
            player1_score: float = 0.0,
            player2_score: float = 0.0
    ):
        self.match = [player1, player1_score], [player2, player2_score]
