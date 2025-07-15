"""Define the players."""

from __future__ import annotations


class Player:
    def __init__(
            self,
            last_name: str,
            first_name: str,
            birth_date: str,
            national_chess_id: str
    ):
        """
        Initialize a player with personal information.
        Args:
            last_name (str): Player's last name.
            first_name (str): Player's first name.
            birth_date (str): Player's date of birth in 'DD-MM-YYYY' format.
            national_chess_id (str): Unique national chess ID (ex: 'AB12345').
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __str__(self) -> str:
        """Return a string representation of the player."""
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        """Convert the player instance into a dictionary."""
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_chess_id": self.national_chess_id
        }

    @classmethod
    def from_dict(cls, player_data: dict) -> Player:
        """Create a Player instance from a dictionary."""
        return cls(
            last_name=player_data["last_name"],
            first_name=player_data["first_name"],
            birth_date=player_data["birth_date"],
            national_chess_id=player_data["national_chess_id"]
        )
