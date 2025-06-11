from domain.models.match import Match
from domain.ports.player_repository import IPlayerRepository


def match_with_loaded_players(
        match: Match,
        player_repository: IPlayerRepository
) -> Match:
    """
    Return a new instance of Match with players loaded from their IDs,
    without modifying the existing instance of Match.
    """
    p1, p1_score = match.data[0]
    p2, p2_score = match.data[1]

    return Match(
        player1=player_repository.get_by_id(p1),
        player2=player_repository.get_by_id(p2),
        player1_score=p1_score,
        player2_score=p2_score,
    )