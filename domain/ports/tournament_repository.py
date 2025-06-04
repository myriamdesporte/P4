"""Port interface for tournament repository."""
from abc import ABC, abstractmethod
from typing import List
from domain.models.tournament import Tournament


class ITournamentRepository(ABC):
    @abstractmethod
    def load_tournaments(self) -> List[Tournament]:
        pass

    @abstractmethod
    def save_tournaments(self, tournaments: List[Tournament]) -> None:
        pass
