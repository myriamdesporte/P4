from domain.models.round import Round
from domain.ports.player_repository import IPlayerRepository
from infra.utils.match_utils import match_with_loaded_players


def round_with_loaded_players(
        round_instance: Round,
        player_repository: IPlayerRepository
) -> Round:
    """
    Return a new instance of Round with matches containing full Player instances
    loaded from their IDs, without modifying the existing Round.
    """
    loaded_matches = []

    for match in round_instance.matches:
        loaded_match = match_with_loaded_players(match, player_repository)
        loaded_matches.append(loaded_match)

    return Round(
        name=round_instance.name,
        matches=loaded_matches,
        start_datetime=round_instance.start_datetime,
        end_datetime=round_instance.end_datetime,
    )