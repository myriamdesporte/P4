"""Port interface for player repository."""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.player import Player


class IPlayerRepository(ABC):
    @abstractmethod
    def load_players(self) -> List[Player]:
        pass

    @abstractmethod
    def save_players(self, players: List[Player]) -> None:
        pass

    @abstractmethod
    def update_player_by_id(self,
                            national_chess_id: str,
                            last_name: str = None,
                            first_name: str = None,
                            birth_date: str = None) -> bool:
        pass

    @abstractmethod
    def delete_player_by_id(self, national_chess_id: str) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, player_id: str) -> Optional[Player]:
        """Return a player by ID or None if not found."""
        pass
