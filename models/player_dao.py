"""Handle persistence for Player data."""

import os
import json
from typing import List
from models.player import Player


class PlayerDAO:
    PLAYERS_DATA_FILE = "data/players.json"

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
            return [
                Player.from_dict(player_data) for player_data in players_data
            ]

    @classmethod
    def save_players(cls, players: List[Player]) -> None:
        """
        Save all players to the JSON file.

        Args:
            players (List[Player]): List of Player instances to save.
        """
        os.makedirs(os.path.dirname(cls.PLAYERS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [player.to_dict() for player in players], indent=2
        )
        with open(cls.PLAYERS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)
