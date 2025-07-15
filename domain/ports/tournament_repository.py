"""Port interface for tournament repository."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from domain.models.player import Player
from domain.models.round import Round
from domain.models.tournament import Tournament


class ITournamentRepository(ABC):
    @abstractmethod
    def load_tournaments(self) -> List[Tournament]:
        """Load all tournaments from the data source."""
        pass

    @abstractmethod
    def save_tournaments(self, tournaments: List[Tournament]) -> None:
        """Save the full list of tournaments to the data source."""
        pass

    @abstractmethod
    def update_tournament_by_id(
            self,
            tournament_id: str,
            name: Optional[str] = None,
            location: Optional[str] = None,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            number_of_rounds: Optional[int] = None,
            current_round_number: Optional[int] = None,
            rounds: Optional[List[Round]] = None,
            players: Optional[List[Player]] = None,
            scores: Optional[Dict[str, float]] = None,
            description: Optional[str] = None,
            status: Optional[str] = None
    ):
        """Update a tournament with the given ID."""
        pass

    @abstractmethod
    def get_by_id(self, tournament_id: str) -> Optional[Tournament]:
        """Return a tournament by ID or None if not found."""
        pass
