"""Implementation of IPlayerRepository using JSON storage."""

import json
import os
from typing import List, Optional
from domain.models.player import Player
from domain.ports.player_repository import IPlayerRepository


class JSONPlayerRepository(IPlayerRepository):
    PLAYERS_DATA_FILE = "data/players/players.json"

    def load_players(self) -> List[Player]:
        """
        Load all players from the JSON file.

        Returns:
            List[Player]: List of all saved players.
        """
        if not os.path.exists(self.PLAYERS_DATA_FILE):
            return []
        with open(self.PLAYERS_DATA_FILE, "r", encoding="utf-8") as file:
            players_data = json.load(file)
            return [
                Player.from_dict(player_data) for player_data in players_data
            ]

    def save_players(self, players: List[Player]) -> None:
        """
        Save all players to the JSON file.

        Args:
            players (List[Player]): List of Player instances to save.
        """
        os.makedirs(os.path.dirname(self.PLAYERS_DATA_FILE), exist_ok=True)
        json_data = json.dumps(
            [player.to_dict() for player in players], indent=2
        )
        with open(self.PLAYERS_DATA_FILE, "w", encoding="utf-8") as file:
            file.write(json_data)

    def update_player_by_id(
            self,
            national_chess_id: str,
            last_name: str = None,
            first_name: str = None,
            birth_date: str = None
    ) -> bool:
        """
        Update an existing player's information.

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
        Delete a player based on their national chess ID.

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
        players = self.load_players()
        for player in players:
            if player.national_chess_id == player_id:
                return player
        return None
