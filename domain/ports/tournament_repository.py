"""Port interface for tournament repository."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament


class ITournamentRepository(ABC):
    @abstractmethod
    def load_tournaments(self) -> List[Tournament]:
        pass

    @abstractmethod
    def save_tournaments(self, tournaments: List[Tournament]) -> None:
        pass

    @abstractmethod
    def update_tournament_by_id(self,
                                tournament_id: str,
                                name: str = None,
                                location: str = None,
                                start_date: str = None,
                                end_date: str = None,
                                number_of_rounds: int = 4,
                                current_round_number: int = 1,
                                rounds: Optional[List[Round]] = None,
                                players: Optional[List[Player]] = None,
                                scores: Optional[Dict[str, float]] = None,
                                description: Optional[str] = None,
                                status: str = "Non démarré",
                                ):
        pass

    @abstractmethod
    def get_by_id(self, tournament_id: str) -> Optional[Tournament]:
        """Return a tournament by ID or None if not found."""
        pass
