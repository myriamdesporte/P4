"""Port interface for player repository."""

from abc import ABC, abstractmethod
from typing import List, Optional

from domain.models.player import Player


class IPlayerRepository(ABC):
    @abstractmethod
    def load_players(self) -> List[Player]:
        """Load all players from the data source."""
        pass

    @abstractmethod
    def save_players(self, players: List[Player]) -> None:
        """Save the full list of players to the data source."""
        pass

    @abstractmethod
    def update_player_by_id(
            self,
            national_chess_id: str,
            last_name: Optional[str] = None,
            first_name: Optional[str] = None,
            birth_date: Optional[str] = None
    ) -> bool:
        """Update a player identified by national_chess_id."""
        pass

    @abstractmethod
    def delete_player_by_id(self, national_chess_id: str) -> bool:
        """Delete a player identified by national_chess_id."""
        pass

    @abstractmethod
    def get_by_id(self, player_id: str) -> Optional[Player]:
        """Return a player by ID or None if not found."""
        pass
