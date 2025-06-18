"""Port interface for round repository."""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from domain.models.match import Match
from domain.models.round import Round


class IRoundRepository(ABC):
    @abstractmethod
    def load_rounds(self) -> List[Round]:
        pass

    @abstractmethod
    def save_rounds(self, players: List[Round]) -> None:
        pass

    @abstractmethod
    def update_round_by_id(self,
                           round_id: str,
                           name: str = None,
                           start_datetime: datetime = None,
                           end_datetime: datetime = None,
                           matches: Optional[List[Match]] = None
                           ) -> bool:
        pass

    @abstractmethod
    def get_by_id(self, round_id: str) -> Optional[Round]:
        """Return a round by ID or None if not found."""
        pass