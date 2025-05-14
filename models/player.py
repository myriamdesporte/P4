"""Define the players."""
from __future__ import annotations
import json
import os
from typing import List


class Player:

    PLAYERS_DATA_FILE = "data/players.json"

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
            birth_date (str): Player's date of birth in 'YYYY-MM-DD' format.
            national_chess_id (str): Unique national chess ID (ex: 'AB12345').
        """
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_chess_id = national_chess_id

    def __str__(self) -> str:
        return (f"{self.first_name} {self.last_name} "
                f"({self.national_chess_id}) - "
                f"Né(e) le {self.birth_date}")

    def to_dict(self):
        """
        Convert the player instance into a dictionary.

        Returns:
            dict: Dictionary representation of the player.
        """
        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_chess_id": self.national_chess_id
        }

    @classmethod
    def from_dict(cls, player_data: dict) -> "Player":
        """
        Create a Player instance from a dictionary.

        Args:
            player_data (dict): Dictionary containing player data.

        Returns:
            Player: A new Player instance.
        """
        return cls(
            last_name=player_data["last_name"],
            first_name=player_data["first_name"],
            birth_date=player_data["birth_date"],
            national_chess_id=player_data["national_chess_id"]
        )

    @classmethod
    def load_players(cls) -> List[Player]:
        """
        Load all players from the JSON file.

        Returns:
            List[Player]: List of all saved players.
        """
        if not os.path.exists(cls.PLAYERS_DATA_FILE):
            return []
        with open(cls.PLAYERS_DATA_FILE, "r", encoding="utf-8") as file:
            players_data = json.load(file)
            return [cls.from_dict(player_data) for player_data in players_data]

    @classmethod
    def save_players(cls, players: List[Player]) -> None:
        """
        Save all players to the JSON file.

        Args:
            players (List[Player]): List of Player instances to save.
        """
        os.makedirs(os.path.dirname(cls.PLAYERS_DATA_FILE), exist_ok=True)

        with open(cls.PLAYERS_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump([player.to_dict() for player in players], file, indent=2)
