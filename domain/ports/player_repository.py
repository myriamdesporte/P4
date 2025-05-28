"""Port interface for player repository."""

from abc import ABC, abstractmethod
from typing import List
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
