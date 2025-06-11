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
        self.data = ([player1, player1_score], [player2, player2_score])

    def get_players(self):
        """Return the two players of a match."""
        return self.data[0][0], self.data[1][0]

    def get_scores(self):
        """Return the score of each player of a match."""
        return self.data[0][1], self.data[1][1]

    def set_scores(self, player1_score: float, player2_score: float):
        self.data[0][1] = player1_score
        self.data[1][1] = player2_score
