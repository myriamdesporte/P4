"""Implementation of IPlayerRepository using JSON storage."""

import json
import os
from typing import List, Optional

from domain.models.player import Player
from domain.ports.player_repository import IPlayerRepository


class JSONPlayerRepository(IPlayerRepository):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PLAYERS_DATA_FILE = os.path.normpath(os.path.join(
        BASE_DIR, "..", "..", "data", "players", "players.json"
    ))

    def load_players(self) -> List[Player]:
        """Load all players from the JSON file."""
        if not os.path.exists(self.PLAYERS_DATA_FILE):
            return []

        with open(self.PLAYERS_DATA_FILE, "r", encoding="utf-8") as file:
            players_data = json.load(file)
            players = [Player.from_dict(player_data) for player_data in players_data]

            players_sorted = sorted(players, key=lambda p: p.last_name.lower())

            return players_sorted

    def save_players(self, players: List[Player]) -> None:
        """Save all players to the JSON file."""
        os.makedirs(os.path.dirname(self.PLAYERS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [player.to_dict() for player in players], indent=2
        )

        with open(self.PLAYERS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)

    def update_player_by_id(
            self,
            national_chess_id: str,
            last_name: Optional[str] = None,
            first_name: Optional[str] = None,
            birth_date: Optional[str] = None
    ) -> bool:
        """
        Update a player identified by national_chess_id.

        Args:
            national_chess_id (str): ID of the player to update.
            last_name (str, optional): New last name.
            first_name (str, optional): New first name.
            birth_date (str, optional): New date of birth.

        Returns:
            bool: True if the player was found and updated, False otherwise.
        """
        players = self.load_players()
        for player in players:
            if player.national_chess_id == national_chess_id:
                if last_name:
                    player.last_name = last_name
                if first_name:
                    player.first_name = first_name
                if birth_date:
                    player.birth_date = birth_date

                self.save_players(players)
                return True
        return False

    def delete_player_by_id(self, national_chess_id: str) -> bool:
        """
        Delete a player identified by national_chess_id.

        Args:
            national_chess_id (str): ID of the player to delete.

        Returns:
            bool: True if the player was found and deleted, False otherwise.
        """
        players = self.load_players()
        for player in players:
            if player.national_chess_id == national_chess_id:
                players.remove(player)

                self.save_players(players)
                return True
        return False

    def get_by_id(self, player_id: str) -> Optional[Player]:
        """Return a player by ID or None if not found.

        Args:
            player_id (str): The ID of the player to return.

        Returns:
            Optional[Player]: The Player instance if found, None otherwise.
        """
        players = self.load_players()
        for player in players:
            if player.national_chess_id == player_id:
                return player
        return None
