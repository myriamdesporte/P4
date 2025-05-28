"""Define the player controller"""

from domain.models.player import Player
from domain.ports.player_repository import IPlayerRepository


class PlayerController:
    def __init__(self, repository: IPlayerRepository):
        """
        Initialize the controller by loading existing players from storage.
        """
        self.repository = repository

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
        players = self.repository.load_players()
        players.append(player)
        self.repository.save_players(players)
        return player

    def list_players(self):
        """
        Retrieve all players from the repository.

        Returns:
            List[Player]: A list of all registered players.
        """
        return self.repository.load_players()

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
        return self.repository.update_player_by_id(
            national_chess_id,
            last_name,
            first_name,
            birth_date
        )

    def delete_player(self, national_chess_id: str) -> bool:
        """
        Delete a player based on their national chess ID.

        Args:
            national_chess_id (str): ID of the player to delete.

        Returns:
            bool: True if the player was found and deleted, False otherwise.
        """
        return self.repository.delete_player_by_id(national_chess_id)
