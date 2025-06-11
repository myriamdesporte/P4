from typing import List
from domain.models.player import Player
from domain.models.tournament import Tournament
from domain.ports.player_repository import IPlayerRepository


def tournament_with_loaded_players(
        tournament: Tournament,
        player_repository: IPlayerRepository
) -> Tournament:
    """
    Return a new instance of Tournament with players loaded from their IDs,
    without modifying the existing instance of Tournament.
    """
    loaded_players: List[Player] = []
    for player_id in tournament.players:
        player = player_repository.get_by_id(player_id)
        if player:
            loaded_players.append(player)

    return Tournament(
        name=tournament.name,
        location=tournament.location,
        start_date=tournament.start_date,
        end_date=tournament.end_date,
        number_of_rounds=tournament.number_of_rounds,
        current_round_number=tournament.current_round_number,
        rounds=tournament.rounds,
        players=loaded_players,
        description=tournament.description,
    )