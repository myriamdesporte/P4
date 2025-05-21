"""Define the player controller"""

from typing import List
from models.player import Player
from models.player_dao import PlayerDAO


class PlayerController:
    def __init__(self):
        """
        Initialize the controller by loading existing players from storage.
        """
        self.players: List[Player] = PlayerDAO.load_players()

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
        PlayerDAO.save_players(self.players)
        return player

    def update_player(
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
        for player in self.players:
            if player.national_chess_id == national_chess_id:
                if last_name:
                    player.last_name = last_name
                if first_name:
                    player.first_name = first_name
                if birth_date:
                    player.birth_date = birth_date
                PlayerDAO.save_players(self.players)
                return True
        return False

    def delete_player(self, national_chess_id: str) -> bool:
        """
        Delete a player based on their national chess ID.

        Args:
            national_chess_id (str): ID of the player to delete.

        Returns:
            bool: True if the player was found and deleted, False otherwise.
        """
        for player in self.players:
            if player.national_chess_id == national_chess_id:
                self.players.remove(player)
                PlayerDAO.save_players(self.players)
                return True
        return False
