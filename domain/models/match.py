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

    def __str__(self):
        return f"{self.data[0][0]}({self.data[0][1]}) - {self.data[1][0]}({self.data[1][1]})"

    def get_players(self):
        """Return the two players of a match."""
        return self.data[0][0], self.data[1][0]

    def get_scores(self):
        """Return the score of each player of a match."""
        return self.data[0][1], self.data[1][1]

    def set_scores(self, player1_score: float, player2_score: float):
        self.data[0][1] = player1_score
        self.data[1][1] = player2_score

    def to_dict(self) -> dict:
        """Convert a Match instance to dictionary."""
        return{
            "player1_id": self.data[0][0].national_chess_id
            if isinstance(self.data[0][0], Player) else self.data[0][0],
                "player2_id": self.data[1][0].national_chess_id
            if isinstance(self.data[1][0], Player) else self.data[1][0],
            "player1_score": self.data[0][1],
            "player2_score": self.data[1][1],
        }

    @classmethod
    def from_dict(cls, match_data: dict):
        """Create a Match instance from a dictionary with player ID only."""
        return cls(
            player1=match_data["player1_id"],
            player2=match_data["player2_id"],
            player1_score=match_data.get("player1_score", 0.0),
            player2_score=match_data.get("player2_score", 0.0),
        )

