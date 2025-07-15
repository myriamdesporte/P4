"""Match-related utilities for handling player references."""

from domain.models.match import Match
from domain.ports.player_repository import IPlayerRepository


def match_with_loaded_players(
        match: Match,
        player_repository: IPlayerRepository
) -> Match:
    """Return a new Match instance with full Player objects loaded from their IDs."""
    p1, p1_score = match.data[0]
    p2, p2_score = match.data[1]

    return Match(
        player1=player_repository.get_by_id(p1),
        player2=player_repository.get_by_id(p2),
        player1_score=p1_score,
        player2_score=p2_score,
    )
