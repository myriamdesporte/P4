"""Define the player controller"""

from models.player import Player
from typing import List


class PlayerController:
    def __init__(self):
        """
        Initialize the controller by loading existing players from storage.
        """
        self.players: List[Player] = Player.load_players()

    def list_players(self) -> List[Player]:
        """
        Return all players loaded from the data store.

        Returns:
            List[Player]: The list of all player instances.
        """
        return self.players

    def create_player(
            self,
            last_name: str,
            first_name: str,
            birth_date: str,
            national_chess_id: str
    ) -> Player:
        """
        Create a new player, add to the list, and save all players

        Args:
            last_name (str): Player's last name.
            first_name (str): Player's first name.
            birth_date (str): Player's date of birth in 'YYYY-MM-DD' format.
            national_chess_id (str): Unique national chess ID (ex: 'AB12345').

        Returns:
            Player: The newly created Player.
        """
        player = Player(
            last_name,
            first_name,
            birth_date,
            national_chess_id
        )
        self.players.append(player)
        Player.save_players(self.players)
        return player
